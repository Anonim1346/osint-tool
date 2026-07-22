#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Logger Module
"""

import logging
import os
from datetime import datetime

def setup_logger():
    """
    Setup and return logger
    """
    # Create logs directory if not exists
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    logger = logging.getLogger('osint_tool')
    logger.setLevel(logging.DEBUG)
    
    # File handler
    log_filename = f'logs/osint_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.DEBUG)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger
