from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_js_website(url):
    """Handle JavaScript-heavy websites"""
    
    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run in background
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    driver = Chrome(options=chrome_options)
    
    try:
        driver.get(url)
        
        # Wait for specific element to load
        wait = WebDriverWait(driver, 10)
        element = wait.until(
            EC.presence_of_element_located(("class name", "product-list"))
        )
        
        # Execute JavaScript to get data
        page_height = driver.execute_script("return document.body.scrollHeight")
        
        # Extract after JavaScript execution
        products = driver.find_elements_by_class_name("product")
        
        return [product.text for product in products]
    
    finally:
        driver.quit()