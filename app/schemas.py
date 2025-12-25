"""Pydantic schemas for request/response validation."""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, HttpUrl


# ============= Base Schemas =============

class SourceBase(BaseModel):
    """Base source schema."""
    name: str
    url: str
    logo_url: Optional[str] = None


class CategoryBase(BaseModel):
    """Base category schema."""
    name: str
    slug: str
    icon: Optional[str] = None
    description: Optional[str] = None


class RegionBase(BaseModel):
    """Base region schema."""
    name: str
    slug: str
    icon: Optional[str] = None


# ============= Response Schemas =============

class SourceResponse(SourceBase):
    """Source response with article count."""
    id: int
    article_count: int = 0
    
    class Config:
        from_attributes = True


class CategoryResponse(CategoryBase):
    """Category response with article count."""
    id: int
    article_count: int = 0
    
    class Config:
        from_attributes = True


class RegionResponse(RegionBase):
    """Region response with article count."""
    id: int
    article_count: int = 0
    
    class Config:
        from_attributes = True


class ArticleSummary(BaseModel):
    """Article summary for list views."""
    id: int
    title: str
    url: str
    summary: Optional[str] = None
    image_url: Optional[str] = None
    author: Optional[str] = None
    published_at: Optional[datetime] = None
    source: Optional[SourceBase] = None
    category: Optional[CategoryBase] = None
    region: Optional[RegionBase] = None
    
    class Config:
        from_attributes = True


class ArticleDetail(ArticleSummary):
    """Full article detail."""
    content: Optional[str] = None
    fetched_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ArticleListResponse(BaseModel):
    """Paginated article list response."""
    total: int
    limit: int
    offset: int
    has_more: bool
    articles: List[ArticleSummary]


# ============= Request Schemas =============

class ArticleFilterParams(BaseModel):
    """Article filter parameters."""
    category: Optional[str] = Field(None, description="Filter by category slug")
    region: Optional[str] = Field(None, description="Filter by region slug")
    source: Optional[str] = Field(None, description="Filter by source name")
    search: Optional[str] = Field(None, description="Search in title/summary")
    limit: int = Field(20, ge=1, le=100, description="Number of articles to return")
    offset: int = Field(0, ge=0, description="Offset for pagination")


# ============= Health Check Schemas =============

class HealthStatus(BaseModel):
    """Health check status."""
    status: str
    environment: str
    version: str
    timestamp: datetime


class DetailedHealthStatus(HealthStatus):
    """Detailed health with component status."""
    database: str
    scheduler: str
    last_feed_update: Optional[datetime] = None
    total_articles: int
    total_sources: int


# ============= Stats Schemas =============

class AppStats(BaseModel):
    """Application statistics."""
    total_articles: int
    total_sources: int
    articles_today: int
    categories: List[CategoryResponse]
    regions: List[RegionResponse]
    top_sources: List[SourceResponse]
