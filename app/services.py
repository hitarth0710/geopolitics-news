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
    if not articles:
        return 0

    # Pre-fetch all existing article URLs to avoid per-article duplicate checks
    existing_urls = {url for (url,) in db.query(Article.url).all()}

    # Pre-fetch lookup maps so each article doesn't issue individual queries
    sources_by_name = {s.name: s for s in db.query(Source).all()}
    categories_by_slug = {c.slug: c for c in db.query(Category).all()}
    regions_by_slug = {r.slug: r for r in db.query(Region).all()}

    new_articles = []
    for article_data in articles:
        url = article_data.get('url')
        if not url or url in existing_urls:
            continue

        source = sources_by_name.get(article_data.get('source_name'))
        category = categories_by_slug.get(article_data.get('category_slug'))
        region = regions_by_slug.get(article_data.get('region_slug'))

        article = Article(
            title=article_data['title'],
            url=url,
            summary=article_data.get('summary'),
            author=article_data.get('author'),
            published_at=article_data.get('published_at'),
            image_url=article_data.get('image_url'),
            source_id=source.id if source else None,
            category_id=category.id if category else None,
            region_id=region.id if region else None,
        )
        new_articles.append(article)
        # Track URL to avoid duplicates within the same batch
        existing_urls.add(url)

    if not new_articles:
        return 0

    try:
        db.bulk_save_objects(new_articles)
        db.commit()
    except IntegrityError:
        db.rollback()
        # Fallback: insert one by one to maximise how many are saved
        saved = 0
        for article in new_articles:
            try:
                db.add(article)
                db.commit()
                saved += 1
            except IntegrityError:
                db.rollback()
        return saved

    return len(new_articles)
