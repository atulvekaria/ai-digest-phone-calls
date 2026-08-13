"""
Text-to-speech converter - converts digest to audio using OpenAI TTS API.
"""

import logging
import os
from pathlib import Path
from openai import OpenAI

logger = logging.getLogger(__name__)


class TTSConverter:
    """Converts text to speech using OpenAI TTS API."""
    
    VOICES = ["onyx", "nova", "shimmer", "echo", "fable"]
    MODELS = ["tts-1", "tts-1-hd"]
    
    def __init__(self, api_key: str, voice: str = "onyx", model: str = "tts-1-hd"):
        self.client = OpenAI(api_key=api_key)
        self.voice = voice
        self.model = model
        self.output_dir = Path("/tmp")
        
        if voice not in self.VOICES:
            logger.warning(f"Unknown voice '{voice}', using 'onyx'")
            self.voice = "onyx"
    
    def convert(self, text: str, output_file: str = "/tmp/ai_digest.mp3") -> str:
        """
        Convert text to speech.
        Returns path to audio file.
        """
        logger.info(f"Converting to speech ({self.voice}, {self.model})...")
        
        response = self.client.audio.speech.create(
            model=self.model,
            voice=self.voice,
            input=text
        )
        
        # Save audio file
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, "wb") as f:
            f.write(response.content)
        
        file_size_mb = os.path.getsize(output_file) / (1024 * 1024)
        logger.info(f"✓ Audio saved: {output_file} ({file_size_mb:.1f} MB)")
        
        return output_file
    
    @staticmethod
    def list_voices():
        """Print available voices."""
        print("\nAvailable TTS Voices:")
        print("  • onyx       (deep, clear)")
        print("  • nova       (bright, energetic)")
        print("  • shimmer    (warm, professional)")
        print("  • echo       (medium, neutral)")
        print("  • fable      (expressive, engaging)")


if __name__ == "__main__":
    # Test: python -m src.tts_converter
    import logging
    from config.settings import get_settings
    
    logging.basicConfig(level=logging.INFO)
    
    settings = get_settings()
    
    converter = TTSConverter(
        api_key=settings.openai_api_key,
        voice=settings.openai_tts_voice,
        model=settings.openai_tts_model
    )
    
    test_text = """
    Good morning. Here is your AI digest for today.
    
    CRITICAL: Claude API now supports two hundred thousand token context window.
    This means you can consolidate multiple API calls into one.
    
    IMPORTANT: New benchmarks show GPT-4o mini outperforms previous models on classification tasks.
    Consider running an A-B test on your current model.
    
    End of briefing. Have a great day.
    """
    
    audio_file = converter.convert(test_text)
    print(f"\n✓ Test audio saved to: {audio_file}")
    print("  To listen on Mac: open", audio_file)
