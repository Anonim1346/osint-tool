#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cache Module - Caching search results
"""

import json
import os
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from core.logger import setup_logger

logger = setup_logger()

class Cache:
    """
    Simple file-based cache for search results
    """
    
    def __init__(self, cache_dir='data/cache', ttl_hours=24):
        self.cache_dir = cache_dir
        self.ttl = timedelta(hours=ttl_hours)
        self._ensure_dir()
    
    def _ensure_dir(self):
        """Ensure cache directory exists"""
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def _get_cache_file(self, key: str) -> str:
        """Get cache file path"""
        return os.path.join(self.cache_dir, f"{hash(key) % 100000}.json")
    
    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """Get cached value"""
        try:
            cache_file = self._get_cache_file(key)
            if not os.path.exists(cache_file):
                return None
            
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            
            # Check TTL
            created_at = datetime.fromisoformat(cache_data.get('created_at', ''))
            if datetime.now() - created_at > self.ttl:
                os.remove(cache_file)
                return None
            
            if cache_data.get('key') == key:
                return cache_data.get('value')
        except Exception as e:
            logger.error(f"Cache get error: {str(e)}")
        
        return None
    
    def set(self, key: str, value: Dict[str, Any]):
        """Set cached value"""
        try:
            cache_file = self._get_cache_file(key)
            cache_data = {
                'key': key,
                'value': value,
                'created_at': datetime.now().isoformat()
            }
            
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Cache set error: {str(e)}")
    
    def delete(self, key: str):
        """Delete cached value"""
        try:
            cache_file = self._get_cache_file(key)
            if os.path.exists(cache_file):
                os.remove(cache_file)
        except Exception as e:
            logger.error(f"Cache delete error: {str(e)}")
    
    def clear(self):
        """Clear all cache"""
        try:
            for file in os.listdir(self.cache_dir):
                os.remove(os.path.join(self.cache_dir, file))
        except Exception as e:
            logger.error(f"Cache clear error: {str(e)}")
