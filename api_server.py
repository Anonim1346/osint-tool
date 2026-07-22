#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WEB API Server - Flask REST API for OSINT tool
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from core.osint_engine import OSINTEngine
from core.cache import Cache
from core.database import Database
from utils.formatters import ResultFormatter
from core.logger import setup_logger
import os

app = Flask(__name__)
CORS(app)

logger = setup_logger()
engine = OSINTEngine()
cache = Cache()
db = Database()
formatter = ResultFormatter()

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'service': 'OSINT Tool API'})

@app.route('/api/search', methods=['POST'])
def search():
    """
    Main search endpoint
    
    Request:
    {
        "query": "user_input",
        "format": "json|html|csv|text|markdown" (optional, default: json)
    }
    """
    try:
        data = request.json
        query = data.get('query', '').strip()
        output_format = data.get('format', 'json').lower()
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        # Check cache
        cached = cache.get(query)
        if cached:
            logger.info(f"Cache hit for: {query}")
            results = cached
        else:
            # Perform search
            results = engine.search(query)
            cache.set(query, results)
            db.add_search_result(query, results.get('query_type'), results)
        
        # Format results
        if output_format == 'json':
            return jsonify(results)
        elif output_format == 'html':
            return formatter.to_html(results), 200, {'Content-Type': 'text/html; charset=utf-8'}
        elif output_format == 'csv':
            return formatter.to_csv(results), 200, {'Content-Type': 'text/csv; charset=utf-8'}
        elif output_format == 'text':
            return formatter.to_text(results), 200, {'Content-Type': 'text/plain; charset=utf-8'}
        elif output_format == 'markdown':
            return formatter.to_markdown(results), 200, {'Content-Type': 'text/markdown; charset=utf-8'}
        else:
            return jsonify({'error': 'Invalid format'}), 400
    
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/history', methods=['GET'])
def search_history():
    """
    Get search history
    
    Query parameters:
    - limit: max number of results (default: 50)
    - query_type: filter by type
    """
    try:
        limit = int(request.args.get('limit', 50))
        query_type = request.args.get('query_type', None)
        
        session = db.get_session()
        from core.database import SearchResult
        
        query = session.query(SearchResult).order_by(SearchResult.created_at.desc()).limit(limit)
        
        if query_type:
            query = query.filter(SearchResult.query_type == query_type)
        
        results = [{
            'id': r.id,
            'query': r.query,
            'query_type': r.query_type,
            'created_at': r.created_at.isoformat()
        } for r in query.all()]
        
        session.close()
        return jsonify(results)
    
    except Exception as e:
        logger.error(f"History error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/cache/clear', methods=['POST'])
def clear_cache():
    """
    Clear cache
    """
    try:
        cache.clear()
        return jsonify({'status': 'cache cleared'})
    except Exception as e:
        logger.error(f"Cache clear error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def stats():
    """
    Get statistics
    """
    try:
        session = db.get_session()
        from core.database import SearchResult
        from sqlalchemy import func
        
        total_searches = session.query(func.count(SearchResult.id)).scalar()
        
        query_types = session.query(
            SearchResult.query_type,
            func.count(SearchResult.id)
        ).group_by(SearchResult.query_type).all()
        
        stats = {
            'total_searches': total_searches,
            'by_type': {qt: count for qt, count in query_types}
        }
        
        session.close()
        return jsonify(stats)
    
    except Exception as e:
        logger.error(f"Stats error: {str(e)}")
        return jsonify({'error': str(e)}), 500

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
    app.run(host='0.0.0.0', port=port, debug=debug)
