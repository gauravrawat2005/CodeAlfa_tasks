import re
from urllib.parse import urlparse

class DataValidator:
    @staticmethod
    def validate_email(email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_price(price_str):
        """Validate and clean price data"""
        # Remove currency symbols and convert to float
        cleaned = re.sub(r'[^\d.]', '', price_str)
        try:
            return float(cleaned)
        except ValueError:
            return None
    
    @staticmethod
    def validate_url(url):
        """Check if URL is valid"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    @staticmethod
    def check_data_consistency(data_list):
        """Check if all records have expected fields"""
        if not data_list:
            return True
        
        expected_fields = set(data_list[0].keys())
        for item in data_list[1:]:
            if set(item.keys()) != expected_fields:
                return False
        return True