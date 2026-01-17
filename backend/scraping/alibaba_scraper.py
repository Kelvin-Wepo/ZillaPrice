"""
Alibaba scraper implementation.
"""
import logging
from typing import List, Dict
from urllib.parse import quote_plus
from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)


class AlibabaScraper(BaseScraper):
    """Scraper for Alibaba e-commerce platform."""
    
    def __init__(self):
        super().__init__('alibaba')
        self.base_url = 'https://www.alibaba.com'
    
    def get_search_url(self, query: str) -> str:
        """Generate Alibaba search URL."""
        encoded_query = quote_plus(query)
        return f"{self.base_url}/trade/search?SearchText={encoded_query}"
    
    def search(self, query: str, max_results: int = 20) -> List[Dict]:
        """Search for products on Alibaba."""
        search_url = self.get_search_url(query)
        logger.info(f"Scraping Alibaba: {search_url}")
        
        results = []
        driver = None
        
        try:
            # Alibaba uses JavaScript rendering, so we need Selenium
            driver = self.get_selenium_driver()
            driver.get(search_url)
            
            # Wait for products to load
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.common.by import By
            
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "organic-list-offer"))
            )
            
            # Get page source and parse with BeautifulSoup
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(driver.page_source, 'lxml')
            
            products = soup.find_all('div', class_='organic-list-offer', limit=max_results)
            
            for product in products:
                try:
                    raw_data = self._extract_product_data(product)
                    if raw_data:
                        results.append(self.standardize_result(raw_data))
                except Exception as e:
                    logger.error(f"Error extracting Alibaba product: {str(e)}")
                    continue
            
            logger.info(f"Found {len(results)} products on Alibaba")
            
        except Exception as e:
            logger.error(f"Error scraping Alibaba: {str(e)}")
        finally:
            if driver:
                driver.quit()
        
        return results
    
    def _extract_product_data(self, product_elem) -> Dict:
        """Extract product data from product element."""
        try:
            # Extract title and URL
            title_elem = product_elem.find('h2', class_='search-card-e-title')
            link_elem = product_elem.find('a', class_='organic-list-offer-outter')
            
            if not title_elem or not link_elem:
                return None
            
            title = title_elem.get_text(strip=True)
            url = link_elem.get('href', '')
            if not url.startswith('http'):
                url = self.base_url + url
            
            # Extract price
            price_elem = product_elem.find('span', class_='search-card-e-price-main')
            price = price_elem.get_text(strip=True) if price_elem else '0'
            
            # Extract image
            img_elem = product_elem.find('img', class_='search-card-e-pic__img')
            image_url = img_elem.get('src', '') or img_elem.get('data-src', '') if img_elem else ''
            
            # Extract supplier
            supplier_elem = product_elem.find('a', class_='search-card-e-company')
            supplier = supplier_elem.get_text(strip=True) if supplier_elem else None
            
            # Extract MOQ (Minimum Order Quantity)
            moq_elem = product_elem.find('span', class_='search-card-e-moq')
            moq = moq_elem.get_text(strip=True) if moq_elem else None
            
            return {
                'title': title,
                'url': url,
                'price': price,
                'currency': 'USD',
                'image_url': image_url,
                'seller_name': supplier,
                'availability': True,
            }
            
        except Exception as e:
            logger.error(f"Error extracting Alibaba product data: {str(e)}")
            return None
