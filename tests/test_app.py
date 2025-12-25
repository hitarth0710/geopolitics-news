"""Tests for the geopolitics news application."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app.models import Article, Source, Category, Region


# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def client():
    """Create test client with test database."""
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    """Create database session for testing."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


class TestHealthEndpoints:
    """Test health check endpoints."""
    
    def test_health_check(self, client):
        """Test basic health check returns 200."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
    
    def test_detailed_health_check(self, client):
        """Test detailed health check returns component status."""
        response = client.get("/health/detailed")
        assert response.status_code == 200
        data = response.json()
        assert "database" in data
        assert "scheduler" in data
        assert "total_articles" in data


class TestArticleAPI:
    """Test article API endpoints."""
    
    def test_get_articles_empty(self, client):
        """Test getting articles when database is empty."""
        response = client.get("/api/articles/")
        assert response.status_code == 200
        data = response.json()
        assert "articles" in data
        assert "total" in data
    
    def test_get_articles_with_filters(self, client):
        """Test article filtering parameters."""
        response = client.get("/api/articles/?limit=10&offset=0")
        assert response.status_code == 200
        data = response.json()
        assert data["limit"] == 10
        assert data["offset"] == 0
    
    def test_get_categories(self, client):
        """Test getting categories list."""
        response = client.get("/api/articles/categories/list")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_regions(self, client):
        """Test getting regions list."""
        response = client.get("/api/articles/regions/list")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_sources(self, client):
        """Test getting sources list."""
        response = client.get("/api/articles/sources/list")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


class TestPageRoutes:
    """Test HTML page routes."""
    
    def test_home_page(self, client):
        """Test home page renders."""
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
    
    def test_home_page_with_search(self, client):
        """Test home page with search parameter."""
        response = client.get("/?search=test")
        assert response.status_code == 200
    
    def test_home_page_with_category(self, client):
        """Test home page with category filter."""
        response = client.get("/?category=conflicts")
        assert response.status_code == 200
    
    def test_home_page_pagination(self, client):
        """Test home page pagination."""
        response = client.get("/?page=1")
        assert response.status_code == 200
    
    def test_about_page(self, client):
        """Test about page renders."""
        response = client.get("/about")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
    
    def test_article_not_found(self, client):
        """Test 404 for non-existent article."""
        response = client.get("/article/99999")
        assert response.status_code == 404


class TestModels:
    """Test database models."""
    
    def test_create_source(self, db_session):
        """Test creating a source."""
        source = Source(
            name="Test Source",
            url="https://test.com",
            feed_url="https://test.com/feed",
            is_active=True
        )
        db_session.add(source)
        db_session.commit()
        
        assert source.id is not None
        assert source.name == "Test Source"
    
    def test_create_category(self, db_session):
        """Test creating a category."""
        category = Category(
            name="Test Category",
            slug="test-category",
            icon="🧪"
        )
        db_session.add(category)
        db_session.commit()
        
        assert category.id is not None
        assert category.slug == "test-category"
    
    def test_create_article(self, db_session):
        """Test creating an article."""
        article = Article(
            title="Test Article",
            url="https://test.com/article",
            summary="This is a test article."
        )
        db_session.add(article)
        db_session.commit()
        
        assert article.id is not None
        assert article.title == "Test Article"


class TestCaching:
    """Test caching functionality."""
    
    @pytest.mark.asyncio
    async def test_cache_set_get(self):
        """Test setting and getting cached values."""
        from app.cache import cache
        
        await cache.set("test_key", "test_value", ttl=60)
        value = await cache.get("test_key")
        assert value == "test_value"
    
    @pytest.mark.asyncio
    async def test_cache_delete(self):
        """Test deleting cached values."""
        from app.cache import cache
        
        await cache.set("delete_key", "value")
        await cache.delete("delete_key")
        value = await cache.get("delete_key")
        assert value is None
    
    @pytest.mark.asyncio
    async def test_cache_clear(self):
        """Test clearing all cached values."""
        from app.cache import cache
        
        await cache.set("key1", "value1")
        await cache.set("key2", "value2")
        await cache.clear()
        assert cache.size == 0
