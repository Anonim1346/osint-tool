#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced Main Entry Point - Enterprise OSINT Tool v2.0
"""

import sys
import os
from core.advanced_engine import AdvancedOSINTEngine
from core.ui import UserInterface
from core.logger import setup_logger

logger = setup_logger()

def main():
    """
    Main entry point for Advanced OSINT Tool
    """
    print("="*70)
    print("  ADVANCED OSINT TOOL v2.0 - ENTERPRISE EDITION")
    print("  Legal Public Sources Intelligence Gathering")
    print("="*70)
    print()
    
    # Initialize
    ui = UserInterface()
    engine = AdvancedOSINTEngine()
    
    print("Available Sources:")
    print()
    for source in engine.get_all_sources():
        print(f"  {source}")
    print()
    
    try:
        while True:
            # Get user input
            query_input = ui.get_query_input()
            
            if not query_input:
                continue
            
            if query_input.lower() in ['exit', 'quit', 'q']:
                print("\n[*] Exiting Advanced OSINT Tool...")
                break
            
            if query_input.lower() in ['help', 'h']:
                print_help()
                continue
            
            if query_input.lower() in ['sources', 's']:
                print_sources(engine)
                continue
            
            # Process query
            print("\n[*] Processing query across all legal public sources...\n")
            results = engine.search(query_input)
            
            # Display results
            ui.display_advanced_results(results)
            
    except KeyboardInterrupt:
        print("\n\n[!] Program interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Critical error: {str(e)}")
        print(f"[!] Error: {str(e)}")
        sys.exit(1)

def print_help():
    """
    Print help information
    """
    help_text = """
╔═══════════════════════════════════════════════════════════════════╗
║         ADVANCED OSINT TOOL v2.0 - HELP MENU                      ║
╚═══════════════════════════════════════════════════════════════════╝

Supported Input Types:

  📧 EMAIL ADDRESS:
     user@example.com
     Searches: Data breaches, social media, news archives

  🌐 DOMAIN NAME:
     example.com
     Searches: WHOIS, DNS, SSL certificates, CT logs, DNS history

  🔢 IP ADDRESS:
     192.168.1.1
     Searches: Reverse DNS, geolocation, forensic data

  🏢 INN (Russian Company ID):
     7711111111
     Searches: EGRUL, court records, financial data, bankruptcy

  👤 PERSON NAME:
     Ivan Ivanov
     Searches: Court cases, news, social media, government records

  💻 GITHUB USERNAME:
     username
     Searches: GitHub profile, social media, repositories

  🏢 COMPANY NAME:
     Company Name
     Searches: Registries, court, news, financial, real estate

Commands:
  help, h    - Show this help
  sources, s - Show all available sources
  exit, q    - Exit program

Legal Notice:
  This tool searches ONLY public, legal, and openly available sources.
  All data is obtained through legitimate channels.

Limitations:
  - Does NOT access private/restricted databases
  - Does NOT perform any illegal activities
  - Does NOT bypass security or authentication
  - Results depend on data availability
"""
    print(help_text)

def print_sources(engine: AdvancedOSINTEngine):
    """
    Print all available sources
    """
    sources_text = """
╔═══════════════════════════════════════════════════════════════════╗
║         AVAILABLE PUBLIC SOURCES                                   ║
╚═══════════════════════════════════════════════════════════════════╝

"""
    for i, source in enumerate(engine.get_all_sources(), 1):
        sources_text += f"{i:2d}. {source}\n"
    
    sources_text += f"""

Total: {len(engine.get_all_sources())} public sources integrated

Data Reliability:
  ✓ All data from official, government, or widely-recognized sources
  ✓ WHOIS data from domain registrars
  ✓ Court records from official judiciary portals
  ✓ News from public archives
  ✓ Social media public profiles (with proper permissions)
  ✓ Financial data from public registries
  ✓ SSL certificates from Certificate Transparency logs
  ✓ Data breaches from HaveIBeenPwned and public sources
"""
    print(sources_text)

if __name__ == "__main__":
    main()
