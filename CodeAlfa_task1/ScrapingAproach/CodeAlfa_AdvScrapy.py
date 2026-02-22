# Create a Scrapy spider (save as scraper.py)
import scrapy
from scrapy.crawler import CrawlerProcess

class ProductSpider(scrapy.Spider):
    name = 'products'
    start_urls = ['https://example.com/products']
    
    def parse(self, response):
        # Extract product information
        for product in response.css('div.product-item'):
            yield {
                'name': product.css('h3::text').get(),
                'price': product.css('span.price::text').get(),
                'rating': product.css('div.rating::text').get(),
                'url': product.css('a::attr(href)').get()
            }
        
        # Follow pagination
        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

# Run the spider
process = CrawlerProcess(settings={
    'FEEDS': {'output.json': {'format': 'json'}}
})
process.crawl(ProductSpider)
process.start()