"""
Models for product and price tracking.
"""
from django.db import models
from django.utils import timezone


class Platform(models.Model):
    """E-commerce platforms to scrape."""
    
    PLATFORMS = [
        ('jumia', 'Jumia'),
        ('kilimall', 'Kilimall'),
        ('alibaba', 'Alibaba'),
        ('amazon', 'Amazon'),
        ('ebay', 'eBay'),
    ]
    
    name = models.CharField(max_length=50, choices=PLATFORMS, unique=True)
    base_url = models.URLField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name', 'is_active']),
        ]
    
    def __str__(self):
        return self.get_name_display()


class Product(models.Model):
    """Product information aggregated from multiple platforms."""
    
    name = models.CharField(max_length=500, db_index=True)
    brand = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True, max_length=1000)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    search_count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['name', '-created_at']),
            models.Index(fields=['brand', 'category']),
            models.Index(fields=['-search_count']),
        ]
    
    def __str__(self):
        return self.name
    
    def increment_search_count(self):
        """Increment the search count for analytics."""
        self.search_count += 1
        self.save(update_fields=['search_count'])


class ProductListing(models.Model):
    """Individual product listings from different platforms."""
    
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='listings'
    )
    platform = models.ForeignKey(
        Platform,
        on_delete=models.CASCADE,
        related_name='listings'
    )
    
    # Product details
    title = models.CharField(max_length=500)
    url = models.URLField(max_length=1000)
    image_url = models.URLField(max_length=1000, blank=True)
    
    # Price information
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Additional info
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    review_count = models.IntegerField(null=True, blank=True)
    availability = models.BooleanField(default=True)
    seller_name = models.CharField(max_length=200, blank=True)
    
    # Confidence score for image-based searches
    confidence_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="AI confidence score (0-100)"
    )
    
    # Timestamps
    scraped_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['price']
        indexes = [
            models.Index(fields=['product', 'platform']),
            models.Index(fields=['price', 'availability']),
            models.Index(fields=['-scraped_at']),
        ]
        unique_together = [['url', 'platform']]
    
    def __str__(self):
        return f"{self.title} - {self.platform.name} - ${self.price}"
    
    @property
    def total_price(self):
        """Calculate total price including shipping."""
        if self.shipping_cost:
            return self.price + self.shipping_cost
        return self.price


class PriceHistory(models.Model):
    """Track price changes over time."""
    
    listing = models.ForeignKey(
        ProductListing,
        on_delete=models.CASCADE,
        related_name='price_history'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    recorded_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-recorded_at']
        indexes = [
            models.Index(fields=['listing', '-recorded_at']),
        ]
        verbose_name_plural = 'Price histories'
    
    def __str__(self):
        return f"{self.listing.title} - ${self.price} at {self.recorded_at}"


class SearchHistory(models.Model):
    """Track user search queries for analytics."""
    
    SEARCH_TYPES = [
        ('text', 'Text Search'),
        ('image', 'Image Search'),
    ]
    
    query = models.CharField(max_length=500)
    search_type = models.CharField(max_length=10, choices=SEARCH_TYPES)
    image_path = models.CharField(max_length=500, blank=True)
    
    # Results
    results_count = models.IntegerField(default=0)
    products_found = models.ManyToManyField(Product, related_name='searches', blank=True)
    
    # Metadata
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['search_type']),
        ]
        verbose_name_plural = 'Search histories'
    
    def __str__(self):
        return f"{self.search_type}: {self.query} ({self.created_at})"


class ScrapingTask(models.Model):
    """Track scraping task status."""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    task_id = models.CharField(max_length=255, unique=True)
    search_query = models.CharField(max_length=500)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Results
    results_count = models.IntegerField(default=0)
    error_message = models.TextField(blank=True)
    
    # Timestamps
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['task_id']),
            models.Index(fields=['status', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.platform.name}: {self.search_query} - {self.status}"
