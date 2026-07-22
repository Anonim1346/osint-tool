#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Formatters Module - Format search results for output
"""

import json
from typing import Dict, Any
from datetime import datetime

class ResultFormatter:
    """
    Format search results for different output formats
    """
    
    @staticmethod
    def to_json(data: Dict[str, Any], pretty: bool = True) -> str:
        """
        Format as JSON
        """
        if pretty:
            return json.dumps(data, ensure_ascii=False, indent=2)
        return json.dumps(data, ensure_ascii=False)
    
    @staticmethod
    def to_html(data: Dict[str, Any]) -> str:
        """
        Format as HTML
        """
        html = "<html><head><meta charset='utf-8'><style>"
        html += "body { font-family: Arial; } .header { background: #333; color: white; padding: 10px; } "
        html += ".result { margin: 10px; padding: 10px; border: 1px solid #ccc; } "
        html += "</style></head><body>"
        
        html += f"<div class='header'><h1>OSINT Search Results</h1></div>"
        html += f"<div class='result'>"
        html += f"<p><strong>Query:</strong> {data.get('query', 'N/A')}</p>"
        html += f"<p><strong>Type:</strong> {data.get('query_type', 'N/A')}</p>"
        html += f"<p><strong>Timestamp:</strong> {datetime.now().isoformat()}</p>"
        
        if data.get('results'):
            html += "<h2>Results:</h2>"
            for category, result in data['results'].items():
                html += f"<h3>{category}</h3>"
                html += f"<pre>{json.dumps(result, ensure_ascii=False, indent=2)}</pre>"
        
        html += "</div></body></html>"
        return html
    
    @staticmethod
    def to_csv(data: Dict[str, Any]) -> str:
        """
        Format as CSV
        """
        csv = "Category,Key,Value\n"
        
        for category, result in data.get('results', {}).items():
            if isinstance(result, dict):
                for key, value in result.items():
                    csv += f'{category},"{key}","{str(value).replace(chr(34), chr(34)+chr(34))}"\n'
        
        return csv
    
    @staticmethod
    def to_text(data: Dict[str, Any]) -> str:
        """
        Format as plain text
        """
        text = "=" * 60 + "\n"
        text += "OSINT SEARCH RESULTS\n"
        text += "=" * 60 + "\n\n"
        
        text += f"Query: {data.get('query', 'N/A')}\n"
        text += f"Type: {data.get('query_type', 'N/A')}\n"
        text += f"Timestamp: {datetime.now().isoformat()}\n\n"
        
        if data.get('results'):
            for category, result in data['results'].items():
                text += f"{'='*40}\n"
                text += f"{category.upper()}\n"
                text += f"{'='*40}\n"
                
                if isinstance(result, dict):
                    for key, value in result.items():
                        if isinstance(value, (dict, list)):
                            text += f"{key}:\n{json.dumps(value, ensure_ascii=False, indent=2)}\n"
                        else:
                            text += f"{key}: {value}\n"
                
                text += "\n"
        
        return text
    
    @staticmethod
    def to_markdown(data: Dict[str, Any]) -> str:
        """
        Format as Markdown
        """
        md = "# OSINT Search Results\n\n"
        md += f"**Query:** {data.get('query', 'N/A')}  \n"
        md += f"**Type:** {data.get('query_type', 'N/A')}  \n"
        md += f"**Timestamp:** {datetime.now().isoformat()}  \n\n"
        
        if data.get('results'):
            for category, result in data['results'].items():
                md += f"## {category}\n\n"
                
                if isinstance(result, dict):
                    md += "| Key | Value |\n"
                    md += "|-----|-------|\n"
                    
                    for key, value in result.items():
                        if isinstance(value, (dict, list)):
                            value_str = json.dumps(value, ensure_ascii=False)
                        else:
                            value_str = str(value)
                        
                        md += f"| {key} | {value_str.replace('|', '\\|')} |\n"
                
                md += "\n"
        
        return md
