#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced OSINT Engine with Legal Public Sources
Version 2.0
"""

import re
from typing import Dict, List, Any
from core.logger import setup_logger
from core.legal_sources import (
    CompanyRegistry,
    CourtRegistry,
    PublicRecords,
    NewsAndMedia,
    RealEstateRegistry,
    PublicSocialMedia,
    DomainAndWebsite,
    EducationRecords,
    TravelAndMobility,
    PublicHealthData,
    PublicFinancialData,
    ForensicData,
    DataBreach,
    LegislativeData
)

logger = setup_logger()

class AdvancedOSINTEngine:
    """
    Advanced OSINT Engine with all legal public sources
    """
    
    def __init__(self):
        self.company_registry = CompanyRegistry()
        self.court_registry = CourtRegistry()
        self.public_records = PublicRecords()
        self.news_media = NewsAndMedia()
        self.real_estate = RealEstateRegistry()
        self.social_media = PublicSocialMedia()
        self.domain_web = DomainAndWebsite()
        self.education = EducationRecords()
        self.travel = TravelAndMobility()
        self.health = PublicHealthData()
        self.financial = PublicFinancialData()
        self.forensic = ForensicData()
        self.breach = DataBreach()
        self.legislative = LegislativeData()
        
        logger.info("Advanced OSINT Engine initialized with all legal public sources")
    
    def identify_query_type(self, query: str) -> tuple:
        """
        Identify query type and clean data
        """
        query = query.strip()
        
        # Email
        if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', query):
            return ('email', query.lower())
        
        # Domain
        if re.match(r'^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$', query):
            return ('domain', query.lower())
        
        # IP address
        if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', query):
            return ('ip', query)
        
        # INN (Russian tax number - 10 or 12 digits)
        if re.match(r'^\d{10}$|^\d{12}$', query):
            return ('inn', query)
        
        # GitHub username
        if re.match(r'^[a-zA-Z0-9]([a-zA-Z0-9-]{0,38}[a-zA-Z0-9])?$', query) and len(query) > 2:
            return ('github', query)
        
        # Person name (multiple words with Cyrillic or Latin)
        if len(query.split()) >= 2 and re.search(r'[а-яА-ЯёЁ\w\s]', query):
            return ('person', query)
        
        # Company name
        if len(query) > 3:
            return ('company', query)
        
        return ('general', query)
    
    def search(self, query: str) -> Dict[str, Any]:
        """
        Perform comprehensive search across all legal public sources
        """
        query_type, cleaned_query = self.identify_query_type(query)
        
        results = {
            'query': query,
            'query_type': query_type,
            'cleaned_query': cleaned_query,
            'sources_searched': [],
            'results': {}
        }
        
        logger.info(f"Advanced search for: {query} (Type: {query_type})")
        
        try:
            if query_type == 'email':
                results['results'].update(self._search_email(cleaned_query))
                results['sources_searched'].extend(['Data Breaches', 'Social Media', 'News'])
            
            elif query_type == 'domain':
                results['results'].update(self._search_domain(cleaned_query))
                results['sources_searched'].extend(['WHOIS', 'DNS', 'SSL', 'Certificate Transparency'])
            
            elif query_type == 'ip':
                results['results'].update(self._search_ip(cleaned_query))
                results['sources_searched'].extend(['Geolocation', 'Forensics', 'DNS'])
            
            elif query_type == 'inn':
                results['results'].update(self._search_company(cleaned_query))
                results['sources_searched'].extend(['EGRUL', 'Court Records', 'Financial'])
            
            elif query_type == 'github':
                results['results'].update(self._search_github(cleaned_query))
                results['sources_searched'].extend(['GitHub', 'Social Media'])
            
            elif query_type == 'person':
                results['results'].update(self._search_person(cleaned_query))
                results['sources_searched'].extend(['Court Records', 'News', 'Social Media', 'Financial', 'Legislative'])
            
            elif query_type == 'company':
                results['results'].update(self._search_company(cleaned_query))
                results['sources_searched'].extend(['EGRUL', 'Court', 'News', 'Financial'])
            
            else:
                results['results'].update(self._search_general(cleaned_query))
        
        except Exception as e:
            logger.error(f"Search error: {str(e)}")
            results['error'] = str(e)
        
        return results
    
    def _search_email(self, email: str) -> Dict:
        """
        Search email across public sources
        """
        results = {}
        
        try:
            # Data breaches
            results['data_breaches'] = self.breach.search_breaches(email)
            
            # Social media
            results['social_media'] = self.social_media.search_vk_public(email)
            
            # News
            results['news'] = self.news_media.search_news_archives(email)
        
        except Exception as e:
            logger.error(f"Email search error: {str(e)}")
        
        return results
    
    def _search_domain(self, domain: str) -> Dict:
        """
        Search domain across public sources
        """
        results = {}
        
        try:
            # WHOIS
            results['whois'] = self.domain_web.whois_lookup(domain)
            
            # DNS records
            results['dns_records'] = self.domain_web.dns_records(domain)
            
            # SSL certificate
            results['ssl_certificate'] = self.domain_web.ssl_certificate_info(domain)
            
            # Certificate Transparency
            results['certificate_transparency'] = self.forensic.search_certificate_transparency(domain)
            
            # DNS history
            results['dns_history'] = self.forensic.search_dns_history(domain)
        
        except Exception as e:
            logger.error(f"Domain search error: {str(e)}")
        
        return results
    
    def _search_ip(self, ip: str) -> Dict:
        """
        Search IP address across public sources
        """
        results = {}
        
        try:
            # Reverse DNS
            results['reverse_dns'] = self.domain_web.dns_records(ip)
            
            # Geolocation from public APIs
            results['geolocation'] = {
                'source': 'IP Geolocation',
                'note': 'Using public geolocation databases'
            }
        
        except Exception as e:
            logger.error(f"IP search error: {str(e)}")
        
        return results
    
    def _search_company(self, query: str) -> Dict:
        """
        Search company information
        """
        results = {}
        
        try:
            # Company registry
            results['company_info'] = self.company_registry.search_company_by_name(query)
            
            # EGRUL (if INN provided)
            if re.match(r'^\d{10}$|^\d{12}$', query):
                results['egrul'] = self.company_registry.search_egrul(query)
            
            # Court records
            results['court_cases'] = self.court_registry.search_court_decisions(query)
            
            # News
            results['news'] = self.news_media.search_news_archives(query)
            
            # Financial data
            results['financial'] = self.financial.search_stock_ownership(query)
            
            # Bankruptcy status
            results['bankruptcy'] = self.public_records.search_bankruptcy_registry(query)
            
            # Real estate
            results['real_estate'] = self.real_estate.search_property(query)
        
        except Exception as e:
            logger.error(f"Company search error: {str(e)}")
        
        return results
    
    def _search_person(self, name: str) -> Dict:
        """
        Search person information
        """
        results = {}
        
        try:
            # Court records
            results['court_cases'] = self.court_registry.search_person_cases(name)
            
            # News archives
            results['news'] = self.news_media.search_news_archives(name)
            
            # Social media
            results['vk'] = self.social_media.search_vk_public(name)
            results['telegram'] = self.social_media.search_telegram_public(name)
            results['linkedin'] = self.social_media.search_linkedin_public(name)
            
            # Legislative records (if public official)
            results['government'] = self.legislative.search_parliament_members(name)
            
            # Financial disclosures
            results['financial_disclosure'] = self.financial.search_financial_disclosures(name)
            
            # Sanctions lists
            results['sanctions'] = self.public_records.search_sanctions_lists(name)
        
        except Exception as e:
            logger.error(f"Person search error: {str(e)}")
        
        return results
    
    def _search_github(self, username: str) -> Dict:
        """
        Search GitHub profile
        """
        results = {}
        
        try:
            # GitHub profile
            results['github'] = self.social_media.search_github(username)
            
            # Related social media
            results['social_media'] = self.social_media.search_vk_public(username)
        
        except Exception as e:
            logger.error(f"GitHub search error: {str(e)}")
        
        return results
    
    def _search_general(self, query: str) -> Dict:
        """
        General search across multiple sources
        """
        results = {}
        
        try:
            # News
            results['news'] = self.news_media.search_news_archives(query)
            
            # Court
            results['court'] = self.court_registry.search_court_decisions(query)
            
            # Social media
            results['social_media'] = self.social_media.search_vk_public(query)
        
        except Exception as e:
            logger.error(f"General search error: {str(e)}")
        
        return results
    
    def get_all_sources(self) -> List[str]:
        """
        Get list of all available legal public sources
        """
        return [
            '📊 Company Registries (EGRUL, Rosreestr)',
            '⚖️ Court Records & Judicial Decisions',
            '🎬 News Archives & Media',
            '🏠 Real Estate Registry',
            '👥 Public Social Media Profiles',
            '🌐 Domain & Website Information',
            '📜 Government & Legislative Data',
            '🎓 Education Records',
            '💼 Financial Disclosures',
            '🔐 Data Breach Information',
            '🔍 Forensic & Technical Data',
            '🚫 Sanctions Lists & Blacklists',
            '📍 IP Geolocation',
            '🏦 Bankruptcy Registry',
            '✈️ Travel & Mobility Data',
            '🏥 Public Health Statistics',
            '💻 GitHub & Developer Profiles',
            '📱 SSL Certificates & CT Logs'
        ]
