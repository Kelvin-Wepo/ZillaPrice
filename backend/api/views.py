"""
API views for product search and comparison.
"""
import logging
import os
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.core.cache import cache
from django.core.files.storage import default_storage
from django.utils import timezone
from celery.result import GroupResult
from products.models import Product, ProductListing, Platform, SearchHistory
from .serializers import (
    ProductSerializer, ProductListingSerializer, PlatformSerializer,
    ImageSearchSerializer, TextSearchSerializer, SearchResultSerializer,
    SearchHistorySerializer
)
from .tasks import scrape_all_platforms, image_search_task

logger = logging.getLogger(__name__)


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Product model."""
    
    queryset = Product.objects.all().prefetch_related('listings__platform')
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        """Filter and order queryset."""
        queryset = super().get_queryset()
        
        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        # Filter by brand
        brand = self.request.query_params.get('brand')
        if brand:
            queryset = queryset.filter(brand=brand)
        
        # Order by
        order_by = self.request.query_params.get('order_by', '-created_at')
        queryset = queryset.order_by(order_by)
        
        return queryset
    
    @action(detail=True, methods=['get'])
    def price_history(self, request, pk=None):
        """Get price history for a product across all platforms."""
        product = self.get_object()
        
        history_data = []
        for listing in product.listings.all():
            price_history = listing.price_history.all()[:30]  # Last 30 records
            
            history_data.append({
                'platform': listing.platform.name,
                'listing_id': listing.id,
                'history': [
                    {
                        'price': float(ph.price),
                        'recorded_at': ph.recorded_at.isoformat()
                    }
                    for ph in price_history
                ]
            })
        
        return Response(history_data)


class PlatformViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Platform model."""
    
    queryset = Platform.objects.filter(is_active=True)
    serializer_class = PlatformSerializer


@api_view(['POST'])
def text_search(request):
    """
    Search for products using text query.
    
    POST /api/search/text/
    {
        "query": "iPhone 15 Pro",
        "platforms": ["jumia", "amazon", "ebay"],  // optional
        "max_results": 20  // optional
    }
    """
    serializer = TextSearchSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    query = serializer.validated_data['query']
    platforms = serializer.validated_data['platforms']
    max_results = serializer.validated_data['max_results']
    
    # Check cache first - use safe cache key (no spaces or special chars)
    import hashlib
    cache_key_raw = f"search_{query}_{'_'.join(sorted(platforms))}"
    cache_key = hashlib.md5(cache_key_raw.encode()).hexdigest()
    cached_result = cache.get(cache_key)
    
    if cached_result:
        logger.info(f"Returning cached results for query: {query}")
        return Response(cached_result)
    
    # Create search history
    search_history = SearchHistory.objects.create(
        query=query,
        search_type='text',
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', '')
    )
    
    # Start async scraping
    result = scrape_all_platforms(query, platforms, max_results)
    
    response_data = {
        'task_id': result['group_id'],
        'status': 'processing',
        'message': f'Searching {len(platforms)} platforms for "{query}"',
        'search_id': search_history.id,
        'query': query,
        'platforms': platforms
    }
    
    return Response(response_data, status=status.HTTP_202_ACCEPTED)


@api_view(['POST'])
def image_search(request):
    """
    Search for products using image.
    
    POST /api/search/image/
    Content-Type: multipart/form-data
    
    Form Data:
        image: <image file>
        max_results: 20 (optional)
    """
    parser_classes = [MultiPartParser, FormParser]
    serializer = ImageSearchSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    image = serializer.validated_data['image']
    max_results = serializer.validated_data['max_results']
    
    # Save uploaded image
    image_path = default_storage.save(
        f'uploads/{timezone.now().strftime("%Y%m%d_%H%M%S")}_{image.name}',
        image
    )
    
    full_image_path = os.path.join(default_storage.location, image_path)
    
    # Create search history
    search_history = SearchHistory.objects.create(
        query='Image Search',
        search_type='image',
        image_path=image_path,
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', '')
    )
    
    # Start async image processing and scraping
    task = image_search_task.delay(full_image_path, max_results)
    
    response_data = {
        'task_id': task.id,
        'status': 'processing',
        'message': 'Processing image and searching platforms',
        'search_id': search_history.id,
        'image_path': image_path
    }
    
    return Response(response_data, status=status.HTTP_202_ACCEPTED)


