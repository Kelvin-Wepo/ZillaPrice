#!/bin/bash

# Price Comparison App Setup Script

echo "🚀 Setting up Price Comparison Application..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env file and add your GEMINI_API_KEY"
    read -p "Press Enter to continue after editing .env file..."
fi

# Build and start services
echo "🐳 Building Docker containers..."
docker-compose build

echo "🚀 Starting services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# Run migrations
echo "📊 Running database migrations..."
docker-compose exec -T backend python manage.py migrate

# Create superuser prompt
echo ""
read -p "Do you want to create a superuser? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    docker-compose exec backend python manage.py createsuperuser
fi

# Initialize platforms
echo "🌐 Initializing e-commerce platforms..."
docker-compose exec -T backend python manage.py shell <<EOF
from products.models import Platform

platforms = [
    {'name': 'jumia', 'base_url': 'https://www.jumia.com.ng'},
    {'name': 'kilimall', 'base_url': 'https://www.kilimall.co.ke'},
    {'name': 'alibaba', 'base_url': 'https://www.alibaba.com'},
    {'name': 'amazon', 'base_url': 'https://www.amazon.com'},
    {'name': 'ebay', 'base_url': 'https://www.ebay.com'},
]

for platform in platforms:
    Platform.objects.get_or_create(**platform)

print("Platforms initialized successfully!")
EOF

echo ""
echo "✅ Setup complete!"
echo ""
echo "📱 Application is running:"
echo "   Frontend:  http://localhost:3000"
echo "   Backend:   http://localhost:8000"
echo "   Admin:     http://localhost:8000/admin"
echo ""
echo "📚 Useful commands:"
echo "   View logs:       docker-compose logs -f"
echo "   Stop services:   docker-compose down"
echo "   Restart:         docker-compose restart"
echo ""
