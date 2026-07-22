#!/bin/bash

# Advanced OSINT Tool v2.0 - Installation Script

echo "================================================"
echo "   Advanced OSINT Tool v2.0 - Installer"
echo "   Legal Public Sources Intelligence"
echo "================================================"
echo ""

# Check Python version
echo "[*] Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "[+] Python version: $python_version"
echo ""

# Check pip
echo "[*] Checking pip..."
if ! command -v pip3 &> /dev/null; then
    echo "[!] pip3 not found. Installing..."
    sudo apt-get install python3-pip
fi
echo "[+] pip found"
echo ""

# Create virtual environment
echo "[*] Creating virtual environment..."
python3 -m venv venv
echo "[+] Virtual environment created"
echo ""

# Activate virtual environment
echo "[*] Activating virtual environment..."
source venv/bin/activate
echo "[+] Virtual environment activated"
echo ""

# Upgrade pip
echo "[*] Upgrading pip..."
pip install --upgrade pip
echo "[+] pip upgraded"
echo ""

# Install requirements
echo "[*] Installing dependencies..."
pip install -r requirements.txt
echo "[+] Dependencies installed"
echo ""

# Create logs directory
echo "[*] Creating directories..."
mkdir -p logs
mkdir -p data
echo "[+] Directories created"
echo ""

# Create .env file
if [ ! -f .env ]; then
    echo "[*] Creating .env file..."
    cat > .env << EOF
# Advanced OSINT Tool v2.0 Configuration

# Telegram Bot
TELEGRAM_BOT_TOKEN=your_token_here

# API Configuration
DEBUG=False
PORT=5000
HOST=0.0.0.0

# Logging
LOG_LEVEL=INFO
EOF
    echo "[+] .env file created"
    echo "[!] Please update .env with your configuration"
fi
echo ""

echo "================================================"
echo "   Installation Complete!"
echo "================================================"
echo ""
echo "Next steps:"
echo "  1. Edit .env file with your configuration"
echo "  2. Run: source venv/bin/activate"
echo "  3. Run: python main.py"
echo ""
echo "Usage:"
echo "  Console:    python main.py"
echo "  API:        python api_server.py"
echo "  Telegram:   python telegram_bot.py"
echo ""
