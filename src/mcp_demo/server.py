"""
MCP server implementation for Yle news RSS feeds.
"""
from typing import List
from pydantic import Field, BaseModel
import feedparser
import httpx
from datetime import datetime
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("yle-news")

# RSS feed URLs for different topics
RSS_FEEDS = {
    "news": "https://feeds.yle.fi/uutiset/v1/majorHeadlines/YLE_UUTISET.rss",
    "recent": "https://feeds.yle.fi/uutiset/v1/recent.rss?publisherIds=YLE_UUTISET",
    "most_read": "https://feeds.yle.fi/uutiset/v1/mostRead/YLE_UUTISET.rss",
    "kotimaa": "https://feeds.yle.fi/uutiset/v1/recent.rss?publisherIds=YLE_UUTISET&concepts=18-34837",
    "ulkomaat": "https://feeds.yle.fi/uutiset/v1/recent.rss?publisherIds=YLE_UUTISET&concepts=18-34953",
    "talous": "https://feeds.yle.fi/uutiset/v1/recent.rss?publisherIds=YLE_UUTISET&concepts=18-19274",
    "politiikka": "https://feeds.yle.fi/uutiset/v1/recent.rss?publisherIds=YLE_UUTISET&concepts=18-38033",
    "kulttuuri": "https://feeds.yle.fi/uutiset/v1/recent.rss?publisherIds=YLE_UUTISET&concepts=18-150067",
    "viihde": "https://feeds.yle.fi/uutiset/v1/recent.rss?publisherIds=YLE_UUTISET&concepts=18-36066",
    "tiede": "https://feeds.yle.fi/uutiset/v1/recent.rss?publisherIds=YLE_UUTISET&concepts=18-819",
    "luonto": "https://feeds.yle.fi/uutiset/v1/recent.rss?publisherIds=YLE_UUTISET&concepts=18-35354",
    "terveys": "https://feeds.yle.fi/uutiset/v1/recent.rss?publisherIds=YLE_UUTISET&concepts=18-35138",
    "media": "https://feeds.yle.fi/uutiset/v1/recent.rss?publisherIds=YLE_UUTISET&concepts=18-35057",
    "liikenne": "https://feeds.yle.fi/uutiset/v1/recent.rss?publisherIds=YLE_UUTISET&concepts=18-12",
    "näkökulmat": "https://feeds.yle.fi/uutiset/v1/recent.rss?publisherIds=YLE_UUTISET&concepts=18-35381",
    "urheilu": "https://feeds.yle.fi/uutiset/v1/recent.rss?publisherIds=YLE_URHEILU",
    "selkouutiset": "https://feeds.yle.fi/uutiset/v1/recent.rss?publisherIds=YLE_SELKOUUTISET",
    "english": "https://feeds.yle.fi/uutiset/v1/recent.rss?publisherIds=YLE_NEWS",
    "sapmi": "https://feeds.yle.fi/uutiset/v1/recent.rss?publisherIds=YLE_SAPMI",
    "novosti": "https://feeds.yle.fi/uutiset/v1/recent.rss?publisherIds=YLE_NOVOSTI",
    "karjalakse": "https://feeds.yle.fi/uutiset/v1/recent.rss?publisherIds=YLE_KARJALAKSE"
}

class NewsItem(BaseModel):
    """Model for a news item."""
    title: str
    published: str
    link: str
    summary: str
    published_parsed: datetime = Field(default=None, exclude=True)

class NewsResponse(BaseModel):
    """Model for the news response."""
    items: List[NewsItem]
    topic: str
    count: int

async def fetch_feed(url: str) -> feedparser.FeedParserDict:
    """Fetch and parse an RSS feed."""
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return feedparser.parse(response.content)

def parse_news_item(entry: feedparser.FeedParserDict) -> NewsItem:
    """Parse a feed entry into a NewsItem."""
    published_parsed = None
    if hasattr(entry, 'published_parsed'):
        published_parsed = datetime(*entry.published_parsed[:6])
    
    return NewsItem(
        title=entry.get('title', 'No title'),
        published=entry.get('published', 'No date'),
        link=entry.get('link', 'No link'),
        summary=entry.get('summary', 'No summary'),
        published_parsed=published_parsed
    )

@mcp.tool()
async def get_news(
    topic: str = Field(
        description="The news topic to fetch. Available topics: news, recent, most_read, kotimaa, ulkomaat, talous, politiikka, kulttuuri, viihde, tiede, luonto, terveys, media, liikenne, näkökulmat, urheilu, selkouutiset, english, sapmi, novosti, karjalakse",
        default="news"
    ),
    limit: int = Field(
        description="Maximum number of news items to fetch",
        default=5
    )
) -> NewsResponse:
    """
    Fetch news from Yle RSS feeds for a specific topic.
    
    Args:
        topic: The news topic to fetch
        limit: Maximum number of news items to return
        
    Returns:
        NewsResponse containing the news items sorted by publication date (newest first)
    """
    if topic not in RSS_FEEDS:
        raise ValueError(f"Invalid topic: {topic}. Available topics: {', '.join(RSS_FEEDS.keys())}")
    
    try:
        feed = await fetch_feed(RSS_FEEDS[topic])
        if not feed.entries:
            return NewsResponse(items=[], topic=topic, count=0)
        
        # Parse all items and sort by publication date
        items = [parse_news_item(entry) for entry in feed.entries]
        items.sort(key=lambda x: x.published_parsed or datetime.min, reverse=True)
        
        # Apply limit after sorting
        if limit > 0:
            items = items[:limit]
        
        return NewsResponse(
            items=items,
            topic=topic,
            count=len(items)
        )
    except Exception as e:
        raise Exception(f"Error fetching news: {str(e)}")

def run_server():
    """Run the MCP server."""
    mcp.run(transport='stdio') 