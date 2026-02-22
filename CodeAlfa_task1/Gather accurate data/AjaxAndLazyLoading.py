import requests
import json

def scrape_ajax_content():
    """Many modern sites load data via AJAX - find the API endpoint"""
    
    # Look in Network tab of Developer Tools for XHR requests
    api_url = "https://example.com/api/products"
    
    # Common patterns for AJAX requests
    params = {
        'page': 1,
        'limit': 50,
        'sort': 'latest'
    }
    
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'Accept': 'application/json'
    }
    
    response = requests.get(api_url, params=params, headers=headers)
    
    if response.headers.get('content-type') == 'application/json':
        return response.json()
    else:
        # Fallback to HTML parsing
        return None