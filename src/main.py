"""
Main orchestration script.
Coordinates: scraping → digest generation → TTS → phone call.
"""

import sys
import argparse
import logging
import schedule
import time
from datetime import datetime
from pathlib import Path

# Import modules
from config.settings import get_settings
from config.news_sources import NEWS_SOURCES
from src.news_scraper import NewsScraper
from src.digest_generator import DigestGenerator
from src.tts_converter import TTSConverter
from src.caller import PhoneCaller

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AIDigestService:
    """Main service that orchestrates daily AI digest."""
    
    def __init__(self):
        logger.info("🚀 Initializing AI Digest Service...")
        
        self.settings = get_settings()
        self.scraper = NewsScraper(NEWS_SOURCES)
        self.digest_gen = DigestGenerator(
            api_key=self.settings.openai_api_key,
            model=self.settings.claude_model
        )
        self.tts = TTSConverter(
            api_key=self.settings.openai_api_key,
            voice=self.settings.openai_tts_voice,
            model=self.settings.openai_tts_model
        )
        self.caller = PhoneCaller(
            account_sid=self.settings.twilio_account_sid,
            auth_token=self.settings.twilio_auth_token,
            from_number=self.settings.twilio_phone_number
        )
    
    def run_digest(self) -> bool:
        """Run full digest pipeline: scrape → generate → call."""
        logger.info("=" * 70)
        logger.info(f"📱 Generating Daily AI Digest - {datetime.now()}")
        logger.info("=" * 70)
        
        try:
            # Step 1: Scrape news
            logger.info("\n1️⃣  Scraping AI news...")
            news_items = self.scraper.fetch_all()
            
            if not news_items:
                logger.warning("   No news found today!")
                return False
            
            news_text = self.scraper.format_for_digest()
            
            # Step 2: Generate digest
            logger.info("\n2️⃣  Generating digest via Claude...")
            digest = self.digest_gen.generate(news_text)
            
            # Validate digest structure
            if not self.digest_gen.validate_digest(digest):
                logger.warning("   ⚠️  Digest validation failed")
            
            # Step 3: Convert to speech
            logger.info("\n3️⃣  Converting to speech...")
            audio_file = self.tts.convert(digest)
            
            # Step 4: Place call
            logger.info("\n4️⃣  Placing phone call...")
            
            # For local testing: use text call (Twilio reads it)
            # For production: upload audio to S3 and use audio URL
            call_sid = self.caller.call_with_text(
                to_number=self.settings.your_cell_number,
                text=digest
            )
            
            if call_sid:
                logger.info(f"\n✅ SUCCESS! Call placed: {call_sid}")
                logger.info(f"   Call to: {self.settings.your_cell_number}")
                logger.info(f"   Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                return True
            else:
                logger.error("\n❌ Call failed!")
                return False
                
        except Exception as e:
            logger.error(f"\n❌ Error: {e}", exc_info=True)
            return False
    
    def start_scheduler(self):
        """Start background scheduler for daily digest."""
        call_time = self.settings.call_time
        
        logger.info(f"\n📅 Scheduler started")
        logger.info(f"   Time: {call_time} daily")
        logger.info(f"   To: {self.settings.your_cell_number}")
        logger.info(f"   Status: waiting for scheduled time...\n")
        
        # Schedule daily
        schedule.every().day.at(call_time).do(self.run_digest)
        
        # Keep running
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            logger.info("\n⏹️  Scheduler stopped by user")
    
    def show_config(self):
        """Display current configuration."""
        print("\n📋 Current Configuration:")
        print(f"   Twilio Number: {self.settings.twilio_phone_number}")
        print(f"   Your Cell: {self.settings.your_cell_number}")
        print(f"   Call Time: {self.settings.call_time}")
        print(f"   TTS Voice: {self.settings.openai_tts_voice}")
        print(f"   Claude Model: {self.settings.claude_model}")
        print()
    
    def list_sources(self):
        """List configured news sources."""
        self.scraper.list_sources()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Daily AI Digest - Automated morning briefings"
    )
    parser.add_argument(
        "command",
        nargs="?",
        default="schedule",
        choices=["test", "schedule", "show-config", "list-sources"],
        help="Command to run"
    )
    
    args = parser.parse_args()
    
    service = AIDigestService()
    
    if args.command == "test":
        # Run digest once, immediately
        logger.info("🧪 TEST MODE - Running digest now")
        success = service.run_digest()
        sys.exit(0 if success else 1)
    
    elif args.command == "schedule":
        # Start daily scheduler
        service.start_scheduler()
    
    elif args.command == "show-config":
        # Show configuration
        service.show_config()
    
    elif args.command == "list-sources":
        # List news sources
        service.list_sources()


if __name__ == "__main__":
    main()
