#!/usr/bin/env python
"""Script to create platform records in the database."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Platform

platforms = [
    {'name': 'jumia', 'base_url': 'https://www.jumia.com', 'is_active': True},
    {'name': 'kilimall', 'base_url': 'https://www.kilimall.com', 'is_active': True},
    {'name': 'alibaba', 'base_url': 'https://www.alibaba.com', 'is_active': True},
    {'name': 'amazon', 'base_url': 'https://www.amazon.com', 'is_active': True},
    {'name': 'ebay', 'base_url': 'https://www.ebay.com', 'is_active': True},
]

for p in platforms:
    platform, created = Platform.objects.get_or_create(name=p['name'], defaults=p)
    if created:
        print(f'✓ Created platform: {p["name"]}')
    else:
        print(f'✓ Platform already exists: {p["name"]}')

print(f'\nTotal platforms: {Platform.objects.count()}')
