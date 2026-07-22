#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
User Interface Module
"""

from typing import Dict, Any
import json

class UserInterface:
    """
    User interface for OSINT tool
    """
    
    def __init__(self):
        self.color_codes = {
            'green': '\033[92m',
            'red': '\033[91m',
            'yellow': '\033[93m',
            'blue': '\033[94m',
            'purple': '\033[95m',
            'cyan': '\033[96m',
            'reset': '\033[0m',
            'bold': '\033[1m'
        }
    
    def get_query_input(self) -> str:
        """
        Get input from user
        """
        try:
            query = input(f"\n{self.color_codes['cyan']}[OSINT]{self.color_codes['reset']} Enter search query: ").strip()
            return query
        except EOFError:
            return ""
    
    def display_results(self, results: Dict[str, Any]):
        """
        Display search results in formatted way
        """
        if not results or not results.get('results'):
            print(f"{self.color_codes['yellow']}[!] No results found{self.color_codes['reset']}")
            return
        
        print(f"\n{self.color_codes['green']}{'='*60}{self.color_codes['reset']}")
        print(f"{self.color_codes['bold']}SEARCH RESULTS{self.color_codes['reset']}")
        print(f"{self.color_codes['green']}{'='*60}{self.color_codes['reset']}\n")
        
        print(f"Query: {results['query']}")
        print(f"Type: {results['query_type']}")
        print()
        
        # Display results by category
        for category, data in results['results'].items():
            self._display_category(category, data)
        
        # Display errors if any
        if results.get('errors'):
            print(f"\n{self.color_codes['red']}[!] Errors:{self.color_codes['reset']}")
            for error in results['errors']:
                print(f"  - {error}")
        
        print(f"\n{self.color_codes['green']}{'='*60}{self.color_codes['reset']}\n")
    
    def _display_category(self, category: str, data: Dict[str, Any]):
        """
        Display single category of results
        """
        print(f"{self.color_codes['blue']}[*] {category.upper().replace('_', ' ')}{self.color_codes['reset']}")
        
        if isinstance(data, dict):
            if data.get('sources'):
                print(f"    Sources: {', '.join(data['sources'])}")
            
            # Display main fields
            for key, value in data.items():
                if key not in ['sources', 'status'] and value is not None:
                    if isinstance(value, (dict, list)):
                        print(f"    {key}: {json.dumps(value, ensure_ascii=False, indent=6)}")
                    else:
                        print(f"    {key}: {value}")
        
        print()
    
    def display_help(self):
        """
        Display help information
        """
        print(f"\n{self.color_codes['bold']}OSINT Tool - Help{self.color_codes['reset']}")
        print(f"{self.color_codes['green']}{'='*60}{self.color_codes['reset']}\n")
        
        print("Supported input formats:")
        print("  - Phone: +7 (XXX) XXX-XX-XX, 7XXXXXXXXXX")
        print("  - Email: user@example.com")
        print("  - Name: John Doe, Ivan Ivanov")
        print("  - Car: А123БВ77, ABC1234")
        print("  - Passport: XXXXXXXXXX (10 digits)")
        print("  - IP: XXX.XXX.XXX.XXX")
        print("  - VIN: XXXXXXXXXXXXXXXXX (17 chars)")
        print()
        print("Commands:")
        print("  - exit/quit/q: Exit program")
        print("  - help: Show this help")
        print()
        print(f"{self.color_codes['green']}{'='*60}{self.color_codes['reset']}\n")
