#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Universal OSINT Tool - Search all information about users
Version 1.0
"""

import sys
import os
from core.osint_engine import OSINTEngine
from core.ui import UserInterface
from core.logger import setup_logger

# Setup logger
logger = setup_logger()

def main():
    """
    Main entry point for OSINT Tool
    """
    print("="*60)
    print("Universal OSINT Tool v1.0")
    print("Advanced Information Search System")
    print("="*60)
    print()
    
    # Initialize UI
    ui = UserInterface()
    
    # Initialize OSINT Engine
    engine = OSINTEngine()
    
    try:
        while True:
            # Get user input
            query_input = ui.get_query_input()
            
            if not query_input:
                continue
            
            if query_input.lower() in ['exit', 'quit', 'q']:
                print("\n[*] Exiting OSINT Tool...")
                break
            
            # Process query
            print("\n[*] Processing query...\n")
            results = engine.search(query_input)
            
            # Display results
            ui.display_results(results)
            
    except KeyboardInterrupt:
        print("\n\n[!] Program interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Critical error: {str(e)}")
        print(f"[!] Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
