"""
URL configuration for API app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'platforms', views.PlatformViewSet, basename='platform')

urlpatterns = [
    path('', include(router.urls)),
    
    # Search endpoints
    path('search/text/', views.text_search, name='text-search'),
    path('search/image/', views.image_search, name='image-search'),
    path('search/status/<str:task_id>/', views.search_status, name='search-status'),
    path('search/history/', views.search_history_list, name='search-history'),
    
    # Comparison
    path('compare/', views.compare_products, name='compare-products'),
]
