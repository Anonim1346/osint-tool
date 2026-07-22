#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram Bot - OSINT Tool as Telegram Bot
"""

import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from core.osint_engine import OSINTEngine
from core.logger import setup_logger

logger = setup_logger()
engine = OSINTEngine()

SEARCH = range(1)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start command"""
    welcome_text = """
╔════════════════════════════════════╗
║     OSINT Tool Telegram Bot        ║
║  Advanced Information Search       ║
╚════════════════════════════════════╝

🔍 Supported searches:
  📱 Phone numbers
  👤 Full names
  🚗 Car numbers
  🛂 Passport numbers
  📧 Email addresses
  🌐 IP addresses
  🚗 VIN numbers

📝 Just send me your query and I'll search for all available information!

/help - Show help
/history - View search history
/settings - Configure bot
    """
    await update.message.reply_text(welcome_text)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Help command"""
    help_text = """
💡 How to use:

1️⃣ Send any of these:
   • Phone: +7 (999) 999-99-99
   • Name: Ivan Ivanov
   • Car: А123БВ77
   • Passport: 1234567890
   • Email: user@example.com
   • IP: 192.168.1.1

2️⃣ Bot will search all available sources

3️⃣ Results will be formatted nicely

📊 Commands:
   /start - Start
   /help - This help
   /history - Recent searches
   /settings - Configure
   /cancel - Cancel operation
    """
    await update.message.reply_text(help_text)

async def handle_search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle search query"""
    try:
        query = update.message.text
        
        # Show loading message
        loading_msg = await update.message.reply_text("🔍 Searching...")
        
        # Perform search
        results = engine.search(query)
        
        # Format response
        response = f"""🔍 Search Results
        
Query: {results['query']}
Type: {results['query_type']}
"""
        
        # Add results
        if results.get('results'):
            for category, data in results['results'].items():
                if data and not isinstance(data, dict) or (isinstance(data, dict) and data.get('error') is None):
                    response += f"\n📌 {category.upper()}\n"
                    
                    if isinstance(data, dict):
                        for key, value in list(data.items())[:5]:  # Limit to 5 items
                            if key not in ['error', 'status', 'sources']:
                                if isinstance(value, (list, dict)):
                                    response += f"  • {key}: (complex data)\n"
                                else:
                                    response += f"  • {key}: {value}\n"
        
        if not results.get('results'):
            response += "\n❌ No results found"
        
        # Delete loading message and send results
        await loading_msg.delete()
        
        # Split long messages
        if len(response) > 4096:
            for chunk in [response[i:i+4096] for i in range(0, len(response), 4096)]:
                await update.message.reply_text(chunk)
        else:
            await update.message.reply_text(response)
    
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def history(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show search history"""
    try:
        # TODO: Implement history retrieval from database
        await update.message.reply_text("📋 Search history feature coming soon!")
    except Exception as e:
        logger.error(f"History error: {str(e)}")
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel operation"""
    await update.message.reply_text("✅ Operation cancelled")
    return ConversationHandler.END

def main():
    """Start Telegram bot"""
    # Get token from environment
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN not set")
        print("Error: TELEGRAM_BOT_TOKEN environment variable not set")
        return
    
    # Create application
    application = Application.builder().token(token).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("history", history))
    application.add_handler(CommandHandler("cancel", cancel))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_search))
    
    # Start bot
    logger.info("Starting Telegram bot...")
    application.run_polling()

if __name__ == '__main__':
    main()