@api_view(['GET'])
def search_status(request, task_id):
    """
    Check status of search task.
    
    GET /api/search/status/<task_id>/
    """
    # Check if it's a group task
    cache_key = f"scraping_group_{task_id}"
    group_info = cache.get(cache_key)
    
    if not group_info:
        # Not a recognized task
        return Response({
            'status': 'not_found',
            'message': 'Task not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Check database for completed scraping tasks
    from products.models import ScrapingTask
    query = group_info.get('query')
    platforms_to_check = group_info.get('platforms', [])
    
    # Get scraping tasks for this query from the database
    scraping_tasks = ScrapingTask.objects.filter(
        search_query=query,
        platform__name__in=platforms_to_check,
        created_at__gte=timezone.now() - timezone.timedelta(minutes=10)
    ).select_related('platform')
    
    if not scraping_tasks.exists():
        # Tasks not yet created or very old
        return Response({
            'status': 'processing',
            'message': 'Initializing search...',
            'query': query,
            'platforms': platforms_to_check
        })
    
    # Check completion status
    total_tasks = len(platforms_to_check)
    completed_tasks = scraping_tasks.filter(status='completed').count()
    failed_tasks = scraping_tasks.filter(status='failed').count()
    
    if completed_tasks + failed_tasks >= total_tasks:
        # All tasks done - get products
        all_product_ids = []
        for task in scraping_tasks.filter(status='completed'):
            # Get products created by this scraping task
            products = Product.objects.filter(
                listings__scraped_at__gte=task.started_at,
                listings__platform=task.platform,
                name__icontains=query.split()[0]  # Basic matching
            ).distinct()
            all_product_ids.extend(products.values_list('id', flat=True))
        
        # Get unique products
        products = Product.objects.filter(
            id__in=set(all_product_ids)
        ).prefetch_related('listings__platform')
        
        # Cache results
        import hashlib
        cache_key_raw = f"search_{query}_{'_'.join(sorted(platforms_to_check))}"
        result_cache_key = hashlib.md5(cache_key_raw.encode()).hexdigest()
        
        response_data = {
            'status': 'completed',
            'message': f'Found {len(products)} products',
            'products': ProductSerializer(products, many=True).data,
            'platforms_scraped': completed_tasks,
            'query': query
        }
        
        cache.set(result_cache_key, response_data, timeout=3600)
        
        return Response(response_data)
    
    else:
        # Still processing
        return Response({
            'status': 'processing',
            'message': f'Searching platforms ({completed_tasks}/{total_tasks} completed)',
            'progress': {
                'completed': completed_tasks,
                'total': total_tasks,
                'percentage': int((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 0
            },
            'query': query,
            'platforms': platforms_to_check
        })
    
    # Check single task
    from celery.result import AsyncResult
    task_result = AsyncResult(task_id)
    
    if task_result.state == 'PENDING':
        return Response({
            'status': 'pending',
            'message': 'Task is waiting to be processed'
        })
    
    elif task_result.state == 'STARTED':
        return Response({
            'status': 'processing',
            'message': 'Task is being processed'
        })
    
    elif task_result.state == 'SUCCESS':
        result = task_result.get()
        
        if 'group_id' in result:
            # Redirect to group status
            return search_status(request, result['group_id'])
        
        return Response({
            'status': 'completed',
            'message': 'Search completed',
            'result': result
        })
    
    elif task_result.state == 'FAILURE':
        return Response({
            'status': 'failed',
            'message': 'Task failed',
            'error': str(task_result.info)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response({
        'status': task_result.state.lower(),
        'message': f'Task state: {task_result.state}'
    })


@api_view(['GET'])
def compare_products(request):
    """
    Compare products across platforms.
    
    GET /api/compare/?product_id=123
    GET /api/compare/?query=iPhone+15
    """
    product_id = request.query_params.get('product_id')
    query = request.query_params.get('query')
    
    if product_id:
        try:
            product = Product.objects.get(id=product_id)
            products = [product]
        except Product.DoesNotExist:
            return Response(
                {'error': 'Product not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    elif query:
        products = Product.objects.filter(name__icontains=query)[:10]
    else:
        return Response(
            {'error': 'product_id or query parameter required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    comparison_data = []
    
    for product in products:
        listings = product.listings.filter(availability=True)
        
        if not listings.exists():
            continue
        
        # Group by platform
        platform_prices = {}
        for listing in listings:
            platform_name = listing.platform.name
            
            if platform_name not in platform_prices:
                platform_prices[platform_name] = []
            
            platform_prices[platform_name].append({
                'listing_id': listing.id,
                'title': listing.title,
                'price': float(listing.price),
                'currency': listing.currency,
                'total_price': float(listing.total_price),
                'url': listing.url,
                'rating': float(listing.rating) if listing.rating else None,
                'review_count': listing.review_count,
                'seller': listing.seller_name
            })
        
        # Find best deal
        all_listings = list(listings)
        best_deal = min(all_listings, key=lambda x: x.total_price)
        
        comparison_data.append({
            'product': ProductSerializer(product).data,
            'platform_prices': platform_prices,
            'best_deal': {
                'platform': best_deal.platform.name,
                'price': float(best_deal.price),
                'total_price': float(best_deal.total_price),
                'url': best_deal.url,
                'savings': float(
                    max(l.total_price for l in all_listings) - best_deal.total_price
                )
            },
            'price_stats': {
                'min': float(min(l.total_price for l in all_listings)),
                'max': float(max(l.total_price for l in all_listings)),
                'avg': float(sum(l.total_price for l in all_listings) / len(all_listings)),
                'count': len(all_listings)
            }
        })
    
    return Response({
        'comparisons': comparison_data,
        'total_products': len(comparison_data)
    })


@api_view(['GET'])
def search_history_list(request):
    """Get recent search history."""
    history = SearchHistory.objects.all()[:50]
    serializer = SearchHistorySerializer(history, many=True)
    return Response(serializer.data)


def get_client_ip(request):
    """Extract client IP address from request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
