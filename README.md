# Price Comparison Web Application

A full-stack web application that allows users to compare product prices across multiple e-commerce platforms (Jumia, Kilimall, Alibaba, Amazon, and eBay) using either text search or image recognition powered by Google Gemini AI.

## Features

### Core Functionality
- **Text-Based Product Search**: Enter product names to search across all platforms simultaneously
- **Image-Based Product Search**: Upload product images for AI-powered identification and search
- **Real-Time Results**: View results as they arrive from each platform
- **Price Comparison Dashboard**: Side-by-side comparison with filtering and sorting
- **Price History Tracking**: Monitor price changes over time with interactive charts
- **Best Deal Highlighting**: Automatically identify and highlight the best deals
- **Multi-Platform Support**: Jumia, Kilimall, Alibaba, Amazon, and eBay

### Technical Features
- Async scraping with Celery for non-blocking operations
- Redis caching for improved performance
- Google Gemini AI for image recognition
- RESTful API with Django REST Framework
- Responsive React UI with TypeScript
- PostgreSQL database with optimized indexing
- Docker containerization for easy deployment

## Tech Stack

### Backend
- **Framework**: Django 5.0+ with Django REST Framework
- **Database**: PostgreSQL
- **Task Queue**: Celery with Redis
- **Cache**: Redis
- **Web Scraping**: BeautifulSoup4, Selenium
- **AI**: Google Gemini API

### Frontend
- **Framework**: React 18+ with TypeScript
- **Build Tool**: Vite
- **Styling**: TailwindCSS
- **State Management**: React Query
- **Charts**: Recharts
- **Icons**: Lucide React

## Prerequisites

- Python 3.11+
- Node.js 20+
- PostgreSQL 16+
- Redis 7+
- Docker & Docker Compose (optional)
- Google Gemini API Key

## Installation

### Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Zilla
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   ```

3. **Configure environment variables**
   Edit `.env` and set:
   - `SECRET_KEY`: Django secret key
   - `GEMINI_API_KEY`: Your Google Gemini API key
   - Other settings as needed

4. **Start services with Docker Compose**
   ```bash
   docker-compose up -d
   ```

5. **Run migrations**
   ```bash
   docker-compose exec backend python manage.py migrate
   ```

6. **Create superuser (optional)**
   ```bash
   docker-compose exec backend python manage.py createsuperuser
   ```

7. **Initialize platforms**
   ```bash
   docker-compose exec backend python manage.py shell
   ```
   ```python
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
   ```

8. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Admin: http://localhost:8000/admin

### Manual Installation

#### Backend Setup

1. **Create virtual environment**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup PostgreSQL database**
   ```bash
   createdb pricecomparison
   ```

4. **Configure environment**
   ```bash
   cp ../.env.example ../.env
   # Edit .env with your settings
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Initialize platforms** (see Docker step 7 above)

8. **Start Redis**
   ```bash
   redis-server
   ```

9. **Start Celery worker**
   ```bash
   celery -A config worker -l info
   ```

10. **Start Celery beat** (in another terminal)
    ```bash
    celery -A config beat -l info
    ```

11. **Start Django server**
    ```bash
    python manage.py runserver
    ```

#### Frontend Setup

1. **Install dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Configure API URL**
   Create `.env.local`:
   ```
   VITE_API_URL=http://localhost:8000
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```

## API Documentation

### Search Endpoints

#### Text Search
```http
POST /api/search/text/
Content-Type: application/json

{
  "query": "iPhone 15 Pro",
  "platforms": ["jumia", "amazon", "ebay"],
  "max_results": 20
}
```

#### Image Search
```http
POST /api/search/image/
Content-Type: multipart/form-data

image: <file>
max_results: 20
```

#### Search Status
```http
GET /api/search/status/<task_id>/
```

#### Compare Products
```http
GET /api/compare/?query=iPhone+15
GET /api/compare/?product_id=123
```

### Product Endpoints

#### List Products
```http
GET /api/products/
GET /api/products/?category=Electronics
GET /api/products/?brand=Apple
```

#### Get Product Details
```http
GET /api/products/<id>/
```

#### Get Price History
```http
GET /api/products/<id>/price_history/
```

### Platform Endpoints

#### List Platforms
```http
GET /api/platforms/
```

## Project Structure

