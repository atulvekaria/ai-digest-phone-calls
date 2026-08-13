"""
Configuration loader from environment variables.
"""

import os
from typing import Optional
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Application settings loaded from .env or environment variables."""
    
    # Twilio
    twilio_account_sid: str = Field(..., alias="TWILIO_ACCOUNT_SID")
    twilio_auth_token: str = Field(..., alias="TWILIO_AUTH_TOKEN")
    twilio_phone_number: str = Field(..., alias="TWILIO_PHONE_NUMBER")
    your_cell_number: str = Field(..., alias="YOUR_CELL_NUMBER")
    
    # OpenAI
    openai_api_key: str = Field(..., alias="OPENAI_API_KEY")
    claude_model: str = Field("claude-3-5-sonnet-20241022", alias="CLAUDE_MODEL")
    
    # TTS Voice
    openai_tts_voice: str = Field("onyx", alias="OPENAI_TTS_VOICE")
    openai_tts_model: str = Field("tts-1-hd", alias="OPENAI_TTS_MODEL")
    
    # Schedule
    call_time: str = Field("09:00", alias="CALL_TIME")
    call_every_day: bool = Field(True, alias="CALL_EVERY_DAY")
    
    # Debug
    debug: bool = Field(False, alias="DEBUG")
    log_level: str = Field("INFO", alias="LOG_LEVEL")
    keep_audio_files: bool = Field(False, alias="KEEP_AUDIO_FILES")
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        
    def validate(self) -> bool:
        """Validate all required settings are present."""
        required = [
            "twilio_account_sid",
            "twilio_auth_token",
            "twilio_phone_number",
            "your_cell_number",
            "openai_api_key"
        ]
        
        for field in required:
            if not getattr(self, field):
                raise ValueError(f"Missing required setting: {field}")
        
        return True


def get_settings() -> Settings:
    """Load and validate settings."""
    settings = Settings()
    settings.validate()
    return settings
