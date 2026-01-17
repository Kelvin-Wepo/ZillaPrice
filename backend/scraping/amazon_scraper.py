"""
Amazon scraper implementation.
"""
import logging
from typing import List, Dict
from urllib.parse import quote_plus
from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)


class AmazonScraper(BaseScraper):
    """Scraper for Amazon e-commerce platform."""
    
    def __init__(self):
        super().__init__('amazon')
        self.base_url = 'https://www.amazon.com'
    
    def get_search_url(self, query: str) -> str:
        """Generate Amazon search URL."""
        encoded_query = quote_plus(query)
        return f"{self.base_url}/s?k={encoded_query}"
    
    def search(self, query: str, max_results: int = 20) -> List[Dict]:
        """Search for products on Amazon."""
        search_url = self.get_search_url(query)
        logger.info(f"Scraping Amazon: {search_url}")
        
        soup = self.make_request(search_url)
        if not soup:
            return []
        
        results = []
        
        try:
            # Find product cards
            products = soup.find_all('div', {'data-component-type': 's-search-result'}, limit=max_results)
            
            for product in products:
                try:
                    raw_data = self._extract_product_data(product)
                    if raw_data:
                        results.append(self.standardize_result(raw_data))
                except Exception as e:
                    logger.error(f"Error extracting Amazon product: {str(e)}")
                    continue
                
                self.rate_limit(0.5)
            
            logger.info(f"Found {len(results)} products on Amazon")
            
        except Exception as e:
            logger.error(f"Error scraping Amazon: {str(e)}")
        
        return results
    
    def _extract_product_data(self, product_elem) -> Dict:
        """Extract product data from product element."""
        try:
            # Extract title and URL
            title_elem = product_elem.find('h2', class_='s-line-clamp-2')
            link_elem = title_elem.find('a') if title_elem else None
            
            if not title_elem or not link_elem:
                return None
            
            title = title_elem.get_text(strip=True)
            url = self.base_url + link_elem.get('href', '')
            
            # Extract price
            price_elem = product_elem.find('span', class_='a-price-whole')
            price = price_elem.get_text(strip=True) if price_elem else '0'
            
            # Extract image
            img_elem = product_elem.find('img', class_='s-image')
            image_url = img_elem.get('src', '') if img_elem else ''
            
            # Extract rating
            rating_elem = product_elem.find('span', class_='a-icon-alt')
            rating = rating_elem.get_text(strip=True) if rating_elem else None
            
            # Extract review count
            review_elem = product_elem.find('span', class_='a-size-base', string=lambda x: x and 'ratings' in x.lower())
            review_count = review_elem.get_text(strip=True) if review_elem else None
            
            # Check availability
            availability_elem = product_elem.find('span', class_='a-color-price')
            availability = not (availability_elem and 'unavailable' in availability_elem.get_text().lower())
            
            return {
                'title': title,
                'url': url,
                'price': price,
                'currency': 'USD',
                'image_url': image_url,
                'rating': rating,
                'review_count': review_count,
                'availability': availability,
            }
            
        except Exception as e:
            logger.error(f"Error extracting Amazon product data: {str(e)}")
            return None
