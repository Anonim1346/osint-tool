# Advanced OSINT Tool v2.0 - Legal Public Sources

## Overview

This is an **enterprise-grade OSINT (Open Source Intelligence) tool** that searches across **18+ legal public sources** for comprehensive information gathering.

**Important:** This tool uses ONLY public, legal, and officially available sources.

## Features

### 🔍 18+ Legal Public Sources

1. **Company Registries**
   - EGRUL (Russian Federal Tax Service)
   - Rosreestr (Real Estate Registry)
   - Company information databases

2. **Court Records**
   - Federal Courts System
   - Judicial decisions
   - Case information

3. **News & Media**
   - News archives
   - Press releases
   - Media databases

4. **Real Estate**
   - Property registry
   - Cadastre data
   - Address information

5. **Social Media (Public Data)**
   - VKontakte public profiles
   - Telegram public channels
   - LinkedIn public profiles
   - GitHub profiles
   - Twitter public data

6. **Domain & Website**
   - WHOIS lookup
   - DNS records
   - SSL certificates
   - Certificate Transparency logs

7. **Financial Data**
   - Stock ownership
   - Financial disclosures
   - Company financial information

8. **Data Breaches**
   - HaveIBeenPwned
   - Public breach databases
   - Paste sites archives

9. **Government & Legislative**
   - Parliament members
   - Government contracts
   - Legislative data

10. **Sanctions & Compliance**
    - UN sanctions lists
    - OFAC lists
    - EU sanctions

11. **And 7+ more sources**

## Installation

```bash
# Clone repository
git clone https://github.com/Anonim1346/osint-tool.git
cd osint-tool

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Console Application

```bash
python advanced_main.py
```

Supported queries:
- Email: `user@example.com`
- Domain: `example.com`
- IP: `192.168.1.1`
- Company INN: `7711111111`
- Person: `Ivan Ivanov`
- GitHub: `username`

### Web API

```bash
python advanced_api_server.py
```

Endpoints:
- `POST /api/v2/search` - Perform search
- `GET /api/v2/sources` - List sources
- `GET /api/v2/info` - Tool information

### Telegram Bot

```bash
export TELEGRAM_BOT_TOKEN="your_token_here"
python advanced_telegram_bot.py
```

## Architecture

```
core/
├── legal_sources.py       # All 18+ public sources
├── advanced_engine.py     # Search engine
├── ui.py                  # User interface
├── logger.py              # Logging
└── config.py              # Configuration

advanced_main.py           # Console application
advanced_api_server.py     # Flask API
advanced_telegram_bot.py   # Telegram Bot
```

## Legal Notice

⚠️ **IMPORTANT:**

1. **This tool searches ONLY public and legal sources**
2. Does NOT access private or restricted databases
3. Does NOT perform hacking or unauthorized access
4. Does NOT bypass security or authentication
5. All data gathering is completely legal and transparent
6. Users are responsible for complying with local laws

## Data Sources Compliance

All data is obtained through:
- ✅ Official government portals
- ✅ Public registries
- ✅ News archives
- ✅ Legitimate APIs
- ✅ Public social media profiles
- ✅ WHOIS and DNS services
- ✅ Certificate transparency logs
- ✅ Official sanctioning lists

## Use Cases

- 🔍 Due diligence research
- 📊 Competitive intelligence
- 🛡️ Fraud detection
- 💼 Background verification
- 📈 Market research
- 🔐 Security analysis
- 📰 Investigative journalism
- 🏛️ Compliance checking

## Requirements

```
requests>=2.28.0
flask>=2.0.0
flask-cors>=3.0.0
python-telegram-bot>=13.0
python-dotenv>=0.19.0
```

## Configuration

Create `.env` file:

```bash
TELEGRAM_BOT_TOKEN=your_token_here
DEBUG=False
PORT=5000
```

## Performance

- Multi-source parallel searching
- Result caching
- Optimized API calls
- Handles large result sets

## Support

For questions or issues:
1. Check `/help` command in CLI
2. Review source code comments
3. Check API documentation at `/api/v2/info`

## Disclaimer

This tool is provided for educational and legitimate research purposes only. Users are solely responsible for ensuring their use complies with all applicable laws and regulations in their jurisdiction.

## License

This project is for legal use only. Use at your own responsibility.

---

**Advanced OSINT Tool v2.0 - Enterprise Edition**
*Legal. Comprehensive. Professional.*
