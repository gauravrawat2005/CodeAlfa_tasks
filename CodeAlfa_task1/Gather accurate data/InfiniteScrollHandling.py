from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scrape_infinite_scroll(url):
    """Handle websites with infinite scroll"""
    driver = webdriver.Chrome()
    driver.get(url)
    
    # Scroll to load more content
    scroll_pause_time = 2
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Wait to load page
        time.sleep(scroll_pause_time)
        
        # Calculate new scroll height and compare with last height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    
    # Now extract all data
    products = driver.find_elements(By.CLASS_NAME, 'product-item')
    data = []
    for product in products:
        data.append({
            'title': product.find_element(By.CLASS_NAME, 'title').text,
            'price': product.find_element(By.CLASS_NAME, 'price').text
        })
    
    driver.quit()
    return data