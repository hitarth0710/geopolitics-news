"""Configuration for news sources and RSS feeds."""

# RSS feeds organized by category/region
RSS_FEEDS = {
    # Major Wire Services & Global News
    "global": [
        {
            "name": "BBC World",
            "feed_url": "http://feeds.bbci.co.uk/news/world/rss.xml",
            "url": "https://www.bbc.com/news/world",
            "logo_url": "https://news.bbcimg.co.uk/nol/shared/img/bbc_news_120x60.gif",
        },
        {
            "name": "Al Jazeera",
            "feed_url": "https://www.aljazeera.com/xml/rss/all.xml",
            "url": "https://www.aljazeera.com",
            "logo_url": "https://www.aljazeera.com/images/logo_aje.png",
        },
        {
            "name": "France 24",
            "feed_url": "https://www.france24.com/en/rss",
            "url": "https://www.france24.com/en/",
            "logo_url": "https://www.france24.com/favicon.ico",
        },
        {
            "name": "DW News",
            "feed_url": "https://rss.dw.com/rdf/rss-en-world",
            "url": "https://www.dw.com/en/",
            "logo_url": "https://www.dw.com/favicon.ico",
        },
    ],
    
    # Think Tanks & Analysis
    "analysis": [
        {
            "name": "Foreign Policy",
            "feed_url": "https://foreignpolicy.com/feed/",
            "url": "https://foreignpolicy.com",
            "logo_url": "https://foreignpolicy.com/favicon.ico",
        },
        {
            "name": "The Diplomat",
            "feed_url": "https://thediplomat.com/feed/",
            "url": "https://thediplomat.com",
            "logo_url": "https://thediplomat.com/favicon.ico",
        },
    ],
    
    # Regional Sources
    "asia": [
        {
            "name": "South China Morning Post",
            "feed_url": "https://www.scmp.com/rss/91/feed",
            "url": "https://www.scmp.com",
            "logo_url": "https://www.scmp.com/favicon.ico",
        },
    ],
    "middle_east": [
        {
            "name": "Middle East Eye",
            "feed_url": "https://www.middleeasteye.net/rss",
            "url": "https://www.middleeasteye.net",
            "logo_url": "https://www.middleeasteye.net/favicon.ico",
        },
    ],
    "europe": [
        {
            "name": "POLITICO Europe",
            "feed_url": "https://www.politico.eu/feed/",
            "url": "https://www.politico.eu",
            "logo_url": "https://www.politico.eu/favicon.ico",
        },
    ],
}

# Categories for article classification
CATEGORIES = [
    {"name": "Conflicts & Security", "slug": "conflicts", "icon": "⚔️", "description": "Armed conflicts, military affairs, security"},
    {"name": "Diplomacy", "slug": "diplomacy", "icon": "🤝", "description": "International relations, treaties, summits"},
    {"name": "Trade & Economics", "slug": "trade", "icon": "💰", "description": "International trade, sanctions, economic policy"},
    {"name": "Elections & Governance", "slug": "elections", "icon": "🗳️", "description": "Elections, political transitions, governance"},
    {"name": "Climate & Energy", "slug": "climate", "icon": "🌡️", "description": "Climate politics, energy security, resources"},
    {"name": "Technology & Cyber", "slug": "technology", "icon": "🔐", "description": "Tech policy, cybersecurity, digital sovereignty"},
]

# Regions for geographic classification
REGIONS = [
    {"name": "Americas", "slug": "americas", "icon": "🌎"},
    {"name": "Europe", "slug": "europe", "icon": "🇪🇺"},
    {"name": "Middle East & North Africa", "slug": "mena", "icon": "🌍"},
    {"name": "Asia-Pacific", "slug": "asia-pacific", "icon": "🌏"},
    {"name": "Sub-Saharan Africa", "slug": "africa", "icon": "🌍"},
    {"name": "Global", "slug": "global", "icon": "🌐"},
]

# Keywords for auto-categorization
CATEGORY_KEYWORDS = {
    "conflicts": ["war", "military", "attack", "troops", "defense", "army", "weapons", "missile", "bomb", "conflict", "battle", "invasion"],
    "diplomacy": ["summit", "treaty", "ambassador", "diplomatic", "negotiations", "talks", "alliance", "relations", "foreign minister", "UN"],
    "trade": ["trade", "tariff", "sanctions", "economy", "export", "import", "economic", "investment", "market", "currency"],
    "elections": ["election", "vote", "democracy", "president", "parliament", "government", "political", "campaign", "referendum"],
    "climate": ["climate", "carbon", "emissions", "renewable", "energy", "oil", "gas", "environment", "green", "sustainability"],
    "technology": ["cyber", "technology", "AI", "artificial intelligence", "data", "privacy", "digital", "tech", "internet", "surveillance"],
}

REGION_KEYWORDS = {
    "americas": ["US", "USA", "United States", "America", "Canada", "Mexico", "Brazil", "Latin America", "Washington", "Biden", "Trump"],
    "europe": ["Europe", "EU", "European", "NATO", "Germany", "France", "UK", "Britain", "Brussels", "London", "Paris", "Berlin", "Ukraine", "Russia"],
    "mena": ["Middle East", "Israel", "Palestine", "Gaza", "Iran", "Saudi", "Syria", "Iraq", "Egypt", "Turkey", "Arab", "Gulf"],
    "asia-pacific": ["China", "Japan", "Korea", "India", "Taiwan", "Asia", "Pacific", "ASEAN", "Beijing", "Tokyo", "Southeast Asia", "Australia"],
    "africa": ["Africa", "African", "Nigeria", "South Africa", "Kenya", "Ethiopia", "Congo", "Sahel"],
}
