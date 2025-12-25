"""Configuration for news sources and RSS feeds."""

# RSS feeds organized by category/region
# Significantly expanded to ensure fresh content every day
RSS_FEEDS = {
    # Major Wire Services & Global News - Publish multiple times per hour
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
        {
            "name": "Reuters World",
            "feed_url": "https://www.reutersagency.com/feed/?best-regions=world&post_type=best",
            "url": "https://www.reuters.com/world/",
            "logo_url": "https://www.reuters.com/favicon.ico",
        },
        {
            "name": "Associated Press",
            "feed_url": "https://rsshub.app/apnews/topics/world-news",
            "url": "https://apnews.com/world-news",
            "logo_url": "https://apnews.com/favicon.ico",
        },
        {
            "name": "NPR World",
            "feed_url": "https://feeds.npr.org/1004/rss.xml",
            "url": "https://www.npr.org/sections/world/",
            "logo_url": "https://www.npr.org/favicon.ico",
        },
        {
            "name": "The Guardian World",
            "feed_url": "https://www.theguardian.com/world/rss",
            "url": "https://www.theguardian.com/world",
            "logo_url": "https://www.theguardian.com/favicon.ico",
        },
        {
            "name": "ABC News International",
            "feed_url": "https://abcnews.go.com/abcnews/internationalheadlines",
            "url": "https://abcnews.go.com/International",
            "logo_url": "https://abcnews.go.com/favicon.ico",
        },
        {
            "name": "CBS News World",
            "feed_url": "https://www.cbsnews.com/latest/rss/world",
            "url": "https://www.cbsnews.com/world/",
            "logo_url": "https://www.cbsnews.com/favicon.ico",
        },
        {
            "name": "Euronews",
            "feed_url": "https://www.euronews.com/rss?level=theme&name=news",
            "url": "https://www.euronews.com/news",
            "logo_url": "https://www.euronews.com/favicon.ico",
        },
    ],
    
    # Think Tanks & Analysis - In-depth geopolitical analysis
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
        {
            "name": "Council on Foreign Relations",
            "feed_url": "https://www.cfr.org/rss.xml",
            "url": "https://www.cfr.org",
            "logo_url": "https://www.cfr.org/favicon.ico",
        },
        {
            "name": "Brookings Institution",
            "feed_url": "https://www.brookings.edu/feed/",
            "url": "https://www.brookings.edu",
            "logo_url": "https://www.brookings.edu/favicon.ico",
        },
        {
            "name": "Carnegie Endowment",
            "feed_url": "https://carnegieendowment.org/rss/solr/?fa=recentPubs",
            "url": "https://carnegieendowment.org",
            "logo_url": "https://carnegieendowment.org/favicon.ico",
        },
        {
            "name": "RAND Corporation",
            "feed_url": "https://www.rand.org/news.xml",
            "url": "https://www.rand.org",
            "logo_url": "https://www.rand.org/favicon.ico",
        },
        {
            "name": "Atlantic Council",
            "feed_url": "https://www.atlanticcouncil.org/feed/",
            "url": "https://www.atlanticcouncil.org",
            "logo_url": "https://www.atlanticcouncil.org/favicon.ico",
        },
        {
            "name": "War on the Rocks",
            "feed_url": "https://warontherocks.com/feed/",
            "url": "https://warontherocks.com",
            "logo_url": "https://warontherocks.com/favicon.ico",
        },
        {
            "name": "Chatham House",
            "feed_url": "https://www.chathamhouse.org/rss.xml",
            "url": "https://www.chathamhouse.org",
            "logo_url": "https://www.chathamhouse.org/favicon.ico",
        },
    ],
    
    # Americas
    "americas": [
        {
            "name": "Washington Post World",
            "feed_url": "https://feeds.washingtonpost.com/rss/world",
            "url": "https://www.washingtonpost.com/world/",
            "logo_url": "https://www.washingtonpost.com/favicon.ico",
        },
        {
            "name": "New York Times World",
            "feed_url": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
            "url": "https://www.nytimes.com/section/world",
            "logo_url": "https://www.nytimes.com/favicon.ico",
        },
        {
            "name": "Americas Quarterly",
            "feed_url": "https://www.americasquarterly.org/feed/",
            "url": "https://www.americasquarterly.org",
            "logo_url": "https://www.americasquarterly.org/favicon.ico",
        },
        {
            "name": "The Hill",
            "feed_url": "https://thehill.com/feed/",
            "url": "https://thehill.com",
            "logo_url": "https://thehill.com/favicon.ico",
        },
        {
            "name": "Politico",
            "feed_url": "https://www.politico.com/rss/politicopicks.xml",
            "url": "https://www.politico.com",
            "logo_url": "https://www.politico.com/favicon.ico",
        },
        {
            "name": "Defense News",
            "feed_url": "https://www.defensenews.com/arc/outboundfeeds/rss/?outputType=xml",
            "url": "https://www.defensenews.com",
            "logo_url": "https://www.defensenews.com/favicon.ico",
        },
    ],
    
    # Asia-Pacific - Comprehensive Asian coverage
    "asia": [
        {
            "name": "South China Morning Post",
            "feed_url": "https://www.scmp.com/rss/91/feed",
            "url": "https://www.scmp.com",
            "logo_url": "https://www.scmp.com/favicon.ico",
        },
        {
            "name": "Nikkei Asia",
            "feed_url": "https://asia.nikkei.com/rss/feed/nar",
            "url": "https://asia.nikkei.com",
            "logo_url": "https://asia.nikkei.com/favicon.ico",
        },
        {
            "name": "The Japan Times",
            "feed_url": "https://www.japantimes.co.jp/feed/",
            "url": "https://www.japantimes.co.jp",
            "logo_url": "https://www.japantimes.co.jp/favicon.ico",
        },
        {
            "name": "Korea Herald",
            "feed_url": "http://www.koreaherald.com/rss/020100000000.xml",
            "url": "https://www.koreaherald.com",
            "logo_url": "https://www.koreaherald.com/favicon.ico",
        },
        {
            "name": "Channel News Asia",
            "feed_url": "https://www.channelnewsasia.com/api/v1/rss-outbound-feed?_format=xml&category=6511",
            "url": "https://www.channelnewsasia.com/asia",
            "logo_url": "https://www.channelnewsasia.com/favicon.ico",
        },
        {
            "name": "The Hindu",
            "feed_url": "https://www.thehindu.com/news/international/feeder/default.rss",
            "url": "https://www.thehindu.com/news/international/",
            "logo_url": "https://www.thehindu.com/favicon.ico",
        },
        {
            "name": "Times of India World",
            "feed_url": "https://timesofindia.indiatimes.com/rssfeeds/296589292.cms",
            "url": "https://timesofindia.indiatimes.com/world",
            "logo_url": "https://timesofindia.indiatimes.com/favicon.ico",
        },
        {
            "name": "Australian Broadcasting Corp",
            "feed_url": "https://www.abc.net.au/news/feed/51120/rss.xml",
            "url": "https://www.abc.net.au/news/world/",
            "logo_url": "https://www.abc.net.au/favicon.ico",
        },
        {
            "name": "Radio Free Asia",
            "feed_url": "https://www.rfa.org/english/rss2.xml",
            "url": "https://www.rfa.org/english/",
            "logo_url": "https://www.rfa.org/favicon.ico",
        },
        {
            "name": "The Straits Times",
            "feed_url": "https://www.straitstimes.com/news/asia/rss.xml",
            "url": "https://www.straitstimes.com/asia",
            "logo_url": "https://www.straitstimes.com/favicon.ico",
        },
    ],
    
    # Middle East & North Africa
    "middle_east": [
        {
            "name": "Middle East Eye",
            "feed_url": "https://www.middleeasteye.net/rss",
            "url": "https://www.middleeasteye.net",
            "logo_url": "https://www.middleeasteye.net/favicon.ico",
        },
        {
            "name": "Al-Monitor",
            "feed_url": "https://www.al-monitor.com/rss",
            "url": "https://www.al-monitor.com",
            "logo_url": "https://www.al-monitor.com/favicon.ico",
        },
        {
            "name": "Haaretz",
            "feed_url": "https://www.haaretz.com/srv/haaretz-latest-headlines",
            "url": "https://www.haaretz.com",
            "logo_url": "https://www.haaretz.com/favicon.ico",
        },
        {
            "name": "Times of Israel",
            "feed_url": "https://www.timesofisrael.com/feed/",
            "url": "https://www.timesofisrael.com",
            "logo_url": "https://www.timesofisrael.com/favicon.ico",
        },
        {
            "name": "Arab News",
            "feed_url": "https://www.arabnews.com/rss.xml",
            "url": "https://www.arabnews.com",
            "logo_url": "https://www.arabnews.com/favicon.ico",
        },
        {
            "name": "Tehran Times",
            "feed_url": "https://www.tehrantimes.com/rss",
            "url": "https://www.tehrantimes.com",
            "logo_url": "https://www.tehrantimes.com/favicon.ico",
        },
        {
            "name": "Daily Sabah",
            "feed_url": "https://www.dailysabah.com/rssFeed/news",
            "url": "https://www.dailysabah.com",
            "logo_url": "https://www.dailysabah.com/favicon.ico",
        },
        {
            "name": "Egypt Independent",
            "feed_url": "https://egyptindependent.com/feed/",
            "url": "https://egyptindependent.com",
            "logo_url": "https://egyptindependent.com/favicon.ico",
        },
    ],
    
    # Europe
    "europe": [
        {
            "name": "POLITICO Europe",
            "feed_url": "https://www.politico.eu/feed/",
            "url": "https://www.politico.eu",
            "logo_url": "https://www.politico.eu/favicon.ico",
        },
        {
            "name": "The Moscow Times",
            "feed_url": "https://www.themoscowtimes.com/rss/news",
            "url": "https://www.themoscowtimes.com",
            "logo_url": "https://www.themoscowtimes.com/favicon.ico",
        },
        {
            "name": "Kyiv Independent",
            "feed_url": "https://kyivindependent.com/feed/",
            "url": "https://kyivindependent.com",
            "logo_url": "https://kyivindependent.com/favicon.ico",
        },
        {
            "name": "EUobserver",
            "feed_url": "https://euobserver.com/rss.xml",
            "url": "https://euobserver.com",
            "logo_url": "https://euobserver.com/favicon.ico",
        },
        {
            "name": "Der Spiegel International",
            "feed_url": "https://www.spiegel.de/international/index.rss",
            "url": "https://www.spiegel.de/international/",
            "logo_url": "https://www.spiegel.de/favicon.ico",
        },
        {
            "name": "The Local Europe",
            "feed_url": "https://www.thelocal.com/tag/europe/feed/",
            "url": "https://www.thelocal.com",
            "logo_url": "https://www.thelocal.com/favicon.ico",
        },
        {
            "name": "Radio Free Europe",
            "feed_url": "https://www.rferl.org/api/",
            "url": "https://www.rferl.org",
            "logo_url": "https://www.rferl.org/favicon.ico",
        },
        {
            "name": "The Irish Times World",
            "feed_url": "https://www.irishtimes.com/cmlink/news-world-1.1319295",
            "url": "https://www.irishtimes.com/world",
            "logo_url": "https://www.irishtimes.com/favicon.ico",
        },
        {
            "name": "Balkan Insight",
            "feed_url": "https://balkaninsight.com/feed/",
            "url": "https://balkaninsight.com",
            "logo_url": "https://balkaninsight.com/favicon.ico",
        },
    ],
    
    # Africa
    "africa": [
        {
            "name": "AllAfrica",
            "feed_url": "https://allafrica.com/tools/headlines/rdf/latest/headlines.rdf",
            "url": "https://allafrica.com",
            "logo_url": "https://allafrica.com/favicon.ico",
        },
        {
            "name": "The Africa Report",
            "feed_url": "https://www.theafricareport.com/feed/",
            "url": "https://www.theafricareport.com",
            "logo_url": "https://www.theafricareport.com/favicon.ico",
        },
        {
            "name": "News24 Africa",
            "feed_url": "https://feeds.news24.com/articles/news24/Africa/rss",
            "url": "https://www.news24.com/news24/africa",
            "logo_url": "https://www.news24.com/favicon.ico",
        },
        {
            "name": "Premium Times Nigeria",
            "feed_url": "https://www.premiumtimesng.com/feed",
            "url": "https://www.premiumtimesng.com",
            "logo_url": "https://www.premiumtimesng.com/favicon.ico",
        },
        {
            "name": "Daily Maverick",
            "feed_url": "https://www.dailymaverick.co.za/feed/",
            "url": "https://www.dailymaverick.co.za",
            "logo_url": "https://www.dailymaverick.co.za/favicon.ico",
        },
        {
            "name": "Nation Africa",
            "feed_url": "https://nation.africa/service/rss/feeds/news.rss",
            "url": "https://nation.africa",
            "logo_url": "https://nation.africa/favicon.ico",
        },
    ],
    
    # Security & Defense
    "security": [
        {
            "name": "Jane's Defence",
            "feed_url": "https://www.janes.com/feeds/news",
            "url": "https://www.janes.com",
            "logo_url": "https://www.janes.com/favicon.ico",
        },
        {
            "name": "Defense One",
            "feed_url": "https://www.defenseone.com/rss/all/",
            "url": "https://www.defenseone.com",
            "logo_url": "https://www.defenseone.com/favicon.ico",
        },
        {
            "name": "Breaking Defense",
            "feed_url": "https://breakingdefense.com/feed/",
            "url": "https://breakingdefense.com",
            "logo_url": "https://breakingdefense.com/favicon.ico",
        },
        {
            "name": "The War Zone",
            "feed_url": "https://www.thedrive.com/the-war-zone/feed",
            "url": "https://www.thedrive.com/the-war-zone",
            "logo_url": "https://www.thedrive.com/favicon.ico",
        },
        {
            "name": "Military Times",
            "feed_url": "https://www.militarytimes.com/arc/outboundfeeds/rss/?outputType=xml",
            "url": "https://www.militarytimes.com",
            "logo_url": "https://www.militarytimes.com/favicon.ico",
        },
    ],
    
    # Economics & Trade
    "economics": [
        {
            "name": "Financial Times World",
            "feed_url": "https://www.ft.com/world?format=rss",
            "url": "https://www.ft.com/world",
            "logo_url": "https://www.ft.com/favicon.ico",
        },
        {
            "name": "The Economist",
            "feed_url": "https://www.economist.com/international/rss.xml",
            "url": "https://www.economist.com/international/",
            "logo_url": "https://www.economist.com/favicon.ico",
        },
        {
            "name": "Bloomberg Politics",
            "feed_url": "https://feeds.bloomberg.com/politics/news.rss",
            "url": "https://www.bloomberg.com/politics",
            "logo_url": "https://www.bloomberg.com/favicon.ico",
        },
        {
            "name": "CNBC World",
            "feed_url": "https://www.cnbc.com/id/100727362/device/rss/rss.html",
            "url": "https://www.cnbc.com/world/",
            "logo_url": "https://www.cnbc.com/favicon.ico",
        },
    ],
    
    # Climate & Energy Geopolitics
    "climate_energy": [
        {
            "name": "Climate Home News",
            "feed_url": "https://www.climatechangenews.com/feed/",
            "url": "https://www.climatechangenews.com",
            "logo_url": "https://www.climatechangenews.com/favicon.ico",
        },
        {
            "name": "Carbon Brief",
            "feed_url": "https://www.carbonbrief.org/feed/",
            "url": "https://www.carbonbrief.org",
            "logo_url": "https://www.carbonbrief.org/favicon.ico",
        },
        {
            "name": "Oil Price",
            "feed_url": "https://oilprice.com/rss/main",
            "url": "https://oilprice.com",
            "logo_url": "https://oilprice.com/favicon.ico",
        },
        {
            "name": "Energy Intelligence",
            "feed_url": "https://www.energyintel.com/rss",
            "url": "https://www.energyintel.com",
            "logo_url": "https://www.energyintel.com/favicon.ico",
        },
    ],
    
    # Technology & Cyber
    "technology": [
        {
            "name": "Wired Security",
            "feed_url": "https://www.wired.com/feed/category/security/latest/rss",
            "url": "https://www.wired.com/category/security/",
            "logo_url": "https://www.wired.com/favicon.ico",
        },
        {
            "name": "The Record",
            "feed_url": "https://therecord.media/feed/",
            "url": "https://therecord.media",
            "logo_url": "https://therecord.media/favicon.ico",
        },
        {
            "name": "CyberScoop",
            "feed_url": "https://cyberscoop.com/feed/",
            "url": "https://cyberscoop.com",
            "logo_url": "https://cyberscoop.com/favicon.ico",
        },
        {
            "name": "Protocol",
            "feed_url": "https://www.protocol.com/feeds/feed.rss",
            "url": "https://www.protocol.com",
            "logo_url": "https://www.protocol.com/favicon.ico",
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
