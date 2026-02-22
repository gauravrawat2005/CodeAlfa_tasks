from selenium import webdriver
from selenium.webdriver.support.ui import Select

def scrape_with_filters(url):
    driver = webdriver.Chrome()
    driver.get(url)
    
    # Handle dropdown selection
    category_dropdown = Select(driver.find_element(By.ID, 'category'))
    category_dropdown.select_by_visible_text('Electronics')
    
    # Wait for AJAX content to load
    time.sleep(3)
    
    # Apply checkbox filter
    filter_checkbox = driver.find_element(By.ID, 'in-stock-only')
    filter_checkbox.click()
    
    time.sleep(2)
    
    # Extract filtered results
    results = driver.find_elements(By.CLASS_NAME, 'result-item')
    
    driver.quit()