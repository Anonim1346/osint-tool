#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced Telegram Bot - Enterprise OSINT Tool v2.0
"""

import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from core.advanced_engine import AdvancedOSINTEngine
from core.logger import setup_logger

logger = setup_logger()
engine = AdvancedOSINTEngine()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start command"""
    welcome_text = """
╔════════════════════════════════════════════════════════════╗
║     ADVANCED OSINT TOOL v2.0 - TELEGRAM BOT             ║
║     Enterprise Intelligence Gathering Platform           ║
╚════════════════════════════════════════════════════════════╝

🔍 Search Information Across 18+ Legal Public Sources

📊 Supported Queries:
  📧 Email addresses
  🌐 Domain names
  🔢 IP addresses
  🏢 Company INN/Names
  👤 Person names
  💻 GitHub usernames

📚 Public Sources Include:
  ✓ Court Records & Judiciary
  ✓ Company Registries (EGRUL)
  ✓ News Archives
  ✓ Real Estate Registry
  ✓ Government Data
  ✓ Social Media (Public Profiles)
  ✓ Domain & SSL Information
  ✓ Data Breach Databases
  ✓ Sanctions Lists
  ✓ Financial Disclosures
  ✓ And more...

/help - Show help
/sources - List all available sources
/search - Start searching
    """
    await update.message.reply_text(welcome_text)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Help command"""
    help_text = """
📖 HOW TO USE:

1️⃣ Send any of these:
   📧 user@example.com
   🌐 example.com
   🔢 192.168.1.1
   🏢 Company Name
   👤 Person Name
   💻 github_username

2️⃣ Bot searches all 18+ legal public sources

3️⃣ Receive comprehensive intelligence report

⚠️ IMPORTANT:
• All data from public, legal sources only
• Does NOT access private/restricted data
• Does NOT perform illegal activities
• For intelligence/research purposes only

📋 Commands:
/start - Welcome
/help - This help
/sources - Available sources
/search - Search instructions
/cancel - Stop search
    """
    await update.message.reply_text(help_text)

async def sources(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show available sources"""
    sources_list = engine.get_all_sources()
    
    text = "📚 Available Legal Public Sources:\n\n"
    for source in sources_list:
        text += f"{source}\n"
    
    text += f"\n✅ Total: {len(sources_list)} sources integrated"
    
    # Split if too long
    if len(text) > 4096:
        for chunk in [text[i:i+4096] for i in range(0, len(text), 4096)]:
            await update.message.reply_text(chunk)
    else:
        await update.message.reply_text(text)

async def handle_search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle search query"""
    try:
        query = update.message.text
        
        # Show loading
        loading_msg = await update.message.reply_text("🔍 Searching across 18+ public sources...")
        
        # Perform search
        results = engine.search(query)
        
        # Format response
        response = f"""
🔍 OSINT SEARCH RESULTS

📌 Query: {results['query']}
🏷️  Type: {results['query_type']}
⏰ Time: {results.get('timestamp', 'N/A')}

"""
        
        # Add sources
        if results.get('sources_searched'):
            response += f"📊 Sources: {', '.join(results['sources_searched'])}\n\n"
        
        # Add results
        if results.get('results'):
            for category, data in list(results['results'].items())[:5]:
                if data and 'error' not in data:
                    response += f"▶ {category.upper()}\n"
                    if isinstance(data, dict):
                        for k, v in list(data.items())[:3]:
                            if k not in ['source', 'error']:
                                response += f"  • {k}: {str(v)[:100]}\n"
                    response += "\n"
        
        if not results.get('results'):
            response += "❌ No results found across available sources."
        
        # Delete loading and send results
        try:
            await loading_msg.delete()
        except:
            pass
        
        # Send results (split if needed)
        if len(response) > 4096:
            for chunk in [response[i:i+4096] for i in range(0, len(response), 4096)]:
                await update.message.reply_text(chunk)
        else:
            await update.message.reply_text(response)
    
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Cancel operation"""
    await update.message.reply_text("✅ Operation cancelled")

def main():
    """Start Telegram bot"""
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN not set")
        print("Error: TELEGRAM_BOT_TOKEN environment variable not set")
        return
    
    print("\nStarting Advanced OSINT Telegram Bot...")
    print(f"Bot Token: {token[:10]}...")
    print()
    
    application = Application.builder().token(token).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("sources", sources))
    application.add_handler(CommandHandler("cancel", cancel))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_search))
    
    logger.info("Advanced OSINT Telegram Bot started")
    application.run_polling()

if __name__ == '__main__':
    main()
