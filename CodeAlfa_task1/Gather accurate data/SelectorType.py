from bs4 import BeautifulSoup

html_content = """
<div class="product-card" id="prod-123">
    <h3 class="title">Smartphone X</h3>
    <span class="price" data-currency="USD">$599</span>
    <div class="specs">
        <ul>
            <li class="ram">8GB RAM</li>
            <li class="storage">128GB</li>
        </ul>
    </div>
</div>
"""

soup = BeautifulSoup(html_content, 'html.parser')

# Different selector approaches
# 1. By element type
titles = soup.find_all('h3')

# 2. By class name
prices = soup.find_all(class_='price')
products = soup.select('.product-card')

# 3. By ID
specific_product = soup.select_one('#prod-123')

# 4. By attribute
usd_prices = soup.select('[data-currency="USD"]')

# 5. Nested selectors
ram = soup.select('.product-card .specs .ram')

# 6. Direct child
direct_children = soup.select('.product-card > h3')