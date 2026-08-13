"""
News scraper - fetches latest AI news from RSS feeds.
"""

import feedparser
import logging
from typing import List, Dict, Optional
from datetime import datetime
from config.news_sources import NEWS_SOURCES

logger = logging.getLogger(__name__)


class NewsItem:
    """Represents a single news article."""
    
    def __init__(self, title: str, source: str, summary: str, link: str):
        self.title = title
        self.source = source
        self.summary = summary
        self.link = link
        self.published = datetime.now().isoformat()
    
    def __repr__(self):
        return f"{self.source}: {self.title[:60]}..."


class NewsScraper:
    """Fetches and aggregates AI news from multiple RSS feeds."""
    
    def __init__(self, sources: Dict = None):
        self.sources = sources or NEWS_SOURCES
        self.all_news: List[NewsItem] = []
    
    def fetch_all(self) -> List[NewsItem]:
        """Fetch news from all configured sources."""
        self.all_news = []
        
        logger.info(f"Fetching from {len(self.sources)} sources...")
        
        for source_name, config in self.sources.items():
            try:
                items = self._fetch_source(source_name, config)
                self.all_news.extend(items)
                logger.info(f"✓ {source_name}: {len(items)} items")
            except Exception as e:
                logger.warning(f"✗ {source_name}: {e}")
        
        logger.info(f"Total: {len(self.all_news)} items fetched")
        return self.all_news
    
    def _fetch_source(self, source_name: str, config: Dict) -> List[NewsItem]:
        """Fetch from single RSS source."""
        feed_url = config.get("url")
        max_items = config.get("max_items", 3)
        keywords = config.get("keywords", [])
        
        feed = feedparser.parse(feed_url)
        items = []
        
        for entry in feed.entries[:max_items]:
            # Check keywords filter if present
            if keywords:
                title_lower = entry.get("title", "").lower()
                summary_lower = entry.get("summary", "").lower()
                
                if not any(kw.lower() in title_lower or kw.lower() in summary_lower 
                          for kw in keywords):
                    continue
            
            item = NewsItem(
                title=entry.get("title", "No title"),
                source=source_name,
                summary=entry.get("summary", "")[:300],
                link=entry.get("link", "")
            )
            items.append(item)
        
        return items
    
    def format_for_digest(self) -> str:
        """Format news items into text for Claude digest generation."""
        if not self.all_news:
            return "No news found today."
        
        formatted = "## Today's AI News\n\n"
        
        for idx, item in enumerate(self.all_news, 1):
            formatted += f"{idx}. **{item.source}**: {item.title}\n"
            if item.summary:
                formatted += f"   Summary: {item.summary}\n"
            formatted += "\n"
        
        return formatted
    
    def list_sources(self) -> None:
        """Print all configured news sources."""
        print("\n📰 Configured News Sources:\n")
        for name, config in self.sources.items():
            print(f"  • {name}")
            print(f"    URL: {config.get('url')}")
            print(f"    Priority: {config.get('priority')}")
            print(f"    Max items: {config.get('max_items')}")
            if config.get("keywords"):
                print(f"    Keywords: {config.get('keywords')}")
            print()


if __name__ == "__main__":
    # Test: python -m src.news_scraper
    logging.basicConfig(level=logging.INFO)
    
    scraper = NewsScraper()
    news = scraper.fetch_all()
    
    print("\n" + scraper.format_for_digest())
