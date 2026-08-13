"""
Twilio caller - places phone calls with audio digest.
"""

import logging
from typing import Optional
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse

logger = logging.getLogger(__name__)


class PhoneCaller:
    """Places phone calls using Twilio."""
    
    def __init__(self, account_sid: str, auth_token: str, from_number: str):
        self.client = Client(account_sid, auth_token)
        self.from_number = from_number
    
    def call_with_audio(self, to_number: str, audio_url: str) -> Optional[str]:
        """
        Call a number and play audio file.
        
        Args:
            to_number: Phone number to call (e.g., "+1234567890")
            audio_url: URL to audio file (must be publicly accessible)
        
        Returns:
            Call SID if successful, None if failed
        """
        logger.info(f"Placing call to {to_number}...")
        
        try:
            # Create TwiML response
            response = VoiceResponse()
            response.say("Good morning. Here is your AI digest for today.")
            response.play(audio_url)
            response.say("End of briefing. Have a great day.")
            response.hangup()
            
            # Place call
            call = self.client.calls.create(
                to=to_number,
                from_=self.from_number,
                twiml=str(response)
            )
            
            logger.info(f"✓ Call placed: {call.sid}")
            return call.sid
            
        except Exception as e:
            logger.error(f"✗ Call failed: {e}")
            return None
    
    def call_with_tts_url(self, to_number: str, audio_url: str) -> Optional[str]:
        """
        Alternative: call and stream audio from URL.
        """
        return self.call_with_audio(to_number, audio_url)
    
    def call_with_text(self, to_number: str, text: str) -> Optional[str]:
        """
        Call and have Twilio read text aloud.
        (Less natural than pre-recorded audio)
        """
        logger.info(f"Placing call to {to_number} (TTS voice)...")
        
        try:
            response = VoiceResponse()
            response.say(text)
            response.hangup()
            
            call = self.client.calls.create(
                to=to_number,
                from_=self.from_number,
                twiml=str(response)
            )
            
            logger.info(f"✓ Call placed: {call.sid}")
            return call.sid
            
        except Exception as e:
            logger.error(f"✗ Call failed: {e}")
            return None
    
    def hangup_call(self, call_sid: str) -> bool:
        """Hangup an active call."""
        try:
            self.client.calls(call_sid).update(status='completed')
            logger.info(f"✓ Call {call_sid} ended")
            return True
        except Exception as e:
            logger.error(f"✗ Could not hangup {call_sid}: {e}")
            return False


class MockPhoneCaller(PhoneCaller):
    """Mock caller for testing (doesn't actually call)."""
    
    def __init__(self):
        pass
    
    def call_with_audio(self, to_number: str, audio_url: str) -> Optional[str]:
        """Simulate call without actually calling."""
        logger.info(f"[MOCK] Would call {to_number} with audio: {audio_url}")
        return "MOCK_CALL_SID_123456"
    
    def call_with_text(self, to_number: str, text: str) -> Optional[str]:
        """Simulate call without actually calling."""
        logger.info(f"[MOCK] Would call {to_number} and say: {text[:50]}...")
        return "MOCK_CALL_SID_123456"


if __name__ == "__main__":
    # Test: python -m src.caller
    import os
    from config.settings import get_settings
    
    logging.basicConfig(level=logging.INFO)
    
    settings = get_settings()
    
    caller = PhoneCaller(
        account_sid=settings.twilio_account_sid,
        auth_token=settings.twilio_auth_token,
        from_number=settings.twilio_phone_number
    )
    
    # Test with mock text call
    call_sid = caller.call_with_text(
        to_number=settings.your_cell_number,
        text="Hello. This is a test call from your AI digest service. Goodbye."
    )
    
    if call_sid:
        print(f"\n✓ Test call successful! SID: {call_sid}")
    else:
        print("\n✗ Test call failed. Check your credentials.")
