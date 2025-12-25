"""Service for storing articles in the database."""
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Dict

from .models import Article, Source, Category, Region
from .feeds.sources import RSS_FEEDS, CATEGORIES, REGIONS


def init_sources(db: Session):
    """Initialize sources from configuration."""
    for category, feeds in RSS_FEEDS.items():
        for feed_config in feeds:
            existing = db.query(Source).filter(Source.name == feed_config['name']).first()
            if not existing:
                source = Source(
                    name=feed_config['name'],
                    url=feed_config['url'],
                    feed_url=feed_config['feed_url'],
                    logo_url=feed_config.get('logo_url'),
                    region=category,
                    is_active=True
                )
                db.add(source)
    db.commit()


def init_categories(db: Session):
    """Initialize categories from configuration."""
    for cat_config in CATEGORIES:
        existing = db.query(Category).filter(Category.slug == cat_config['slug']).first()
        if not existing:
            category = Category(
                name=cat_config['name'],
                slug=cat_config['slug'],
                icon=cat_config['icon'],
                description=cat_config.get('description')
            )
            db.add(category)
    db.commit()


def init_regions(db: Session):
    """Initialize regions from configuration."""
    for reg_config in REGIONS:
        existing = db.query(Region).filter(Region.slug == reg_config['slug']).first()
        if not existing:
            region = Region(
                name=reg_config['name'],
                slug=reg_config['slug'],
                icon=reg_config['icon']
            )
            db.add(region)
    db.commit()


def store_articles(db: Session, articles: List[Dict]) -> int:
    """Store articles in database, skipping duplicates. Returns count of new articles."""
    new_count = 0
    
    for article_data in articles:
        # Check if article already exists (by URL)
        existing = db.query(Article).filter(Article.url == article_data['url']).first()
        if existing:
            continue
        
        # Get source
        source = None
        if article_data.get('source_name'):
            source = db.query(Source).filter(Source.name == article_data['source_name']).first()
        
        # Get category
        category = None
        if article_data.get('category_slug'):
            category = db.query(Category).filter(Category.slug == article_data['category_slug']).first()
        
        # Get region
        region = None
        if article_data.get('region_slug'):
            region = db.query(Region).filter(Region.slug == article_data['region_slug']).first()
        
        # Create article
        article = Article(
            title=article_data['title'],
            url=article_data['url'],
            summary=article_data.get('summary'),
            author=article_data.get('author'),
            published_at=article_data.get('published_at'),
            image_url=article_data.get('image_url'),
            source_id=source.id if source else None,
            category_id=category.id if category else None,
            region_id=region.id if region else None,
        )
        
        try:
            db.add(article)
            db.commit()
            new_count += 1
        except IntegrityError:
            db.rollback()
            continue
    
    return new_count
