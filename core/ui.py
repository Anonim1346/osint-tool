#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced User Interface for Enterprise OSINT Tool
"""

from typing import Dict, Any
import json
from datetime import datetime

class UserInterface:
    """
    Advanced user interface for OSINT tool
    """
    
    def __init__(self):
        self.color_codes = {
            'green': '\033[92m',
            'red': '\033[91m',
            'yellow': '\033[93m',
            'blue': '\033[94m',
            'purple': '\033[95m',
            'cyan': '\033[96m',
            'white': '\033[97m',
            'reset': '\033[0m',
            'bold': '\033[1m',
            'dim': '\033[2m'
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
    
    def display_advanced_results(self, results: Dict[str, Any]):
        """
        Display search results from advanced engine
        """
        if not results or not results.get('results'):
            print(f"{self.color_codes['yellow']}[!] No results found{self.color_codes['reset']}")
            return
        
        print(f"{self.color_codes['green']}{'='*70}{self.color_codes['reset']}")
        print(f"{self.color_codes['bold']}{self.color_codes['cyan']}OSINT SEARCH RESULTS - ADVANCED{self.color_codes['reset']}")
        print(f"{self.color_codes['green']}{'='*70}{self.color_codes['reset']}\n")
        
        print(f"Query: {results['query']}")
        print(f"Type: {results['query_type']}")
        print(f"Cleaned: {results['cleaned_query']}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        if results.get('sources_searched'):
            print(f"Sources Searched: {', '.join(results['sources_searched'])}")
            print()
        
        # Display results by category
        for category, data in results['results'].items():
            self._display_advanced_category(category, data)
        
        # Display errors if any
        if results.get('error'):
            print(f"\n{self.color_codes['red']}[!] Error: {results['error']}{self.color_codes['reset']}")
        
        print(f"\n{self.color_codes['green']}{'='*70}{self.color_codes['reset']}\n")
    
    def _display_advanced_category(self, category: str, data: Dict[str, Any]):
        """
        Display single category of advanced results
        """
        if isinstance(data, dict):
            # Skip empty results
            if not data or (len(data) == 1 and 'error' in data):
                return
            
            print(f"{self.color_codes['bold']}{self.color_codes['blue']}▶ {category.upper()}{self.color_codes['reset']}")
            
            # Display source if available
            if data.get('source'):
                print(f"  Source: {data['source']}")
            
            # Display main data
            for key, value in data.items():
                if key not in ['source', 'status', 'query', 'error'] and value is not None:
                    if isinstance(value, (dict, list)):
                        try:
                            print(f"  {key}:")
                            print(f"    {json.dumps(value, ensure_ascii=False, indent=6)}")
                        except:
                            print(f"  {key}: {str(value)[:200]}")
                    elif isinstance(value, str) and len(value) > 100:
                        print(f"  {key}: {value[:100]}...")
                    else:
                        print(f"  {key}: {value}")
            
            print()
    
    def display_results(self, results: Dict[str, Any]):
        """
        Display basic search results (backward compatibility)
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
        
        for category, data in results['results'].items():
            self._display_category(category, data)
        
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
            
            for key, value in data.items():
                if key not in ['sources', 'status'] and value is not None:
                    if isinstance(value, (dict, list)):
                        print(f"    {key}: {json.dumps(value, ensure_ascii=False, indent=6)}")
                    else:
                        print(f"    {key}: {value}")
        
        print()
