"""
News sources for AI digest.
Add or remove RSS feeds here.
"""

NEWS_SOURCES = {
    "Anthropic": {
        "url": "https://www.anthropic.com/news/feed.xml",
        "priority": 1,
        "max_items": 3
    },
    "OpenAI": {
        "url": "https://openai.com/blog/feed.rss",
        "priority": 1,
        "max_items": 3
    },
    "HuggingFace": {
        "url": "https://huggingface.co/feed/papers",
        "priority": 2,
        "max_items": 2,
        "keywords": ["efficient", "inference", "production", "llm"]
    },
    "Google DeepMind": {
        "url": "https://blog.google/feed/",
        "priority": 2,
        "max_items": 2,
        "keywords": ["gemini", "inference", "ai"]
    },
}

"""
How to add a new source:

1. Find the RSS feed URL for your news source
2. Add to NEWS_SOURCES dict:

    "Source Name": {
        "url": "https://example.com/feed.xml",
        "priority": 1,  # 1 = always include, 2 = secondary
        "max_items": 3,  # How many articles to fetch
        "keywords": ["optional", "filter", "keywords"]  # Optional
    }

3. Save and test:
   python -m src.main --list-sources

Common AI news sources:
- Anthropic: https://www.anthropic.com/news/feed.xml
- OpenAI: https://openai.com/blog/feed.rss
- HuggingFace: https://huggingface.co/feed/papers
- Google AI: https://blog.google/feed/
- DeepMind: https://deepmind.google/feed.xml
"""
