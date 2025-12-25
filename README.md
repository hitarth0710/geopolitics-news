# GeoPolitics Watch

A production-ready news aggregator web application focused on world geopolitics, built with FastAPI and Python.

## Features

- 📰 **Multi-source aggregation** - Fetches articles from BBC, Al Jazeera, Foreign Policy, The Diplomat, and more
- 🌍 **Geographic filtering** - Browse by region (Americas, Europe, MENA, Asia-Pacific, Africa)
- 🏷️ **Topic categorization** - Filter by Conflicts, Diplomacy, Trade, Elections, Climate, Technology
- 🔍 **Full-text search** - Search across article titles and summaries
- 🌓 **Dark/Light mode** - Toggle theme preference
- ⏰ **Auto-refresh** - Background scheduler fetches new articles every 30 minutes
- 📱 **Responsive design** - Mobile-friendly interface

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy, APScheduler
- **Frontend**: Jinja2 Templates, Tailwind CSS
- **Database**: SQLite (development), PostgreSQL (production)
- **Deployment**: Docker, Gunicorn

## Quick Start

### Local Development

```bash
# Clone and navigate
cd geopolitics-news

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: .\venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Run development server
uvicorn app.main:app --reload --port 8000
```

Visit http://localhost:8000

### Docker

```bash
# Build and run
docker build -t geopolitics-news .
docker run -p 8000:8000 geopolitics-news

# Or use docker-compose
docker-compose up -d
```

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | Home page with articles |
| `GET /article/{id}` | Article detail page |
| `GET /about` | About page |
| `GET /api/articles/` | List articles (JSON) |
| `GET /api/articles/{id}` | Get article detail (JSON) |
| `GET /api/articles/categories/list` | List categories |
| `GET /api/articles/regions/list` | List regions |
| `GET /api/articles/sources/list` | List sources |
| `GET /health` | Health check |
| `GET /health/detailed` | Detailed health with stats |
| `POST /api/refresh` | Trigger feed refresh |

### Query Parameters

```
GET /api/articles/?category=conflicts&region=europe&search=ukraine&limit=20&offset=0
```

## Configuration

Environment variables (see `.env.example`):

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Enable debug mode | `false` |
| `DATABASE_URL` | Database connection string | `sqlite:///./geopolitics_news.db` |
| `FEED_UPDATE_INTERVAL` | Minutes between feed updates | `30` |
| `CACHE_TTL` | Cache TTL in seconds | `300` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `LOG_JSON` | Use JSON log format | `false` |
| `RATE_LIMIT_REQUESTS` | Requests per minute limit | `100` |

## News Sources

| Source | Type | Region Focus |
|--------|------|--------------|
| BBC World | RSS | Global |
| Al Jazeera | RSS | Global |
| France 24 | RSS | Global |
| DW News | RSS | Europe/Global |
| Foreign Policy | RSS | Analysis |
| The Diplomat | RSS | Asia-Pacific |
| Middle East Eye | RSS | MENA |
| POLITICO Europe | RSS | Europe |

## Project Structure

```
geopolitics-news/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI app & routes
│   ├── settings.py       # Pydantic settings
│   ├── database.py       # SQLAlchemy setup
│   ├── models.py         # Database models
│   ├── schemas.py        # Pydantic schemas
│   ├── services.py       # Business logic
│   ├── cache.py          # Caching layer
│   ├── middleware.py     # Security middleware
│   ├── exceptions.py     # Error handlers
│   ├── logging_config.py # Logging setup
│   ├── feeds/
│   │   ├── sources.py    # Feed configurations
│   │   └── rss_parser.py # RSS parsing
│   ├── routes/
│   │   └── articles.py   # API routes
│   └── templates/        # Jinja2 templates
├── static/               # Static assets
├── tests/                # Test suite
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Production Deployment

### Docker Compose (Recommended)

```bash
# Production with PostgreSQL
docker-compose -f docker-compose.yml up -d
```

### Manual Deployment

```bash
# Set production environment
export ENVIRONMENT=production
export DEBUG=false
export LOG_JSON=true

# Run with Gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `pytest`
5. Submit a pull request
