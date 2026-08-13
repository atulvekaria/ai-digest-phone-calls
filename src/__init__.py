"""
AI Digest Phone Calls - Automated voice briefings of latest AI news
"""

__version__ = "1.0.0"
__author__ = "Your Name"

from src.news_scraper import NewsScraper
from src.digest_generator import DigestGenerator
from src.tts_converter import TTSConverter
from src.caller import PhoneCaller

__all__ = [
    "NewsScraper",
    "DigestGenerator",
    "TTSConverter",
    "PhoneCaller",
]
