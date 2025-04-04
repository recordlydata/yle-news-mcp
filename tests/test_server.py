"""
Tests for the MCP server implementation.
"""
import pytest
from datetime import datetime
from mcp_demo.server import get_news, RSS_FEEDS, NewsResponse, NewsItem

@pytest.mark.asyncio
async def test_get_news_valid_topic():
    """Test fetching news for a valid topic."""
    result = await get_news(topic="news", limit=2)
    
    # Verify we got a NewsResponse
    assert isinstance(result, NewsResponse)
    assert result.topic == "news"
    assert result.count > 0
    assert len(result.items) == result.count
    
    # Verify each item is a NewsItem with the expected fields
    for item in result.items:
        assert isinstance(item, NewsItem)
        assert item.title
        assert item.published
        assert item.link
        assert item.summary

@pytest.mark.asyncio
async def test_get_news_invalid_topic():
    """Test fetching news for an invalid topic."""
    with pytest.raises(ValueError) as exc_info:
        await get_news(topic="invalid_topic")
    assert "Invalid topic" in str(exc_info.value)
    assert "Available topics" in str(exc_info.value)

@pytest.mark.asyncio
async def test_get_news_limit():
    """Test the limit parameter."""
    limit = 3
    result = await get_news(topic="news", limit=limit)
    assert result.count == limit
    assert len(result.items) == limit

@pytest.mark.asyncio
async def test_get_news_all_topics():
    """Test fetching news for all available topics."""
    for topic in RSS_FEEDS.keys():
        result = await get_news(topic=topic, limit=1)
        assert isinstance(result, NewsResponse)
        assert result.topic == topic
        assert result.count > 0

@pytest.mark.asyncio
async def test_get_news_sorted_by_date():
    """Test that news items are sorted by publication date in descending order."""
    result = await get_news(topic="news", limit=5)
    
    # Verify we have at least 2 items to compare
    assert len(result.items) >= 2
    
    # Check that items are sorted by publication date (newest first)
    for i in range(len(result.items) - 1):
        current_date = result.items[i].published_parsed
        next_date = result.items[i + 1].published_parsed
        
        # If both dates are available, verify they're in descending order
        if current_date is not None and next_date is not None:
            assert current_date >= next_date, f"Items not sorted correctly: {current_date} < {next_date}"
