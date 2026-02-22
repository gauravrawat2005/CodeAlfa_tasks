import requests
from bs4 import BeautifulSoup
import time

class PaginationScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def scrape_all_pages(self):
        page = 1
        all_data = []
        
        while True:
            # Construct page URL
            url = f"{self.base_url}?page={page}"
            print(f"Scraping page {page}...")
            
            # Fetch page
            response = self.session.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract data from current page
            page_data = self.extract_page_data(soup)
            
            if not page_data:  # No more data
                break
                
            all_data.extend(page_data)
            
            # Check for next page
            next_button = soup.select_one('.pagination .next:not(.disabled)')
            if not next_button:
                # Alternative: check if current page has less than expected items
                break
            
            # Polite delay between requests
            time.sleep(2)
            page += 1
        
        return all_data
    
    def extract_page_data(self, soup):
        """Extract product data from a single page"""
        products = []
        for product in soup.select('.product-item'):
            data = {
                'title': product.select_one('.title').text.strip(),
                'price': product.select_one('.price').text.strip(),
                'link': product.select_one('a')['href']
            }
            products.append(data)
        return products