"""
Jumia scraper implementation.
"""
import logging
from typing import List, Dict
from urllib.parse import quote_plus
from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)


class JumiaScraper(BaseScraper):
    """Scraper for Jumia e-commerce platform."""
    
    def __init__(self):
        super().__init__('jumia')
        self.base_url = 'https://www.jumia.com.ng'
    
    def get_search_url(self, query: str) -> str:
        """Generate Jumia search URL."""
        encoded_query = quote_plus(query)
        return f"{self.base_url}/catalog/?q={encoded_query}"
    
    def search(self, query: str, max_results: int = 20) -> List[Dict]:
        """Search for products on Jumia."""
        search_url = self.get_search_url(query)
        logger.info(f"Scraping Jumia: {search_url}")
        
        soup = self.make_request(search_url)
        if not soup:
            return []
        
        results = []
        
        try:
            # Find product cards
            products = soup.find_all('article', class_='prd', limit=max_results)
            
            for product in products:
                try:
                    raw_data = self._extract_product_data(product)
                    if raw_data:
                        results.append(self.standardize_result(raw_data))
                except Exception as e:
                    logger.error(f"Error extracting Jumia product: {str(e)}")
                    continue
                
                self.rate_limit(0.5)
            
            logger.info(f"Found {len(results)} products on Jumia")
            
        except Exception as e:
            logger.error(f"Error scraping Jumia: {str(e)}")
        
        return results
    
    def _extract_product_data(self, product_elem) -> Dict:
        """Extract product data from product element."""
        try:
            # Extract title and URL
            title_elem = product_elem.find('h3', class_='name')
            link_elem = product_elem.find('a', class_='core')
            
            if not title_elem or not link_elem:
                return None
            
            title = title_elem.get_text(strip=True)
            url = self.base_url + link_elem.get('href', '')
            
            # Extract price
            price_elem = product_elem.find('div', class_='prc')
            price = price_elem.get_text(strip=True) if price_elem else '0'
            
            # Extract image
            img_elem = product_elem.find('img', class_='img')
            image_url = img_elem.get('data-src', '') or img_elem.get('src', '') if img_elem else ''
            
            # Extract rating
            rating_elem = product_elem.find('div', class_='stars')
            rating = rating_elem.get_text(strip=True) if rating_elem else None
            
            # Extract review count
            review_elem = product_elem.find('div', class_='rev')
            review_count = review_elem.get_text(strip=True) if review_elem else None
            
            return {
                'title': title,
                'url': url,
                'price': price,
                'currency': 'NGN',
                'image_url': image_url,
                'rating': rating,
                'review_count': review_count,
                'availability': True,
            }
            
        except Exception as e:
            logger.error(f"Error extracting Jumia product data: {str(e)}")
            return None
