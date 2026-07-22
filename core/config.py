#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration Module
"""

import json
import os
from typing import Dict, Any

class Config:
    """
    Configuration manager for OSINT tool
    """
    
    def __init__(self):
        self.config_path = 'config.json'
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """
        Load configuration from file or use defaults
        """
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"[!] Error loading config: {e}")
                return self._get_default_config()
        else:
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """
        Get default configuration
        """
        return {
            'timeout': 10,
            'retries': 3,
            'output_format': 'json',
            'log_level': 'INFO',
            'database': {
                'enabled': True,
                'path': 'data/osint.db'
            },
            'apis': {
                'enable_hlr': False,
                'enable_viber': True,
                'enable_telegram': True
            }
        }
    
    def get(self, key: str, default=None):
        """
        Get config value
        """
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any):
        """
        Set config value
        """
        self.config[key] = value
    
    def save(self):
        """
        Save configuration to file
        """
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"[!] Error saving config: {e}")
