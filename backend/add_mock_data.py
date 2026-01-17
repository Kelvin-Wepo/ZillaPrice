#!/usr/bin/env python
"""Add mock product data for demonstration."""
import os
import django
import random
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Platform, Product, ProductListing
from django.utils import timezone

# Get all platforms
platforms = {p.name: p for p in Platform.objects.all()}

# Sample products with prices
mock_products = [
    {
        'name': 'Apple iPhone 15 Pro Max 256GB',
        'prices': {
            'jumia': (1200.00, 'KES'),
            'amazon': (1299.99, 'USD'),
            'ebay': (1249.00, 'USD'),
            'alibaba': (1150.00, 'USD'),
            'kilimall': (1180.00, 'KES'),
        }
    },
    {
        'name': 'Samsung Galaxy S24 Ultra 512GB',
        'prices': {
            'jumia': (1100.00, 'KES'),
            'amazon': (1199.99, 'USD'),
            'ebay': (1150.00, 'USD'),
            'alibaba': (1050.00, 'USD'),
            'kilimall': (1080.00, 'KES'),
        }
    },
    {
        'name': 'MacBook Pro 14" M3 16GB RAM',
        'prices': {
            'jumia': (1999.00, 'KES'),
            'amazon': (1999.99, 'USD'),
            'ebay': (1899.00, 'USD'),
            'alibaba': (1850.00, 'USD'),
            'kilimall': (1950.00, 'KES'),
        }
    },
    {
        'name': 'Sony WH-1000XM5 Headphones',
        'prices': {
            'jumia': (399.00, 'KES'),
            'amazon': (399.99, 'USD'),
            'ebay': (379.00, 'USD'),
            'alibaba': (350.00, 'USD'),
            'kilimall': (385.00, 'KES'),
        }
    },
    {
        'name': 'Apple AirPods Pro 2nd Generation',
        'prices': {
            'jumia': (249.00, 'KES'),
            'amazon': (249.99, 'USD'),
            'ebay': (229.00, 'USD'),
            'alibaba': (220.00, 'USD'),
            'kilimall': (235.00, 'KES'),
        }
    },
]

print("Adding mock data for demonstration...")
print(f"{'='*60}")

for product_data in mock_products:
    # Get or create product
    product, created = Product.objects.get_or_create(
        name=product_data['name'],
        defaults={
            'description': f"High-quality {product_data['name']}",
            'category': 'Electronics',
            'brand': product_data['name'].split()[0],
        }
    )
    
    if created:
        print(f"✓ Created product: {product.name}")
    else:
        print(f"• Product exists: {product.name}")
    
    # Add listings for each platform
    for platform_name, (price, currency) in product_data['prices'].items():
        platform = platforms.get(platform_name)
        if not platform:
            continue
            
        # Check if listing exists
        listing, listing_created = ProductListing.objects.get_or_create(
            product=product,
            platform=platform,
            defaults={
                'title': product.name,
                'price': Decimal(str(price)),
                'currency': currency,
                'url': f'https://www.{platform_name}.com/product/{product.id}',
                'image_url': f'https://via.placeholder.com/300x300?text={product.name.replace(" ", "+")}',
                'availability': True,
                'rating': round(random.uniform(4.0, 5.0), 1),
                'review_count': random.randint(50, 500),
                'seller_name': f'{platform_name.title()} Official Store',
                'shipping_cost': Decimal(str(random.uniform(0, 20))),
                'scraped_at': timezone.now(),
            }
        )
        
        if listing_created:
            print(f"  + Added {platform_name} listing: ${price}")

print(f"{'='*60}")
print("\n✅ Mock data added successfully!")
print(f"\nTotal products: {Product.objects.count()}")
print(f"Total listings: {ProductListing.objects.count()}")
print("\nYou can now search and compare prices across all platforms!")
