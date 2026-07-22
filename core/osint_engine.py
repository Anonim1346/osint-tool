#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Core OSINT Engine - Main search and analysis engine
"""

import re
from typing import Dict, List, Any
from core.logger import setup_logger
from core.data_sources import (
    PhoneSearcher,
    NameSearcher,
    CarSearcher,
    PassportSearcher,
    EmailSearcher,
    IPSearcher,
    SocialMediaSearcher
)

logger = setup_logger()

class OSINTEngine:
    """
    Main OSINT search engine that coordinates all data sources
    """
    
    def __init__(self):
        self.phone_searcher = PhoneSearcher()
        self.name_searcher = NameSearcher()
        self.car_searcher = CarSearcher()
        self.passport_searcher = PassportSearcher()
        self.email_searcher = EmailSearcher()
        self.ip_searcher = IPSearcher()
        self.social_media_searcher = SocialMediaSearcher()
        
        logger.info("OSINT Engine initialized")
    
    def identify_query_type(self, query: str) -> tuple:
        """
        Identify the type of query and extract relevant data
        
        Returns: (query_type, cleaned_query)
        """
        query = query.strip()
        
        # Phone number patterns
        if re.match(r'^[+\d\s\-()]{10,}$', query):
            cleaned = re.sub(r'[\s\-()]', '', query)
            if cleaned.startswith('+'):
                return ('phone', cleaned)
            elif len(cleaned) >= 10:
                return ('phone', cleaned)
        
        # Email pattern
        if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', query):
            return ('email', query.lower())
        
        # IP address pattern
        if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', query):
            return ('ip', query)
        
        # Passport number (Russian: 10 digits)
        if re.match(r'^\d{10}$', query):
            return ('passport', query)
        
        # Car number pattern (Russian: XXX123XX or similar)
        if re.match(r'^[А-ЯA-Z]{1,3}\d{3}[А-ЯA-Z]{2}\d{2,3}$|^[А-ЯA-Z]{2}\d{5,6}$', query):
            return ('car', query.upper())
        
        # VIN number (17 characters)
        if re.match(r'^[A-HJ-NPR-Z0-9]{17}$', query):
            return ('vin', query.upper())
        
        # Default: treat as name
        return ('name', query)
    
    def search(self, query: str) -> Dict[str, Any]:
        """
        Main search method - analyze query and search all sources
        """
        query_type, cleaned_query = self.identify_query_type(query)
        
        results = {
            'query': query,
            'query_type': query_type,
            'cleaned_query': cleaned_query,
            'results': {},
            'errors': []
        }
        
        logger.info(f"Searching for: {query} (Type: {query_type})")
        
        try:
            if query_type == 'phone':
                results['results'].update(self._search_phone(cleaned_query))
            
            elif query_type == 'email':
                results['results'].update(self._search_email(cleaned_query))
            
            elif query_type == 'name':
                results['results'].update(self._search_name(cleaned_query))
            
            elif query_type == 'car':
                results['results'].update(self._search_car(cleaned_query))
            
            elif query_type == 'passport':
                results['results'].update(self._search_passport(cleaned_query))
            
            elif query_type == 'ip':
                results['results'].update(self._search_ip(cleaned_query))
            
            elif query_type == 'vin':
                results['results'].update(self._search_vin(cleaned_query))
        
        except Exception as e:
            logger.error(f"Search error: {str(e)}")
            results['errors'].append(str(e))
        
        return results
    
    def _search_phone(self, phone: str) -> Dict:
        """
        Search by phone number - multiple sources
        """
        results = {}
        
        try:
            # Search in phone databases
            phone_info = self.phone_searcher.search(phone)
            results['phone_info'] = phone_info
            
            # If we found a name, search by name too
            if phone_info and phone_info.get('name'):
                results['name_by_phone'] = self.name_searcher.search(phone_info['name'])
            
            # Search in social media
            results['social_media'] = self.social_media_searcher.search(phone)
            
        except Exception as e:
            logger.error(f"Phone search error: {str(e)}")
        
        return results
    
    def _search_name(self, name: str) -> Dict:
        """
        Search by full name or person name
        """
        results = {}
        
        try:
            # Search by name in databases
            results['person_info'] = self.name_searcher.search(name)
            
            # Search in social media
            results['social_media'] = self.social_media_searcher.search(name)
            
        except Exception as e:
            logger.error(f"Name search error: {str(e)}")
        
        return results
    
    def _search_email(self, email: str) -> Dict:
        """
        Search by email address
        """
        results = {}
        
        try:
            results['email_info'] = self.email_searcher.search(email)
            results['social_media'] = self.social_media_searcher.search(email)
            
        except Exception as e:
            logger.error(f"Email search error: {str(e)}")
        
        return results
    
    def _search_car(self, car_number: str) -> Dict:
        """
        Search by car registration number
        """
        results = {}
        
        try:
            results['car_info'] = self.car_searcher.search(car_number)
            
        except Exception as e:
            logger.error(f"Car search error: {str(e)}")
        
        return results
    
    def _search_passport(self, passport: str) -> Dict:
        """
        Search by passport number
        """
        results = {}
        
        try:
            results['passport_info'] = self.passport_searcher.search(passport)
            
        except Exception as e:
            logger.error(f"Passport search error: {str(e)}")
        
        return results
    
    def _search_ip(self, ip: str) -> Dict:
        """
        Search by IP address
        """
        results = {}
        
        try:
            results['ip_info'] = self.ip_searcher.search(ip)
            
        except Exception as e:
            logger.error(f"IP search error: {str(e)}")
        
        return results
    
    def _search_vin(self, vin: str) -> Dict:
        """
        Search by VIN number
        """
        results = {}
        
        try:
            results['vin_info'] = self.car_searcher.search_vin(vin)
            
        except Exception as e:
            logger.error(f"VIN search error: {str(e)}")
        
        return results
