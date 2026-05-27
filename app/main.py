from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional
from app.config import settings
import aiohttp
import logging
import whois
import dns.resolver
import re

logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="Open Source Intelligence Tool",
    docs_url="/api/docs"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter(prefix="/api/search")

# ===== Models =====
class EmailSearchRequest(BaseModel):
    email: EmailStr
    include_breaches: bool = True

class EmailSearchResponse(BaseModel):
    email: str
    breaches: list = []
    compromised: bool = False
    summary: Optional[str] = None

class PhoneSearchRequest(BaseModel):
    phone: str

class PhoneSearchResponse(BaseModel):
    phone: str
    valid: bool
    country: Optional[str] = None
    breaches: list = []

class DomainSearchRequest(BaseModel):
    domain: str

class DomainSearchResponse(BaseModel):
    domain: str
    registrar: Optional[str] = None
    dns_records: list = []
    age_days: Optional[int] = None

class IPSearchRequest(BaseModel):
    ip: str

class IPSearchResponse(BaseModel):
    ip: str
    country: Optional[str] = None
    city: Optional[str] = None
    isp: Optional[str] = None
    organization: Optional[str] = None

class UsernameSearchRequest(BaseModel):
    username: str

class UsernameSearchResponse(BaseModel):
    username: str
    accounts: list = []
    found_count: int = 0

# ===== HIBP Integration =====
async def check_email_breaches(email: str) -> list:
    if not settings.HIBP_API_KEY:
        return []
    
    try:
        headers = {
            "User-Agent": "OSINT-Tool",
            "hibp-api-key": settings.HIBP_API_KEY
        }
        
        url = f"{settings.HIBP_API_URL}/breachedaccount"
        params = {"account": email, "truncateResponse": False}
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status == 200:
                    breaches = await response.json()
                    return [{"name": b.get("Name"), "date": b.get("BreachDate")} for b in breaches]
                elif response.status == 404:
                    return []
    except Exception as e:
        logger.error(f"HIBP error: {str(e)}")
    
    return []

# ===== Phone Parser =====
def parse_phone(phone: str) -> dict:
    cleaned = re.sub(r'[\s\-\(\)\+]', '', phone)
    
    if not re.match(r'^\d{7,15}$', cleaned):
        return {"valid": False}
    
    country_codes = {
        "1": "US/Canada", "7": "Russia", "44": "UK", "33": "France",
        "49": "Germany", "39": "Italy", "34": "Spain"
    }
    
    country = None
    for prefix, c in country_codes.items():
        if cleaned.startswith(prefix):
            country = c
            break
    
    return {"valid": True, "phone": cleaned, "country": country}

# ===== WHOIS =====
def get_whois(domain: str) -> dict:
    try:
        from datetime import datetime
        w = whois.whois(domain)
        
        created_date = w.creation_date
        if created_date:
            if isinstance(created_date, list):
                created_date = created_date[0]
            age_days = (datetime.now() - created_date).days
        else:
            age_days = None
        
        return {
            "domain": domain,
            "registrar": str(w.registrar) if w.registrar else None,
            "age_days": age_days,
            "name_servers": w.name_servers if w.name_servers else []
        }
    except Exception as e:
        logger.error(f"WHOIS error: {str(e)}")
        return {}

# ===== DNS =====
async def get_dns_records(domain: str) -> list:
    records = []
    record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT']
    
    for rtype in record_types:
        try:
            answers = dns.resolver.resolve(domain, rtype)
            for answer in answers:
                records.append({"type": rtype, "value": str(answer)})
        except:
            pass
    
    return records

def find_subdomains(domain: str) -> list:
    subdomains = []
    common = ['www', 'mail', 'ftp', 'admin', 'test', 'api', 'cdn', 'git']
    
    for sub in common:
        try:
            dns.resolver.resolve(f"{sub}.{domain}", 'A')
            subdomains.append(f"{sub}.{domain}")
        except:
            pass
    
    return subdomains

# ===== IP Geolocation =====
async def get_ip_info(ip: str) -> dict:
    try:
        url = f"{settings.IPAPI_URL}/{ip}"
        params = {"fields": "status,country,city,isp,org,as"}
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("status") == "success":
                        return {
                            "ip": ip,
                            "country": data.get("country"),
                            "city": data.get("city"),
                            "isp": data.get("isp"),
                            "organization": data.get("org"),
                            "asn": data.get("as")
                        }
    except Exception as e:
        logger.error(f"IP API error: {str(e)}")
    
    return {"ip": ip}

# ===== Social Media Check =====
async def check_username(username: str) -> list:
    platforms = [
        ("GitHub", f"https://github.com/{username}"),
        ("Twitter", f"https://twitter.com/{username}"),
        ("Instagram", f"https://www.instagram.com/{username}/"),
        ("Reddit", f"https://www.reddit.com/user/{username}/"),
        ("LinkedIn", f"https://www.linkedin.com/in/{username}/"),
        ("YouTube", f"https://www.youtube.com/@{username}"),
    ]
    
    results = []
    async with aiohttp.ClientSession() as session:
        for name, url in platforms:
            try:
                async with session.head(url, allow_redirects=True, timeout=aiohttp.ClientTimeout(total=5)) as resp:
                    found = resp.status == 200
                    results.append({"platform": name, "url": url if found else None, "found": found})
            except:
                results.append({"platform": name, "url": None, "found": False})
    
    return results

# ===== Endpoints =====
@app.get("/")
async def root():
    return {
        "name": "OSINT Tool API",
        "version": settings.API_VERSION,
        "docs": "/api/docs",
        "status": "running"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

@router.post("/email", response_model=EmailSearchResponse)
async def search_email(request: EmailSearchRequest):
    """Search email in breaches and find related accounts"""
    try:
        breaches = await check_email_breaches(request.email)
        
        result = {
            "email": request.email,
            "breaches": breaches,
            "compromised": len(breaches) > 0,
            "summary": f"Found in {len(breaches)} breach(es)" if breaches else "Not found in known breaches"
        }
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/phone", response_model=PhoneSearchResponse)
async def search_phone(request: PhoneSearchRequest):
    """Search phone number"""
    try:
        parsed = parse_phone(request.phone)
        breaches = await check_email_breaches(request.phone)
        
        result = {
            "phone": request.phone,
            "valid": parsed.get("valid", False),
            "country": parsed.get("country"),
            "breaches": breaches
        }
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/domain", response_model=DomainSearchResponse)
async def search_domain(request: DomainSearchRequest):
    """Search domain information"""
    try:
        whois_data = get_whois(request.domain)
        dns_records = await get_dns_records(request.domain)
        subdomains = find_subdomains(request.domain)
        
        result = {
            "domain": request.domain,
            "registrar": whois_data.get("registrar"),
            "age_days": whois_data.get("age_days"),
            "dns_records": dns_records + [{"type": "subdomain", "value": s} for s in subdomains]
        }
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ip", response_model=IPSearchResponse)
async def search_ip(request: IPSearchRequest):
    """Search IP address"""
    try:
        ip_info = await get_ip_info(request.ip)
        return ip_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/username", response_model=UsernameSearchResponse)
async def search_username(request: UsernameSearchRequest):
    """Search username across platforms"""
    try:
        accounts = await check_username(request.username)
        found_count = sum(1 for a in accounts if a.get("found"))
        
        result = {
            "username": request.username,
            "accounts": accounts,
            "found_count": found_count
        }
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
