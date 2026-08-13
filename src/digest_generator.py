"""
Digest generator - uses Claude to synthesize news into actionable digest.
"""

import logging
from openai import OpenAI

logger = logging.getLogger(__name__)


class DigestGenerator:
    """Uses Claude API to generate actionable AI digest."""
    
    def __init__(self, api_key: str, model: str = "claude-3-5-sonnet-20241022"):
        self.client = OpenAI(api_key=api_key)
        self.model = model
    
    def generate(self, news: str) -> str:
        """
        Generate digest from raw news text.
        Returns formatted digest ready for text-to-speech.
        """
        logger.info("Generating digest via Claude...")
        
        prompt = self._build_prompt(news)
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1500,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        digest = response.content[0].text
        logger.info("✓ Digest generated")
        
        return digest
    
    def _build_prompt(self, news: str) -> str:
        """Build the prompt for Claude."""
        return f"""You are an AI news briefer for a full-stack engineer building LLM products.

Synthesize this morning's AI news into a SHORT, ACTIONABLE digest for speaking aloud (8-10 minutes max).

IMPORTANT: Write ONLY for voice (spoken word, not reading). Use:
- Short sentences (max 15 words)
- Natural pauses indicated by dashes
- No URLs or email addresses
- No markdown formatting
- Expand acronyms on first use (LLM = Large Language Model)

Format your response EXACTLY like this (use these section headers):

CRITICAL
- [Any breaking API changes, deprecations, or outages]
- [Pricing changes affecting your product costs]

IMPORTANT
- [New model capability you should benchmark]
- [Speed improvement to evaluate]

MONITOR
- [Research paper worth reading later]
- [New tool worth trying]

ACTION ITEMS
- Test [specific thing] with [your use case]
- Evaluate [feature] by [date]

Keep each bullet to 1-2 sentences. Write for SPEAKING, not reading.

---

Today's News:
{news}

Now generate the digest (voice-ready, no markdown):"""
    
    def validate_digest(self, digest: str) -> bool:
        """Validate digest has expected structure."""
        required_sections = ["CRITICAL", "IMPORTANT", "MONITOR", "ACTION"]
        
        digest_upper = digest.upper()
        missing = [s for s in required_sections if s not in digest_upper]
        
        if missing:
            logger.warning(f"Missing sections: {missing}")
            return False
        
        return True


if __name__ == "__main__":
    # Test: python -m src.digest_generator
    import os
    from config.settings import get_settings
    from src.news_scraper import NewsScraper
    
    logging.basicConfig(level=logging.INFO)
    
    settings = get_settings()
    
    # Fetch news
    scraper = NewsScraper()
    scraper.fetch_all()
    news_text = scraper.format_for_digest()
    
    # Generate digest
    generator = DigestGenerator(api_key=settings.openai_api_key)
    digest = generator.generate(news_text)
    
    print("\n" + "="*60)
    print("GENERATED DIGEST:")
    print("="*60)
    print(digest)
    print("\n✓ Validation:", "PASS" if generator.validate_digest(digest) else "FAIL")
