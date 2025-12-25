"""RSS feed parser for fetching articles from various sources."""
import feedparser
import httpx
from datetime import datetime
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
import re

from .sources import RSS_FEEDS, CATEGORY_KEYWORDS, REGION_KEYWORDS


def parse_date(date_str: Optional[str]) -> Optional[datetime]:
    """Parse various date formats from RSS feeds."""
    if not date_str:
        return None
    
    try:
        # feedparser usually provides a time struct
        if hasattr(date_str, 'tm_year'):
            return datetime(*date_str[:6])
        
        # Try common formats
        formats = [
            "%a, %d %b %Y %H:%M:%S %z",
            "%a, %d %b %Y %H:%M:%S GMT",
            "%Y-%m-%dT%H:%M:%S%z",
            "%Y-%m-%dT%H:%M:%SZ",
            "%Y-%m-%d %H:%M:%S",
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(str(date_str), fmt)
            except ValueError:
                continue
                
    except Exception:
        pass
    
    return None


def clean_html(html_content: str) -> str:
    """Remove HTML tags and clean up text."""
    if not html_content:
        return ""
    
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text(separator=' ')
    # Clean up whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:1000]  # Limit summary length


def extract_image_url(entry: dict) -> Optional[str]:
    """Extract image URL from RSS entry."""
    # Check media content
    if 'media_content' in entry and entry['media_content']:
        for media in entry['media_content']:
            if 'url' in media:
                return media['url']
    
    # Check media thumbnail
    if 'media_thumbnail' in entry and entry['media_thumbnail']:
        return entry['media_thumbnail'][0].get('url')
    
    # Check enclosures
    if 'enclosures' in entry and entry['enclosures']:
        for enc in entry['enclosures']:
            if enc.get('type', '').startswith('image'):
                return enc.get('url')
    
    # Try to extract from content
    content = entry.get('content', [{}])[0].get('value', '') or entry.get('summary', '')
    if content:
        soup = BeautifulSoup(content, 'html.parser')
        img = soup.find('img')
        if img and img.get('src'):
            return img['src']
    
    return None


def detect_category(title: str, summary: str) -> Optional[str]:
    """Auto-detect article category based on keywords."""
    text = f"{title} {summary}".lower()
    
    scores = {}
    for category, keywords in CATEGORY_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw.lower() in text)
        if score > 0:
            scores[category] = score
    
    if scores:
        return max(scores, key=scores.get)
    return None


def detect_region(title: str, summary: str) -> Optional[str]:
    """Auto-detect article region based on keywords."""
    text = f"{title} {summary}"
    
    scores = {}
    for region, keywords in REGION_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text)
        if score > 0:
            scores[region] = score
    
    if scores:
        return max(scores, key=scores.get)
    return "global"


async def fetch_feed(feed_url: str, timeout: int = 30) -> Optional[feedparser.FeedParserDict]:
    """Fetch and parse an RSS feed."""
    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(
                feed_url,
                timeout=timeout,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                }
            )
            response.raise_for_status()
            return feedparser.parse(response.text)
    except Exception as e:
        print(f"Error fetching feed {feed_url}: {e}")
        return None


def parse_feed_entries(feed: feedparser.FeedParserDict, source_name: str) -> List[Dict]:
    """Parse entries from a feed into article dictionaries."""
    articles = []
    
    for entry in feed.entries:
        title = entry.get('title', '')
        if not title:
            continue
            
        summary = clean_html(entry.get('summary', '') or entry.get('description', ''))
        
        article = {
            'title': title,
            'url': entry.get('link', ''),
            'summary': summary,
            'author': entry.get('author', ''),
            'published_at': parse_date(entry.get('published_parsed') or entry.get('updated_parsed')),
            'image_url': extract_image_url(entry),
            'source_name': source_name,
            'category_slug': detect_category(title, summary),
            'region_slug': detect_region(title, summary),
        }
        
        articles.append(article)
    
    return articles


async def fetch_all_feeds() -> List[Dict]:
    """Fetch articles from all configured RSS feeds."""
    all_articles = []
    
    for category, feeds in RSS_FEEDS.items():
        for feed_config in feeds:
            feed = await fetch_feed(feed_config['feed_url'])
            if feed:
                articles = parse_feed_entries(feed, feed_config['name'])
                all_articles.extend(articles)
                print(f"Fetched {len(articles)} articles from {feed_config['name']}")
    
    return all_articles