```
Zilla/
├── backend/
│   ├── api/                    # REST API app
│   │   ├── serializers.py      # DRF serializers
│   │   ├── views.py            # API views
│   │   ├── urls.py             # API routes
│   │   └── tasks.py            # Celery tasks
│   ├── config/                 # Django settings
│   │   ├── settings.py         # Main settings
│   │   ├── celery.py           # Celery config
│   │   └── urls.py             # Root URLs
│   ├── products/               # Product models
│   │   ├── models.py           # Database models
│   │   └── admin.py            # Admin interface
│   ├── scraping/               # Web scraping
│   │   ├── base_scraper.py     # Base scraper class
│   │   ├── jumia_scraper.py    # Jumia scraper
│   │   ├── kilimall_scraper.py # Kilimall scraper
│   │   ├── amazon_scraper.py   # Amazon scraper
│   │   ├── ebay_scraper.py     # eBay scraper
│   │   ├── alibaba_scraper.py  # Alibaba scraper
│   │   ├── gemini_service.py   # AI service
│   │   └── scraper_factory.py  # Scraper factory
│   ├── manage.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/         # React components
│   │   │   ├── Layout.tsx
│   │   │   ├── SearchBar.tsx
│   │   │   └── ProductCard.tsx
│   │   ├── pages/              # Page components
│   │   │   ├── HomePage.tsx
│   │   │   ├── SearchResultsPage.tsx
│   │   │   ├── ComparisonPage.tsx
│   │   │   └── ProductDetailsPage.tsx
│   │   ├── api.ts              # API client
│   │   ├── types.ts            # TypeScript types
│   │   ├── utils.ts            # Utility functions
│   │   ├── config.ts           # Configuration
│   │   ├── App.tsx             # Main app component
│   │   └── main.tsx            # Entry point
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

## Usage

### Text Search

1. Navigate to the home page
2. Enter a product name in the search bar
3. Click search or press Enter
4. View results from all platforms as they arrive
5. Filter by platform and sort by price
6. Click "View Deal" to visit the product page

### Image Search

1. Click the "Image Search" tab
2. Upload or drag an image
3. Click "Search with Image"
4. AI identifies the product and searches all platforms
5. View results with confidence scores

### Price Comparison

1. Search for a product
2. Navigate to the comparison page
3. View side-by-side price comparison
4. See best deal highlighted
5. View price statistics and history

## Configuration

### Environment Variables

```bash
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/pricecomparison

# Redis
REDIS_URL=redis://localhost:6379/0

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Google Gemini API
GEMINI_API_KEY=your-gemini-api-key-here

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# Scraping Settings
USER_AGENT=Mozilla/5.0 (Windows NT 10.0; Win64; x64)
SCRAPING_TIMEOUT=30
MAX_CONCURRENT_SCRAPERS=5
```

## Development

### Running Tests

```bash
# Backend tests
cd backend
python manage.py test

# Frontend tests
cd frontend
npm test
```

### Code Quality

```bash
# Backend
black backend/
flake8 backend/

# Frontend
npm run lint
```

## Deployment

### Production Considerations

1. **Set DEBUG=False** in production
2. **Use strong SECRET_KEY**
3. **Configure proper ALLOWED_HOSTS**
4. **Use production-grade database**
5. **Enable HTTPS**
6. **Set up proper logging**
7. **Configure rate limiting**
8. **Use CDN for static files**
9. **Implement monitoring**
10. **Set up backups**

### Docker Production Build

```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Troubleshooting

### Common Issues

1. **Scraping fails**: Some platforms may block requests. Consider using proxies or rotating user agents.

2. **Celery tasks not running**: Ensure Redis is running and Celery worker/beat are started.

3. **Image search fails**: Verify GEMINI_API_KEY is set correctly.

4. **Database connection errors**: Check DATABASE_URL and PostgreSQL service.

5. **CORS errors**: Ensure frontend URL is in CORS_ALLOWED_ORIGINS.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation
- Review API documentation

## Acknowledgments

- Google Gemini AI for image recognition
- E-commerce platforms for product data
- Open source community for tools and libraries

## Roadmap

- [ ] Add more e-commerce platforms
- [ ] Implement user accounts
- [ ] Add product watchlist
- [ ] Email price alerts
- [ ] Mobile app
- [ ] Advanced filtering options
- [ ] Product recommendations
- [ ] Cryptocurrency payment tracking
# ZillaPrice
