"""
Complete example scraping an e-commerce site with proper navigation
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import random

class EcommerceScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.results = []
    
    def parse_product(self, product_html):
        """Parse individual product element"""
        product = {}
        
        # Try multiple selectors for robustness
        product['title'] = (
            product_html.select_one('.product-title') or
            product_html.select_one('h2 a') or
            product_html.select_one('.name')
        )
        product['title'] = product['title'].text.strip() if product['title'] else None
        
        # Extract price
        price_elem = (
            product_html.select_one('.price') or
            product_html.select_one('.current-price') or
            product_html.select_one('[itemprop="price"]')
        )
        if price_elem:
            price_text = price_elem.text.strip()
            # Clean price
            product['price'] = float(re.sub(r'[^\d.]', '', price_text))
        
        # Extract link
        link_elem = product_html.select_one('a')
        product['url'] = link_elem.get('href') if link_elem else None
        
        return product
    
    def navigate_category(self, category_url, max_pages=10):
        """Navigate through category pages"""
        page = 1
        
        while page <= max_pages:
            print(f"Scraping page {page}...")
            
            # Construct page URL
            url = f"{category_url}?page={page}"
            response = self.session.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all product elements
            products = soup.select('.product-item, .product, .card')
            
            if not products:
                break
            
            # Parse each product
            for product_html in products:
                product_data = self.parse_product(product_html)
                if product_data and product_data.get('title'):
                    product_data['category'] = category_url.split('/')[-1]
                    product_data['scrape_date'] = datetime.now().isoformat()
                    self.results.append(product_data)
            
            # Check for next page
            next_page = soup.select_one('.pagination .next:not(.disabled)')
            if not next_page:
                break
            
            # Random delay to be polite
            time.sleep(random.uniform(1, 3))
            page += 1
    
    def save_results(self, filename):
        """Save scraped data"""
        df = pd.DataFrame(self.results)
        
        # Save with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"{filename}_{timestamp}.csv"
        
        df.to_csv(output_file, index=False)
        print(f"Saved {len(df)} records to {output_file}")
        
        # Also save summary statistics
        summary = {
            'total_products': len(df),
            'unique_categories': df['category'].nunique() if 'category' in df else 0,
            'avg_price': df['price'].mean() if 'price' in df else 0,
            'date_range': f"{df['scrape_date'].min()} to {df['scrape_date'].max()}"
        }
        
        return df, summary

# Usage
scraper = EcommerceScraper("https://example-store.com")
scraper.navigate_category("/electronics", max_pages=5)
df, summary = scraper.save_results("electronics_products")

print("Summary:", summary)