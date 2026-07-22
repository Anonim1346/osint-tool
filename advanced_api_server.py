#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced Flask API Server - Enterprise OSINT Tool v2.0
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from core.advanced_engine import AdvancedOSINTEngine
from core.logger import setup_logger
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

logger = setup_logger()
engine = AdvancedOSINTEngine()

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'service': 'Advanced OSINT Tool v2.0',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/v2/search', methods=['POST'])
def search():
    """
    Advanced search endpoint
    
    Request:
    {
        "query": "search_query"
    }
    """
    try:
        data = request.json
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        # Perform search
        results = engine.search(query)
        
        return jsonify(results)
    
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/v2/sources', methods=['GET'])
def get_sources():
    """
    Get list of all available sources
    """
    try:
        sources = engine.get_all_sources()
        return jsonify({
            'sources': sources,
            'total': len(sources)
        })
    except Exception as e:
        logger.error(f"Sources error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/v2/info', methods=['GET'])
def info():
    """
    Get tool information
    """
    return jsonify({
        'name': 'Advanced OSINT Tool',
        'version': '2.0',
        'edition': 'Enterprise',
        'description': 'Legal Public Sources Intelligence Gathering',
        'sources_count': len(engine.get_all_sources()),
        'legal_notice': 'This tool searches only public and legal sources'
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    print(f"\nStarting Advanced OSINT API Server on port {port}...")
    print(f"API Documentation: http://localhost:{port}/api/v2/info")
    print(f"Available sources: http://localhost:{port}/api/v2/sources")
    print()
    app.run(host='0.0.0.0', port=port, debug=debug)
