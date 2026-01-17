"""
Scraper factory to get the appropriate scraper for each platform.
"""
from typing import Optional
from .jumia_scraper import JumiaScraper
from .kilimall_scraper import KilimallScraper
from .amazon_scraper import AmazonScraper
from .ebay_scraper import EbayScraper
from .alibaba_scraper import AlibabaScraper


class ScraperFactory:
    """Factory class to create scraper instances."""
    
    _scrapers = {
        'jumia': JumiaScraper,
        'kilimall': KilimallScraper,
        'amazon': AmazonScraper,
        'ebay': EbayScraper,
        'alibaba': AlibabaScraper,
    }
    
    @classmethod
    def get_scraper(cls, platform_name: str):
        """Get scraper instance for the given platform."""
        scraper_class = cls._scrapers.get(platform_name.lower())
        
        if not scraper_class:
            raise ValueError(f"No scraper found for platform: {platform_name}")
        
        return scraper_class()
    
    @classmethod
    def get_all_scrapers(cls):
        """Get all available scrapers."""
        return {name: scraper() for name, scraper in cls._scrapers.items()}
    
    @classmethod
    def get_platform_names(cls):
        """Get list of all supported platform names."""
        return list(cls._scrapers.keys())
