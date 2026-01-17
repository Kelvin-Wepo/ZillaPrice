"""
Serializers for API endpoints.
"""
from rest_framework import serializers
from products.models import Product, ProductListing, Platform, PriceHistory, SearchHistory


class PlatformSerializer(serializers.ModelSerializer):
    """Serializer for Platform model."""
    
    class Meta:
        model = Platform
        fields = ['id', 'name', 'base_url', 'is_active']


class PriceHistorySerializer(serializers.ModelSerializer):
    """Serializer for PriceHistory model."""
    
    class Meta:
        model = PriceHistory
        fields = ['price', 'recorded_at']


class ProductListingSerializer(serializers.ModelSerializer):
    """Serializer for ProductListing model."""
    
    platform = PlatformSerializer(read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    price_history = PriceHistorySerializer(many=True, read_only=True)
    
    class Meta:
        model = ProductListing
        fields = [
            'id', 'platform', 'title', 'url', 'image_url',
            'price', 'currency', 'shipping_cost', 'total_price',
            'rating', 'review_count', 'availability', 'seller_name',
            'confidence_score', 'scraped_at', 'price_history'
        ]


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product model."""
    
    listings = ProductListingSerializer(many=True, read_only=True)
    lowest_price = serializers.SerializerMethodField()
    price_range = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'brand', 'category', 'description',
            'image_url', 'created_at', 'updated_at', 'search_count',
            'listings', 'lowest_price', 'price_range'
        ]
    
    def get_lowest_price(self, obj):
        """Get the lowest price from all listings."""
        listings = obj.listings.filter(availability=True)
        if listings.exists():
            lowest = listings.order_by('price').first()
            return {
                'price': float(lowest.price),
                'currency': lowest.currency,
                'platform': lowest.platform.name
            }
        return None
    
    def get_price_range(self, obj):
        """Get price range across all listings."""
        listings = obj.listings.filter(availability=True)
        if listings.exists():
            prices = [float(l.price) for l in listings]
            return {
                'min': min(prices),
                'max': max(prices),
                'avg': sum(prices) / len(prices)
            }
        return None


class SearchHistorySerializer(serializers.ModelSerializer):
    """Serializer for SearchHistory model."""
    
    class Meta:
        model = SearchHistory
        fields = [
            'id', 'query', 'search_type', 'results_count',
            'created_at'
        ]


class ImageSearchSerializer(serializers.Serializer):
    """Serializer for image search request."""
    
    image = serializers.ImageField(required=True)
    max_results = serializers.IntegerField(default=20, min_value=1, max_value=50)


class TextSearchSerializer(serializers.Serializer):
    """Serializer for text search request."""
    
    query = serializers.CharField(required=True, max_length=500)
    platforms = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        default=['jumia', 'kilimall', 'alibaba', 'amazon', 'ebay']
    )
    max_results = serializers.IntegerField(default=20, min_value=1, max_value=50)


class SearchResultSerializer(serializers.Serializer):
    """Serializer for search results."""
    
    task_id = serializers.CharField()
    status = serializers.CharField()
    message = serializers.CharField()
    products = ProductSerializer(many=True, required=False)
    search_info = serializers.DictField(required=False)
