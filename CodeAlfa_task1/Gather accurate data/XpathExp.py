from lxml import html
import requests

response = requests.get('https://example.com')
tree = html.fromstring(response.content)

# XPath examples
xpath_queries = {
    # Absolute path
    "absolute": "/html/body/div[1]/div[2]/span",
    
    # Relative path (more common)
    "relative": "//div[@class='product']//span[@class='price']",
    
    # By text content
    "by_text": "//h2[contains(text(), 'Laptop')]",
    
    # Multiple conditions
    "multiple": "//div[@class='product' and @data-available='true']",
    
    # Position
    "position": "(//div[@class='product'])[1]",
    
    # Get attribute values
    "attribute": "//img/@src",
    
    # Get text
    "text": "//div[@class='price']/text()"
}

# Usage example
prices = tree.xpath('//span[@class="price"]/text()')
links = tree.xpath('//a[starts-with(@href, "/product")]/@href')