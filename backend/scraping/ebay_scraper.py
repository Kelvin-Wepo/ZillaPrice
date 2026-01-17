"""
eBay scraper implementation.
"""
import logging
from typing import List, Dict
from urllib.parse import quote_plus
from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)


class EbayScraper(BaseScraper):
    """Scraper for eBay e-commerce platform."""
    
    def __init__(self):
        super().__init__('ebay')
        self.base_url = 'https://www.ebay.com'
    
    def get_search_url(self, query: str) -> str:
        """Generate eBay search URL."""
        encoded_query = quote_plus(query)
        return f"{self.base_url}/sch/i.html?_nkw={encoded_query}"
    
    def search(self, query: str, max_results: int = 20) -> List[Dict]:
        """Search for products on eBay."""
        search_url = self.get_search_url(query)
        logger.info(f"Scraping eBay: {search_url}")
        
        soup = self.make_request(search_url)
        if not soup:
            return []
        
        results = []
        
        try:
            # Find product cards
            products = soup.find_all('div', class_='s-item__wrapper', limit=max_results)
            
            for product in products:
                try:
                    raw_data = self._extract_product_data(product)
                    if raw_data:
                        results.append(self.standardize_result(raw_data))
                except Exception as e:
                    logger.error(f"Error extracting eBay product: {str(e)}")
                    continue
                
                self.rate_limit(0.5)
            
            logger.info(f"Found {len(results)} products on eBay")
            
        except Exception as e:
            logger.error(f"Error scraping eBay: {str(e)}")
        
        return results
    
    def _extract_product_data(self, product_elem) -> Dict:
        """Extract product data from product element."""
        try:
            # Extract title and URL
            title_elem = product_elem.find('div', class_='s-item__title')
            link_elem = product_elem.find('a', class_='s-item__link')
            
            if not title_elem or not link_elem:
                return None
            
            title = title_elem.get_text(strip=True)
            url = link_elem.get('href', '')
            
            # Extract price
            price_elem = product_elem.find('span', class_='s-item__price')
            price = price_elem.get_text(strip=True) if price_elem else '0'
            
            # Extract image
            img_elem = product_elem.find('img', class_='s-item__image-img')
            image_url = img_elem.get('src', '') if img_elem else ''
            
            # Extract shipping
            shipping_elem = product_elem.find('span', class_='s-item__shipping')
            shipping = shipping_elem.get_text(strip=True) if shipping_elem else None
            
            # Extract seller
            seller_elem = product_elem.find('span', class_='s-item__seller-info-text')
            seller = seller_elem.get_text(strip=True) if seller_elem else None
            
            # Check availability
            availability_elem = product_elem.find('span', class_='s-item__etrs-text')
            availability = not (availability_elem and 'sold' in availability_elem.get_text().lower())
            
            return {
                'title': title,
                'url': url,
                'price': price,
                'currency': 'USD',
                'image_url': image_url,
                'shipping_cost': shipping,
                'seller_name': seller,
                'availability': availability,
            }
            
        except Exception as e:
            logger.error(f"Error extracting eBay product data: {str(e)}")
            return None
