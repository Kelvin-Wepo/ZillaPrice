"""
Kilimall scraper implementation.
"""
import logging
from typing import List, Dict
from urllib.parse import quote_plus
from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)


class KilimallScraper(BaseScraper):
    """Scraper for Kilimall e-commerce platform."""
    
    def __init__(self):
        super().__init__('kilimall')
        self.base_url = 'https://www.kilimall.co.ke'
    
    def get_search_url(self, query: str) -> str:
        """Generate Kilimall search URL."""
        encoded_query = quote_plus(query)
        return f"{self.base_url}/new/search?keywords={encoded_query}"
    
    def search(self, query: str, max_results: int = 20) -> List[Dict]:
        """Search for products on Kilimall."""
        search_url = self.get_search_url(query)
        logger.info(f"Scraping Kilimall: {search_url}")
        
        results = []
        driver = None
        
        try:
            # Kilimall uses JavaScript rendering, so we need Selenium
            driver = self.get_selenium_driver()
            driver.get(search_url)
            
            # Wait for products to load
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.common.by import By
            
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "goods-item"))
            )
            
            # Get page source and parse with BeautifulSoup
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(driver.page_source, 'lxml')
            
            products = soup.find_all('div', class_='goods-item', limit=max_results)
            
            for product in products:
                try:
                    raw_data = self._extract_product_data(product)
                    if raw_data:
                        results.append(self.standardize_result(raw_data))
                except Exception as e:
                    logger.error(f"Error extracting Kilimall product: {str(e)}")
                    continue
            
            logger.info(f"Found {len(results)} products on Kilimall")
            
        except Exception as e:
            logger.error(f"Error scraping Kilimall: {str(e)}")
        finally:
            if driver:
                driver.quit()
        
        return results
    
    def _extract_product_data(self, product_elem) -> Dict:
        """Extract product data from product element."""
        try:
            # Extract title and URL
            title_elem = product_elem.find('div', class_='goods-name')
            link_elem = product_elem.find('a')
            
            if not title_elem or not link_elem:
                return None
            
            title = title_elem.get_text(strip=True)
            url = self.base_url + link_elem.get('href', '')
            
            # Extract price
            price_elem = product_elem.find('span', class_='goods-price')
            price = price_elem.get_text(strip=True) if price_elem else '0'
            
            # Extract image
            img_elem = product_elem.find('img')
            image_url = img_elem.get('src', '') or img_elem.get('data-src', '') if img_elem else ''
            
            # Extract rating (if available)
            rating_elem = product_elem.find('div', class_='rating')
            rating = rating_elem.get_text(strip=True) if rating_elem else None
            
            return {
                'title': title,
                'url': url,
                'price': price,
                'currency': 'KES',
                'image_url': image_url,
                'rating': rating,
                'availability': True,
            }
            
        except Exception as e:
            logger.error(f"Error extracting Kilimall product data: {str(e)}")
            return None
