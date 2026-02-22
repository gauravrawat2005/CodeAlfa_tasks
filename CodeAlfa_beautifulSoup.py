import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Basic web scraping example
def scrape_basic_info(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract specific elements
        titles = soup.find_all('h2', class_='title')
        prices = soup.find_all('span', class_='price')
        
        data = []
        for title, price in zip(titles, prices):
            data.append({
                'title': title.text.strip(),
                'price': price.text.strip()
            })
        
        return pd.DataFrame(data)
    
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

# Save to CSV
df = scrape_basic_info('https://example.com')
df.to_csv('scraped_data.csv', index=False)