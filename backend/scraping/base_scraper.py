"""
Base scraper class for all platform scrapers.
"""
import logging
import time
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.conf import settings

logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    """Abstract base class for platform scrapers."""
    
    def __init__(self, platform_name: str):
        self.platform_name = platform_name
        self.timeout = settings.SCRAPING_TIMEOUT
        self.headers = {
            'User-Agent': settings.USER_AGENT,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
    
    def get_selenium_driver(self):
        """Initialize Selenium WebDriver with Chrome."""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument(f'user-agent={settings.USER_AGENT}')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(self.timeout)
        return driver
    
    def make_request(self, url: str) -> Optional[BeautifulSoup]:
        """Make HTTP request and return BeautifulSoup object."""
        try:
            response = requests.get(
                url,
                headers=self.headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            return BeautifulSoup(response.content, 'lxml')
        except requests.RequestException as e:
            logger.error(f"Request failed for {url}: {str(e)}")
            return None
    
    @abstractmethod
    def search(self, query: str, max_results: int = 20) -> List[Dict]:
        """
        Search for products on the platform.
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            
        Returns:
            List of product dictionaries with standardized fields
        """
        pass
    
    @abstractmethod
    def get_search_url(self, query: str) -> str:
        """Generate search URL for the platform."""
        pass
    
    def standardize_result(self, raw_data: Dict) -> Dict:
        """
        Standardize scraped data to common format.
        
        Expected output format:
        {
            'title': str,
            'url': str,
            'price': float,
            'currency': str,
            'image_url': str,
            'rating': float (optional),
            'review_count': int (optional),
            'availability': bool,
            'seller_name': str (optional),
            'shipping_cost': float (optional),
        }
        """
        return {
            'title': raw_data.get('title', ''),
            'url': raw_data.get('url', ''),
            'price': self.parse_price(raw_data.get('price', '0')),
            'currency': raw_data.get('currency', 'USD'),
            'image_url': raw_data.get('image_url', ''),
            'rating': self.parse_rating(raw_data.get('rating')),
            'review_count': self.parse_int(raw_data.get('review_count')),
            'availability': raw_data.get('availability', True),
            'seller_name': raw_data.get('seller_name', ''),
            'shipping_cost': self.parse_price(raw_data.get('shipping_cost', '0')),
        }
    
    @staticmethod
    def parse_price(price_str: str) -> float:
        """Extract numeric price from string."""
        if not price_str:
            return 0.0
        
        # Remove currency symbols and extra characters
        import re
        cleaned = re.sub(r'[^\d.,]', '', str(price_str))
        cleaned = cleaned.replace(',', '')
        
        try:
            return float(cleaned)
        except (ValueError, AttributeError):
            return 0.0
    
    @staticmethod
    def parse_rating(rating_str) -> Optional[float]:
        """Extract numeric rating from string."""
        if not rating_str:
            return None
        
        import re
        match = re.search(r'(\d+\.?\d*)', str(rating_str))
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                return None
        return None
    
    @staticmethod
    def parse_int(value) -> Optional[int]:
        """Extract integer from value."""
        if not value:
            return None
        
        import re
        cleaned = re.sub(r'[^\d]', '', str(value))
        
        try:
            return int(cleaned)
        except (ValueError, AttributeError):
            return None
    
    def rate_limit(self, delay: float = 1.0):
        """Add delay between requests to avoid rate limiting."""
        time.sleep(delay)
