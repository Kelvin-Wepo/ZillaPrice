"""
Admin configuration for products app.
"""
from django.contrib import admin
from .models import Platform, Product, ProductListing, PriceHistory, SearchHistory, ScrapingTask


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ['name', 'base_url', 'is_active', 'created_at']
    list_filter = ['is_active', 'name']
    search_fields = ['name', 'base_url']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'category', 'search_count', 'created_at']
    list_filter = ['category', 'brand', 'created_at']
    search_fields = ['name', 'brand', 'category']
    readonly_fields = ['search_count', 'created_at', 'updated_at']


class PriceHistoryInline(admin.TabularInline):
    model = PriceHistory
    extra = 0
    readonly_fields = ['price', 'recorded_at']


@admin.register(ProductListing)
class ProductListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'platform', 'price', 'currency', 'availability', 'rating', 'scraped_at']
    list_filter = ['platform', 'availability', 'currency', 'scraped_at']
    search_fields = ['title', 'seller_name']
    readonly_fields = ['scraped_at', 'last_updated']
    inlines = [PriceHistoryInline]


@admin.register(PriceHistory)
class PriceHistoryAdmin(admin.ModelAdmin):
    list_display = ['listing', 'price', 'recorded_at']
    list_filter = ['recorded_at']
    readonly_fields = ['recorded_at']


@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ['query', 'search_type', 'results_count', 'created_at']
    list_filter = ['search_type', 'created_at']
    search_fields = ['query']
    readonly_fields = ['created_at']


@admin.register(ScrapingTask)
class ScrapingTaskAdmin(admin.ModelAdmin):
    list_display = ['search_query', 'platform', 'status', 'results_count', 'created_at']
    list_filter = ['status', 'platform', 'created_at']
    search_fields = ['search_query', 'task_id']
    readonly_fields = ['task_id', 'created_at', 'started_at', 'completed_at']
