"""RSS feed parser for fetching articles from various sources."""
import feedparser
import httpx
import asyncio
from datetime import datetime
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
import re

from .sources import RSS_FEEDS, CATEGORY_KEYWORDS, REGION_KEYWORDS


# Global stats for monitoring
_fetch_stats = {"success": 0, "failed": 0, "articles": 0}


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
            "%a, %d %b %Y %H:%M:%S %Z",
            "%Y-%m-%dT%H:%M:%S%z",
            "%Y-%m-%dT%H:%M:%SZ",
            "%Y-%m-%dT%H:%M:%S.%f%z",
            "%Y-%m-%d %H:%M:%S",
            "%d %b %Y %H:%M:%S %z",
            "%Y-%m-%d",
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
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'application/rss+xml, application/xml, text/xml, application/atom+xml, */*',
                    'Accept-Language': 'en-US,en;q=0.9',
                }
            )
            response.raise_for_status()
            return feedparser.parse(response.text)
    except httpx.TimeoutException:
        print(f"Timeout fetching feed {feed_url}")
        return None
    except httpx.HTTPStatusError as e:
        print(f"HTTP error fetching feed {feed_url}: {e.response.status_code}")
        return None
    except Exception as e:
        print(f"Error fetching feed {feed_url}: {e}")
        return None


async def fetch_single_source(feed_config: dict) -> List[Dict]:
    """Fetch articles from a single source."""
    feed = await fetch_feed(feed_config['feed_url'])
    if feed:
        articles = parse_feed_entries(feed, feed_config['name'])
        if articles:
            _fetch_stats["success"] += 1
            _fetch_stats["articles"] += len(articles)
            print(f"✓ Fetched {len(articles)} articles from {feed_config['name']}")
            return articles
    _fetch_stats["failed"] += 1
    print(f"✗ Failed to fetch from {feed_config['name']}")
    return []


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


async def fetch_all_feeds(max_concurrent: int = 10) -> List[Dict]:
    """Fetch articles from all configured RSS feeds concurrently."""
    global _fetch_stats
    _fetch_stats = {"success": 0, "failed": 0, "articles": 0}
    
    all_articles = []
    all_feed_configs = []
    
    # Collect all feed configurations
    for category, feeds in RSS_FEEDS.items():
        for feed_config in feeds:
            all_feed_configs.append(feed_config)
    
    print(f"\n📡 Fetching from {len(all_feed_configs)} sources...")
    
    # Use semaphore to limit concurrent requests
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def fetch_with_semaphore(feed_config):
        async with semaphore:
            return await fetch_single_source(feed_config)
    
    # Fetch all feeds concurrently
    tasks = [fetch_with_semaphore(config) for config in all_feed_configs]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Collect results
    for result in results:
        if isinstance(result, list):
            all_articles.extend(result)
        elif isinstance(result, Exception):
            print(f"Task error: {result}")
    
    print(f"\n📊 Fetch complete: {_fetch_stats['success']} sources successful, {_fetch_stats['failed']} failed")
    print(f"📰 Total articles fetched: {len(all_articles)}")
    
    return all_articles


def get_fetch_stats() -> Dict:
    """Get the latest fetch statistics."""
    return _fetch_stats.copy()
