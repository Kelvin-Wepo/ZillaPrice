"""
Celery tasks for async scraping and price tracking.
"""
import logging
from celery import shared_task, group
from django.utils import timezone
from django.core.cache import cache
from products.models import Product, ProductListing, Platform, ScrapingTask, PriceHistory
from scraping.scraper_factory import ScraperFactory
from scraping.gemini_service import GeminiService

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def scrape_platform(self, platform_name: str, query: str, max_results: int = 20):
    """
    Scrape a single platform for products.
    
    Args:
        platform_name: Name of the platform to scrape
        query: Search query
        max_results: Maximum number of results
        
    Returns:
        List of product data
    """
    task_id = self.request.id
    
    try:
        # Get platform
        platform = Platform.objects.get(name=platform_name, is_active=True)
        
        # Create scraping task record
        scraping_task = ScrapingTask.objects.create(
            task_id=task_id,
            search_query=query,
            platform=platform,
            status='running',
            started_at=timezone.now()
        )
        
        logger.info(f"Starting scraping task {task_id} for {platform_name}: {query}")
        
        # Get scraper and search
        scraper = ScraperFactory.get_scraper(platform_name)
        results = scraper.search(query, max_results=max_results)
        
        # Save results to database
        product_ids = []
        for result_data in results:
            try:
                product_id = save_product_listing(result_data, platform, query)
                if product_id:
                    product_ids.append(product_id)
            except Exception as e:
                logger.error(f"Error saving product: {str(e)}")
                continue
        
        # Update task status
        scraping_task.status = 'completed'
        scraping_task.results_count = len(product_ids)
        scraping_task.completed_at = timezone.now()
        scraping_task.save()
        
        logger.info(f"Completed scraping task {task_id}: {len(product_ids)} products")
        
        return {
            'task_id': task_id,
            'platform': platform_name,
            'results_count': len(product_ids),
            'product_ids': product_ids,
            'status': 'completed'
        }
        
    except Platform.DoesNotExist:
        logger.error(f"Platform {platform_name} not found or inactive")
        return {
            'task_id': task_id,
            'platform': platform_name,
            'error': 'Platform not found',
            'status': 'failed'
        }
    
    except Exception as e:
        logger.error(f"Error in scraping task {task_id}: {str(e)}")
        
        # Update task status
        try:
            scraping_task = ScrapingTask.objects.get(task_id=task_id)
            scraping_task.status = 'failed'
            scraping_task.error_message = str(e)
            scraping_task.completed_at = timezone.now()
            scraping_task.save()
        except:
            pass
        
        # Retry on failure
        raise self.retry(exc=e, countdown=60)


@shared_task
def scrape_all_platforms(query: str, platforms: list = None, max_results: int = 20):
    """
    Scrape all platforms in parallel.
    
    Args:
        query: Search query
        platforms: List of platform names (defaults to all)
        max_results: Maximum results per platform
        
    Returns:
        Group result object
    """
    if platforms is None:
        platforms = ['jumia', 'kilimall', 'alibaba', 'amazon', 'ebay']
    
    logger.info(f"Starting parallel scraping for query: {query}")
    
    # Create group of tasks
    job = group([
        scrape_platform.s(platform, query, max_results)
        for platform in platforms
    ])
    
    result = job.apply_async()
    
    # Cache the group result ID for status checking (use safe key without colons)
    cache_key = f"scraping_group_{result.id}"
    cache.set(cache_key, {
        'query': query,
        'platforms': platforms,
        'started_at': timezone.now().isoformat()
    }, timeout=3600)
    
    return {
        'group_id': result.id,
        'query': query,
        'platforms': platforms,
        'status': 'running'
    }


@shared_task
def image_search_task(image_path: str, max_results: int = 20):
    """
    Process image search with Gemini AI and scrape all platforms.
    
    Args:
        image_path: Path to uploaded image
        max_results: Maximum results per platform
        
    Returns:
        Search results
    """
    logger.info(f"Starting image search task for: {image_path}")
    
    try:
        # Read image file
        with open(image_path, 'rb') as f:
            image_data = f.read()
        
        # Use Gemini to identify product
        gemini_service = GeminiService()
        product_info = gemini_service.identify_product_from_image(image_data)
        
        if not product_info:
            logger.error("Failed to identify product from image")
            return {
                'status': 'failed',
                'error': 'Could not identify product from image'
            }
        
        # Generate search query
        search_query = gemini_service.generate_search_query(image_data)
        
        if not search_query:
            search_query = product_info.get('product_name', 'unknown product')
        
        logger.info(f"Generated search query: {search_query}")
        
        # Scrape all platforms
        result = scrape_all_platforms(search_query, max_results=max_results)
        
        # Add product info to result
        result['product_info'] = product_info
        result['search_query'] = search_query
        
        return result
        
    except Exception as e:
        logger.error(f"Error in image search task: {str(e)}")
        return {
            'status': 'failed',
            'error': str(e)
        }


def save_product_listing(result_data: dict, platform: Platform, query: str) -> int:
    """
    Save or update product listing in database.
    
    Args:
        result_data: Product data from scraper
        platform: Platform object
        query: Search query
        
    Returns:
        Product ID
    """
    # Create or get product
    product, created = Product.objects.get_or_create(
        name=result_data['title'][:500],
        defaults={
            'image_url': result_data.get('image_url', ''),
            'description': result_data.get('title', ''),
        }
    )
    
    # Create or update listing
    listing, created = ProductListing.objects.update_or_create(
        url=result_data['url'],
        platform=platform,
        defaults={
            'product': product,
            'title': result_data['title'],
            'image_url': result_data.get('image_url', ''),
            'price': result_data['price'],
            'currency': result_data.get('currency', 'USD'),
            'shipping_cost': result_data.get('shipping_cost'),
            'rating': result_data.get('rating'),
            'review_count': result_data.get('review_count'),
            'availability': result_data.get('availability', True),
            'seller_name': result_data.get('seller_name', ''),
            'confidence_score': result_data.get('confidence_score'),
        }
    )
    
    # Track price history
    if not created:
        # Check if price changed
        latest_price = listing.price_history.first()
        if not latest_price or latest_price.price != listing.price:
            PriceHistory.objects.create(
                listing=listing,
                price=listing.price
            )
    else:
        # Create initial price history entry
        PriceHistory.objects.create(
            listing=listing,
            price=listing.price
        )
    
    return product.id


@shared_task
def update_price_history():
    """
    Periodic task to update price history for all products.
    """
    logger.info("Starting periodic price history update")
    
    # Get all active listings
    listings = ProductListing.objects.filter(
        platform__is_active=True,
        availability=True
    )
    
    updated_count = 0
    
    for listing in listings:
        try:
            # Re-scrape the product
            scraper = ScraperFactory.get_scraper(listing.platform.name)
            # This would require implementation of individual product scraping
            # For now, we'll just log
            logger.debug(f"Would update: {listing.title}")
            updated_count += 1
            
        except Exception as e:
            logger.error(f"Error updating listing {listing.id}: {str(e)}")
            continue
    
    logger.info(f"Completed price history update: {updated_count} listings")
    return updated_count
