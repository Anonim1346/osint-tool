# Advanced OSINT Tool v2.0 - Enterprise Edition

![OSINT](https://img.shields.io/badge/OSINT-Tool-blue)
![Version](https://img.shields.io/badge/Version-2.0-green)
![Legal](https://img.shields.io/badge/Legal-Public%20Sources-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8+-blue)

## 📋 Overview

**Advanced OSINT Tool v2.0** is an enterprise-grade intelligence gathering platform that searches across **18+ legal public sources** for comprehensive information.

> **Important:** This tool uses ONLY public, legal, and officially available sources. All operations are completely transparent and legitimate.

---

## 🎯 Key Features

### 🔍 18+ Legal Public Sources

- **Company Registries** - EGRUL, Rosreestr, company databases
- **Court Records** - Federal courts, judicial decisions
- **News & Media** - Archives, press releases, media databases
- **Real Estate** - Property registry, cadastre data
- **Social Media** - VK, Telegram, LinkedIn, GitHub (public data)
- **Domain & Web** - WHOIS, DNS, SSL, Certificate Transparency
- **Financial Data** - Stock ownership, disclosures
- **Data Breaches** - HaveIBeenPwned, breach archives
- **Government** - Parliament members, contracts
- **Sanctions** - UN, OFAC, EU sanctions lists
- **Education** - University and education records
- **Health** - Public health statistics
- **IP Geolocation** - Location data
- **Forensics** - DNS history, certificates
- **And more...**

### 💻 Three Interfaces

1. **Console Application** - Interactive CLI
2. **Web API** - RESTful endpoints
3. **Telegram Bot** - Chat interface

---

## ⚡ Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/Anonim1346/osint-tool.git
cd osint-tool

# Install dependencies
pip install -r requirements.txt
```

### Usage

#### Console
```bash
python main.py
```

#### Web API
```bash
python api_server.py
# Access at http://localhost:5000
```

#### Telegram Bot
```bash
export TELEGRAM_BOT_TOKEN="your_token_here"
python telegram_bot.py
```

---

## 📖 Documentation

### Supported Query Types

```
📧 EMAIL ADDRESS
  user@example.com
  → Data breaches, social media, news

🌐 DOMAIN NAME
  example.com
  → WHOIS, DNS, SSL, CT logs

🔢 IP ADDRESS
  192.168.1.1
  → Geolocation, reverse DNS, forensics

🏢 COMPANY INN (Russian)
  7711111111
  → EGRUL, court records, financial data

👤 PERSON NAME
  Ivan Ivanov
  → Court cases, news, social media, government

💻 GITHUB USERNAME
  username
  → GitHub profile, repositories, social media

🏪 COMPANY NAME
  Company Name
  → Registries, court, news, financial
```

### API Endpoints

```bash
# Search
POST /api/v2/search
Body: {"query": "search_query"}

# Get sources
GET /api/v2/sources

# Tool information
GET /api/v2/info

# Health check
GET /health
```

### Console Commands

```
help, h     - Show help menu
sources, s  - List all available sources
exit, q     - Exit program
```

---

## 🏗️ Project Structure

```
osint-tool/
├── main.py                   # Console entry point
├── api_server.py             # API entry point
├── telegram_bot.py           # Telegram entry point
├── advanced_main.py          # Console implementation
├── advanced_api_server.py    # API implementation
├── advanced_telegram_bot.py  # Telegram implementation
├── requirements.txt          # Dependencies
├── README.md                 # This file
├── ADVANCED_README.md        # Detailed documentation
└── core/
    ├── advanced_engine.py    # Search engine
    ├── legal_sources.py      # 18+ public sources
    ├── ui.py                 # User interface
    ├── logger.py             # Logging
    └── config.py             # Configuration
```

---

## 📊 Sources Information

### Government & Official
- Russian Federal Tax Service (EGRUL)
- Rosreestr (Real Estate Registry)
- Federal Courts System
- Parliament Registry

### Financial
- Stock market data
- Financial disclosures
- Company information

### Internet & Technical
- WHOIS registries
- DNS services
- Certificate Transparency logs
- IP geolocation

### Media & News
- News archives
- Press releases
- Media databases

### Social Media (Public)
- VKontakte public profiles
- Telegram public channels
- LinkedIn public profiles
- GitHub public repositories

### Compliance
- UN sanctions lists
- OFAC lists
- EU sanctions
- International blacklists

### Security
- HaveIBeenPwned
- Data breach archives
- Public paste sites

---

## 🔒 Legal & Compliance

### ✅ What This Tool Does
- Searches ONLY public sources
- Uses official APIs and portals
- Respects robots.txt and TOS
- Provides transparent data retrieval
- Follows GDPR and data protection laws

### ❌ What This Tool Does NOT Do
- Access private/restricted databases
- Perform hacking or unauthorized access
- Bypass authentication or security
- Violate anyone's privacy
- Perform illegal activities

### ⚖️ Legal Notice

**IMPORTANT:** This tool is for legitimate research, due diligence, and intelligence gathering purposes only. Users are solely responsible for ensuring compliance with all applicable laws and regulations in their jurisdiction. Misuse of this tool for illegal purposes is prohibited.

---

## 💼 Use Cases

- **Due Diligence** - Verify business partners and contractors
- **Fraud Detection** - Identify suspicious activities
- **Background Checks** - Employee and vendor verification
- **Competitive Intelligence** - Market research
- **Risk Assessment** - Identify potential risks
- **Investigative Journalism** - Public interest research
- **Academic Research** - Information gathering
- **Compliance Checking** - Regulatory verification

---

## 📦 Requirements

```
Python 3.8+
requests>=2.28.0
flask>=2.0.0
flask-cors>=3.0.0
python-telegram-bot>=13.0
python-dotenv>=0.19.0
```

---

## 🔧 Configuration

Create `.env` file in project root:

```bash
# Telegram
TELEGRAM_BOT_TOKEN=your_token_here

# API
DEBUG=False
PORT=5000
HOST=0.0.0.0

# Logging
LOG_LEVEL=INFO
```

---

## 🚀 Performance

- **Multi-source searching** - Parallel API queries
- **Result caching** - Improved response times
- **Optimized queries** - Efficient API usage
- **Large datasets** - Handles extensive results
- **Rate limiting** - Respects API limits

---

## 📝 Examples

### Console Example
```bash
$ python main.py
============================================================
  ADVANCED OSINT TOOL v2.0 - ENTERPRISE EDITION
  Legal Public Sources Intelligence Gathering
============================================================

[OSINT] Enter search query: user@example.com

[*] Processing query across all legal public sources...

============================================================
OSINT SEARCH RESULTS - ADVANCED
============================================================

Query: user@example.com
Type: email
Timestamp: 2024-01-15 10:30:45

Sources Searched: Data Breaches, Social Media, News

▶ DATA_BREACHES
  Source: HaveIBeenPwned
  Breaches found: Yes
```

### API Example
```bash
curl -X POST http://localhost:5000/api/v2/search \
  -H "Content-Type: application/json" \
  -d '{"query": "example.com"}'
```

### Telegram Bot
```
Just send any query to the bot and it searches all sources!
```

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

---

## 📞 Support

- Check `/help` command in console
- Review `ADVANCED_README.md`
- Visit API docs at `/api/v2/info`
- Check logs in `logs/` directory

---

## 📄 License

This project is provided for legal and legitimate use only.

---

## ⚠️ Disclaimer

This tool is provided as-is for educational and research purposes. Users are solely responsible for ensuring their use complies with all applicable laws and regulations. The authors assume no liability for misuse or illegal activities.

---

## 👨‍💻 About

**Advanced OSINT Tool v2.0** - Enterprise Intelligence Gathering Platform

- **Legal** - Uses only public sources
- **Comprehensive** - 18+ integrated sources
- **Professional** - Enterprise-grade code
- **Transparent** - Open and honest approach

---

**Made with ❤️ for legitimate research and intelligence gathering**
