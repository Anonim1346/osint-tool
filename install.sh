#!/bin/bash
# Installation and setup script

echo "╔════════════════════════════════════╗"
echo "║    OSINT Tool Installation         ║"
echo "╚════════════════════════════════════╝"
echo ""

# Create directories
echo "[*] Creating directories..."
mkdir -p data/databases
mkdir -p data/cache
mkdir -p logs
mkdir -p core
mkdir -p utils
mkdir -p integrations
mkdir -p modules
echo "[✓] Directories created"

# Install Python dependencies
echo ""
echo "[*] Installing Python dependencies..."
pip install -r requirements.txt
echo "[✓] Dependencies installed"

# Create config.json
echo ""
echo "[*] Creating configuration file..."
cat > config.json << 'EOF'
{
  "timeout": 10,
  "retries": 3,
  "output_format": "json",
  "log_level": "INFO",
  "database": {
    "enabled": true,
    "path": "data/osint.db"
  },
  "apis": {
    "enable_hlr": false,
    "enable_viber": true,
    "enable_telegram": true,
    "enable_vk": true,
    "enable_instagram": true,
    "enable_facebook": true,
    "enable_twitter": true,
    "enable_linkedin": true,
    "enable_ip_lookup": true,
    "enable_breach_check": true
  },
  "api_keys": {
    "hlr_api_key": "your_api_key_here",
    "ip_lookup_key": "your_api_key_here",
    "breach_check_key": "your_api_key_here",
    "vk_token": "your_token_here",
    "telegram_token": "your_token_here",
    "instagram_token": "your_token_here",
    "facebook_token": "your_token_here",
    "twitter_token": "your_token_here",
    "linkedin_token": "your_token_here",
    "whois_api_key": "your_api_key_here"
  }
}
EOF
echo "[✓] Configuration file created"

# Create .env file
echo ""
echo "[*] Creating .env file..."
cat > .env << 'EOF'
# OSINT Tool Configuration
DEBUG=False
PORT=5000
TIMEOUT=10
LOG_LEVEL=INFO

# API Keys (optional)
TELEGRAM_BOT_TOKEN=your_token_here
HLR_API_KEY=your_key_here
IP_LOOKUP_KEY=your_key_here
BREACH_CHECK_KEY=your_key_here
EOF
echo "[✓] .env file created"

echo ""
echo "[✓] Installation complete!"
echo ""
echo "Usage:"
echo "  1. Console:     python main.py"
echo "  2. Web API:     python api_server.py"
echo "  3. Telegram:    python telegram_bot.py"
echo ""
echo "First, update config.json with your API keys!"
echo ""
