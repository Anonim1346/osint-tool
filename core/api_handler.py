#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API Handler Module - Manage multiple API integrations
"""

import os
import json
from typing import Dict, Any, Optional
from requests import Session, Response
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from core.logger import setup_logger
from core.config import Config

logger = setup_logger()
config = Config()

class APIHandler:
    """
    Central handler for all API integrations
    """
    
    def __init__(self):
        self.config = config
        self.session = self._create_session()
        self.api_keys = self._load_api_keys()
        self.endpoints = self._load_endpoints()
    
    def _create_session(self) -> Session:
        """
        Create requests session with retry strategy
        """
        session = Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "OPTIONS"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session
    
    def _load_api_keys(self) -> Dict[str, str]:
        """
        Load API keys from config or environment
        """
        keys = {}
        api_config = self.config.get('api_keys', {})
        
        for key, value in api_config.items():
            env_key = f"OSINT_{key.upper()}"
            keys[key] = os.getenv(env_key, value)
        
        return keys
    
    def _load_endpoints(self) -> Dict[str, str]:
        """
        Load API endpoints
        """
        return {
            'hlr': 'https://api.example.com/hlr',
            'ip_lookup': 'https://api.example.com/ip',
            'breach_check': 'https://haveibeenpwned.com/api/v3',
            'vk': 'https://api.vk.com/method',
            'telegram': 'https://api.telegram.org/bot',
            'instagram': 'https://www.instagram.com/api/v1',
            'facebook': 'https://graph.facebook.com',
            'twitter': 'https://api.twitter.com/2',
            'linkedin': 'https://api.linkedin.com/v2',
            'whois': 'https://www.whoisxmlapi.com/api'
        }
    
    def request(self, method: str, url: str, **kwargs) -> Optional[Response]:
        """
        Make HTTP request with error handling
        """
        try:
            timeout = kwargs.pop('timeout', self.config.get('timeout', 10))
            response = self.session.request(method, url, timeout=timeout, **kwargs)
            response.raise_for_status()
            return response
        except Exception as e:
            logger.error(f"API request error: {str(e)}")
            return None
    
    def get(self, url: str, **kwargs) -> Optional[Response]:
        """GET request"""
        return self.request('GET', url, **kwargs)
    
    def post(self, url: str, **kwargs) -> Optional[Response]:
        """POST request"""
        return self.request('POST', url, **kwargs)
    
    def put(self, url: str, **kwargs) -> Optional[Response]:
        """PUT request"""
        return self.request('PUT', url, **kwargs)
    
    def delete(self, url: str, **kwargs) -> Optional[Response]:
        """DELETE request"""
        return self.request('DELETE', url, **kwargs)
    
    # HLR Lookup
    def hlr_lookup(self, phone: str) -> Optional[Dict[str, Any]]:
        """
        Perform HLR lookup for phone number
        """
        try:
            if not self.config.get('apis', {}).get('enable_hlr', False):
                logger.warning("HLR lookup is disabled")
                return None
            
            url = f"{self.endpoints['hlr']}?phone={phone}"
            headers = {'Authorization': f"Bearer {self.api_keys.get('hlr_api_key')}"}
            
            response = self.get(url, headers=headers)
            if response:
                return response.json()
        except Exception as e:
            logger.error(f"HLR lookup error: {str(e)}")
        
        return None
    
    # IP Geolocation
    def ip_geolocation(self, ip: str) -> Optional[Dict[str, Any]]:
        """
        Get IP geolocation information
        """
        try:
            if not self.config.get('apis', {}).get('enable_ip_lookup', False):
                return None
            
            url = f"{self.endpoints['ip_lookup']}?ip={ip}"
            headers = {'Authorization': f"Bearer {self.api_keys.get('ip_lookup_key')}"}
            
            response = self.get(url, headers=headers)
            if response:
                return response.json()
        except Exception as e:
            logger.error(f"IP geolocation error: {str(e)}")
        
        return None
    
    # Data Breach Check
    def check_breach(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Check if email found in data breaches (HaveIBeenPwned)
        """
        try:
            if not self.config.get('apis', {}).get('enable_breach_check', False):
                return None
            
            url = f"{self.endpoints['breach_check']}/breachedaccount?account={email}"
            headers = {'User-Agent': 'OSINT-Tool', 'hibp-api-key': self.api_keys.get('breach_check_key', '')}
            
            response = self.get(url, headers=headers)
            if response:
                return {'breaches': response.json()}
            return {'breaches': []}
        except Exception as e:
            logger.error(f"Breach check error: {str(e)}")
        
        return None
    
    # VK Search
    def vk_search(self, query: str, search_type: str = 'people') -> Optional[Dict[str, Any]]:
        """
        Search in VKontakte
        """
        try:
            if not self.config.get('apis', {}).get('enable_vk', False):
                return None
            
            token = self.api_keys.get('vk_token')
            url = f"{self.endpoints['vk']}/{search_type}.search"
            params = {'access_token': token, 'v': '5.131', 'q': query}
            
            response = self.get(url, params=params)
            if response:
                return response.json()
        except Exception as e:
            logger.error(f"VK search error: {str(e)}")
        
        return None
    
    # Telegram Search
    def telegram_search(self, query: str) -> Optional[Dict[str, Any]]:
        """
        Search in Telegram
        """
        try:
            if not self.config.get('apis', {}).get('enable_telegram', False):
                return None
            
            token = self.api_keys.get('telegram_token')
            url = f"{self.endpoints['telegram']}{token}/searchPublicChats"
            params = {'query': query}
            
            response = self.post(url, json=params)
            if response:
                return response.json()
        except Exception as e:
            logger.error(f"Telegram search error: {str(e)}")
        
        return None
    
    # Instagram Search
    def instagram_search(self, username: str) -> Optional[Dict[str, Any]]:
        """
        Search in Instagram
        """
        try:
            if not self.config.get('apis', {}).get('enable_instagram', False):
                return None
            
            # Instagram API requires special handling
            logger.warning("Instagram search requires session handling")
            return None
        except Exception as e:
            logger.error(f"Instagram search error: {str(e)}")
        
        return None
    
    # Facebook Search
    def facebook_search(self, query: str) -> Optional[Dict[str, Any]]:
        """
        Search in Facebook
        """
        try:
            if not self.config.get('apis', {}).get('enable_facebook', False):
                return None
            
            token = self.api_keys.get('facebook_token')
            url = f"{self.endpoints['facebook']}/search"
            params = {'access_token': token, 'q': query, 'type': 'user'}
            
            response = self.get(url, params=params)
            if response:
                return response.json()
        except Exception as e:
            logger.error(f"Facebook search error: {str(e)}")
        
        return None
    
    # Twitter Search
    def twitter_search(self, query: str) -> Optional[Dict[str, Any]]:
        """
        Search in Twitter
        """
        try:
            if not self.config.get('apis', {}).get('enable_twitter', False):
                return None
            
            token = self.api_keys.get('twitter_token')
            url = f"{self.endpoints['twitter']}/tweets/search/recent"
            headers = {'Authorization': f"Bearer {token}"}
            params = {'query': query}
            
            response = self.get(url, headers=headers, params=params)
            if response:
                return response.json()
        except Exception as e:
            logger.error(f"Twitter search error: {str(e)}")
        
        return None
    
    # LinkedIn Search
    def linkedin_search(self, query: str) -> Optional[Dict[str, Any]]:
        """
        Search in LinkedIn
        """
        try:
            if not self.config.get('apis', {}).get('enable_linkedin', False):
                return None
            
            token = self.api_keys.get('linkedin_token')
            url = f"{self.endpoints['linkedin']}/search"
            headers = {'Authorization': f"Bearer {token}"}
            params = {'keywords': query}
            
            response = self.get(url, headers=headers, params=params)
            if response:
                return response.json()
        except Exception as e:
            logger.error(f"LinkedIn search error: {str(e)}")
        
        return None
    
    # WHOIS Lookup
    def whois_lookup(self, domain: str) -> Optional[Dict[str, Any]]:
        """
        Get WHOIS information for domain
        """
        try:
            token = self.api_keys.get('whois_api_key')
            url = f"{self.endpoints['whois']}/whois"
            params = {'apiKey': token, 'domain': domain}
            
            response = self.get(url, params=params)
            if response:
                return response.json()
        except Exception as e:
            logger.error(f"WHOIS lookup error: {str(e)}")
        
        return None
