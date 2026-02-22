import logging
from tenacity import retry, stop_after_attempt, wait_exponential

class RobustScraper:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    @retry(stop=stop_after_attempt(3), 
           wait=wait_exponential(multiplier=1, min=4, max=10))
    def fetch_with_retry(self, url):
        """Fetch with automatic retry on failure"""
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response
    
    def safe_extract(self, soup, selector, attribute=None):
        """Safely extract data with error handling"""
        try:
            element = soup.select_one(selector)
            if element:
                if attribute:
                    return element.get(attribute)
                return element.text.strip()
            return None
        except Exception as e:
            self.logger.warning(f"Failed to extract {selector}: {e}")
            return None
    
    def scrape_with_fallbacks(self, url):
        """Try multiple selectors for the same data"""
        response = self.fetch_with_retry(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try different selectors for price
        price = (self.safe_extract(soup, '.price') or
                 self.safe_extract(soup, '[itemprop="price"]') or
                 self.safe_extract(soup, '.product-price') or
                 self.safe_extract(soup, '.sale-price'))
        
        return {'price': price}