#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Data Validators Module - Validate and normalize input data
"""

import re
from typing import Tuple, Optional

class DataValidator:
    """
    Validate and normalize various data formats
    """
    
    @staticmethod
    def validate_phone(phone: str) -> Tuple[bool, str]:
        """
        Validate and normalize phone number
        """
        # Remove spaces, dashes, parentheses
        cleaned = re.sub(r'[\s\-().]', '', phone)
        
        # Check if it's a valid phone
        if not re.match(r'^\+?\d{10,15}$', cleaned):
            return False, ""
        
        # Normalize to international format
        if not cleaned.startswith('+'):
            if cleaned.startswith('8'):
                cleaned = '+7' + cleaned[1:]
            elif cleaned.startswith('7'):
                cleaned = '+' + cleaned
            else:
                cleaned = '+' + cleaned
        
        return True, cleaned
    
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str]:
        """
        Validate email address
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(pattern, email):
            return True, email.lower()
        return False, ""
    
    @staticmethod
    def validate_name(name: str) -> Tuple[bool, str]:
        """
        Validate person name
        """
        # Name should be at least 2 characters and contain letters
        if len(name.strip()) >= 2 and re.search(r'[а-яА-ЯёЁa-zA-Z]', name):
            return True, name.strip()
        return False, ""
    
    @staticmethod
    def validate_car_number(car_number: str) -> Tuple[bool, str]:
        """
        Validate car registration number
        """
        cleaned = car_number.upper().strip()
        
        # Russian format: А123БВ77
        russian_pattern = r'^[А-ЯЁ]{1,3}\d{3}[А-ЯЁ]{2}\d{2,3}$'
        # International format: ABC1234
        international_pattern = r'^[A-Z]{2,3}\d{4,6}$'
        
        if re.match(russian_pattern, cleaned) or re.match(international_pattern, cleaned):
            return True, cleaned
        
        return False, ""
    
    @staticmethod
    def validate_passport(passport: str) -> Tuple[bool, str]:
        """
        Validate passport number
        """
        cleaned = re.sub(r'\D', '', passport)
        
        # Russian passport: 10 digits
        if len(cleaned) == 10 and cleaned.isdigit():
            return True, cleaned
        
        # International passport (up to 20 chars)
        if 5 <= len(passport) <= 20 and re.match(r'^[A-Z0-9]+$', passport.upper()):
            return True, passport.upper()
        
        return False, ""
    
    @staticmethod
    def validate_ip(ip: str) -> Tuple[bool, str]:
        """
        Validate IP address (IPv4 or IPv6)
        """
        ip = ip.strip()
        
        # IPv4
        ipv4_pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
        if re.match(ipv4_pattern, ip):
            parts = [int(x) for x in ip.split('.')]
            if all(0 <= x <= 255 for x in parts):
                return True, ip
        
        # IPv6
        ipv6_pattern = r'^([0-9a-fA-F]{0,4}:){2,7}[0-9a-fA-F]{0,4}$'
        if re.match(ipv6_pattern, ip):
            return True, ip
        
        return False, ""
    
    @staticmethod
    def validate_vin(vin: str) -> Tuple[bool, str]:
        """
        Validate VIN number
        """
        cleaned = vin.upper().strip()
        
        # VIN should be 17 characters
        if len(cleaned) == 17 and re.match(r'^[A-HJ-NPR-Z0-9]{17}$', cleaned):
            return True, cleaned
        
        return False, ""
    
    @staticmethod
    def validate_url(url: str) -> Tuple[bool, str]:
        """
        Validate URL
        """
        pattern = r'^https?://[\w.-]+\.\w+'
        if re.match(pattern, url):
            return True, url
        return False, ""
