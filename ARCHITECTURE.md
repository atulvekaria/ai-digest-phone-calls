# 🏗️ System Architecture Deep Dive

Comprehensive guide to the technical architecture, design patterns, and system interactions.

---

## System Components Diagram

```
┌────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                    DAILY AI DIGEST PHONE CALLS SYSTEM                      │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │                          CONFIGURATION LAYER                        │  │
│  │  .env → config/settings.py → Settings(Pydantic)                    │  │
│  │  • Twilio credentials      • OpenAI API key                        │  │
│  │  • Phone numbers           • Schedule settings                      │  │
│  │  • TTS voice & model       • Debug flags                           │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                    ↓                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │                    ORCHESTRATION LAYER                             │  │
│  │  src/main.py → AIDigestService                                    │  │
│  │  • Coordinates pipeline              • Manages scheduler           │  │
│  │  • Error handling & logging          • CLI interface               │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│           │                  │                  │                  │       │
│     ┌─────┴──────┐    ┌──────┴──────┐   ┌──────┴──────┐   ┌──────┴──────┐ │
│     ↓            ↓    ↓             ↓   ↓             ↓   ↓             ↓ │
│  ┌──────────┐ ┌──────────────┐ ┌─────────────┐ ┌────────────┐           │ │
│  │  Scraper │→│    Digest    │→│   TTS       │→│  Caller    │           │ │
│  │  (RSS)   │ │  (Claude)    │ │  (OpenAI)   │ │  (Twilio)  │           │ │
│  └──────────┘ └──────────────┘ └─────────────┘ └────────────┘           │ │
│     ↓            ↓                ↓                ↓                      │ │
│  RSS Feeds    Claude API       OpenAI TTS      Twilio API                │ │
│                                                                            │ │
│  ┌──────────────────────────────────────────────────────────────────────┐ │
│  │                    EXTERNAL SERVICES                                │ │
│  │  • Anthropic, OpenAI, HuggingFace RSS feeds                        │ │
│  │  • Claude API (synthesis)                                          │ │
│  │  • OpenAI TTS API (voice generation)                              │ │
│  │  • Twilio API (phone calls)                                       │ │
│  └──────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## Detailed Module Interaction Diagram

```
                            ┌──────────────────┐
                            │  .env / Settings │
                            └────────┬──────────┘
                                     │
                        ┌────────────┼────────────┐
                        │            │            │
                   ┌────┴──┐    ┌────┴──┐    ┌───┴────┐
                   │Twilio │    │OpenAI │    │Schedule│
                   │Creds  │    │Keys   │    │Config  │
                   └────┬──┘    └────┬──┘    └───┬────┘
                        └────────────┼────────────┘
                                     │
                         ┌───────────┴───────────┐
                         │                       │
                    ┌────┴─────────┐      ┌─────┴──────┐
                    │ Settings obj │      │ NEWS_      │
                    │ (pydantic)   │      │ SOURCES    │
                    └────┬─────────┘      └─────┬──────┘
                         │                      │
    ┌────────────────────┴──────────┬───────────┴──────────┐
    │                               │                      │
    │                    ┌──────────┴────────┐             │
    │                    │ AIDigestService   │             │
    │                    │ (Orchestrator)    │             │
    │                    └──────────┬────────┘             │
    │                               │                      │
    │  ┌────────────────────────────┼────────────────────────────┐
    │  │                            │                             │
    │  ↓                            ↓                             ↓
    │ ┌──────────┐  ┌─────────┐  ┌──────────┐              ┌─────────┐
    │ │NewsScraper    Digest     TTS        │              │PhoneCaller
    │ │          │  │Generator │ │Converter │              │
    │ └────┬─────┘  └────┬─────┘ └────┬─────┘              └────┬────┘
    │      │             │            │                         │
    │      │             │            │                         │
    ├──────┼─────────────┼────────────┼─────────────────────────┤
    │      │             │            │                         │
    │      ↓             ↓            ↓                         ↓
    │  RSS Feeds    Claude API    OpenAI TTS          Twilio REST API
    │      │             │            │                         │
    │      └─────────────┼────────────┴─────────────────────────┘
    │                    │
    │              Data Flow:
    │              1. News items (RSS)
    │              2. News text (formatted)
    │              3. Digest text (Claude)
    │              4. Audio file path (TTS)
    │              5. Call SID (Twilio)
    │
    └────────────────────────────────────────────────────────────
```

---

## Data Structures & Flow

### NewsItem (Dataclass)
```python
class NewsItem:
    title: str          # "Claude 3.5 Sonnet Released"
    source: str         # "Anthropic"
    summary: str        # First 300 chars of article
    link: str           # URL to original article
    published: str      # ISO timestamp
```

### Processing Pipeline

```
STAGE 1: RAW NEWS
────────────────
RSS Feed Entry (dict)
  ├─ title: str
  ├─ summary: str
  ├─ link: str
  └─ published: datetime

        ↓ (NewsScraper._fetch_source)

STAGE 2: FILTERED NEWS
──────────────────────
NewsItem (object)
  ├─ title: "Claude 3.5 Sonnet Released"
  ├─ source: "Anthropic"
  ├─ summary: "New Claude model with..."
  ├─ link: "https://..."
  └─ published: "2026-08-13T09:00:00"

        ↓ (NewsScraper.format_for_digest)

STAGE 3: FORMATTED TEXT
───────────────────────
Markdown string:
  "## Today's AI News
   
   1. Anthropic: Claude 3.5 Sonnet Released
      Summary: New Claude model with...
   
   2. OpenAI: New API Endpoints
      Summary: ..."

        ↓ (DigestGenerator.generate)

STAGE 4: SYNTHESIZED DIGEST
───────────────────────────
Plain text (voice-ready):
  "CRITICAL
   Claude 3.5 Sonnet released today.
   Supports 200,000 token context.
   
   IMPORTANT
   New benchmarks show improvements.
   
   MONITOR
   Research paper on efficient inference.
   
   ACTION ITEMS
   Run benchmark with your use case."

        ↓ (TTSConverter.convert)

STAGE 5: AUDIO FILE
───────────────────
MP3 Audio file:
  Location: /tmp/ai_digest.mp3
  Size: ~2-3 MB
  Duration: 8-10 minutes
  Voice: onyx (or configured)

        ↓ (PhoneCaller.call_with_text)

STAGE 6: PHONE CALL
───────────────────
Twilio VoiceResponse (TwiML):
  <?xml version="1.0" encoding="UTF-8"?>
  <Response>
    <Say>Good morning. Here is your AI digest...</Say>
    <Say>[DIGEST TEXT]</Say>
    <Say>End of briefing. Have a great day.</Say>
    <Hangup/>
  </Response>

        ↓ (Twilio API)

STAGE 7: DELIVERED
──────────────────
Call SID: CA1234567890abcdef
Status: completed
Duration: 8:42 minutes
Your phone: rings at 9:00 AM
```

---

## Class Hierarchy & Relationships

```
┌─────────────────────────────────────────┐
│         AIDigestService                 │
│  ┌─────────────────────────────────────┐│
│  │ - settings: Settings                ││
│  │ - scraper: NewsScraper              ││
│  │ - digest_gen: DigestGenerator       ││
│  │ - tts: TTSConverter                 ││
│  │ - caller: PhoneCaller               ││
│  │                                     ││
│  │ + run_digest() → bool               ││
│  │ + start_scheduler() → None          ││
│  │ + show_config() → None              ││
│  │ + list_sources() → None             ││
│  └─────────────────────────────────────┘│
└─────────────────────────────────────────┘
         │         │        │        │
         │         │        │        │
    ┌────┴────┐ ┌──┴──┐ ┌───┴───┐ ┌─┴────────┐
    │          │ │     │ │       │ │          │
    ↓          ↓ ↓     ↓ ↓       ↓ ↓          ↓
    
┌──────────────┐  ┌──────────────┐  ┌────────────┐
│NewsScraper   │  │DigestGenerator   TTSConverter
│              │  │              │  │
│- sources     │  │- client      │  │- client
│- all_news    │  │- model       │  │- voice
│              │  │              │  │- model
│+ fetch_all() │  │+ generate()  │  │+ convert()
│+ _fetch_source  │+ _build_prompt   │+ list_voices()
│+ format_for_│  │+ validate_│  │
│  digest()    │  │  digest() │  │
│+ list_sources   └──────────────┘  └────────────┘
└──────────────┘

                  ┌─────────────────────┐
                  │ PhoneCaller         │
                  │                     │
                  │ - client: Twilio    │
                  │ - from_number       │
                  │                     │
                  │ + call_with_text()  │
                  │ + call_with_audio() │
                  │ + hangup_call()     │
                  └─────────────────────┘
                  
                  ┌─────────────────────┐
                  │ MockPhoneCaller     │
                  │ (for testing)       │
                  │                     │
                  │ + call_with_text()  │ (simulated)
                  │ + call_with_audio() │ (simulated)
                  └─────────────────────┘
```

---

## Execution Flow Diagram

### Flow 1: Test Mode (One-Time Execution)

```
START
  │
  ├─ Parse args: command="test"
  │
  ├─ AIDigestService.__init__()
  │   ├─ Load .env → Settings
  │   ├─ NewsScraper(NEWS_SOURCES)
  │   ├─ DigestGenerator(api_key, model)
  │   ├─ TTSConverter(api_key, voice, model)
  │   └─ PhoneCaller(sid, token, number)
  │
  ├─ service.run_digest()
  │   │
  │   ├─ Step 1: NewsScraper.fetch_all()
  │   │   ├─ For each source in NEWS_SOURCES:
  │   │   │   ├─ feedparser.parse(url)
  │   │   │   ├─ Filter by keywords (if configured)
  │   │   │   └─ Append NewsItems to list
  │   │   └─ Return List[NewsItem]
  │   │
  │   ├─ Step 2: scraper.format_for_digest()
  │   │   └─ Return markdown formatted string
  │   │
  │   ├─ Step 3: digest_gen.generate(news_text)
  │   │   ├─ Build prompt with constraints
  │   │   ├─ OpenAI.messages.create(...)
  │   │   └─ Return digest text
  │   │
  │   ├─ Step 4: digest_gen.validate_digest(digest)
  │   │   └─ Check for required sections
  │   │
  │   ├─ Step 5: tts.convert(digest)
  │   │   ├─ OpenAI.audio.speech.create(...)
  │   │   ├─ Save MP3 to /tmp/ai_digest.mp3
  │   │   └─ Return file path
  │   │
  │   └─ Step 6: caller.call_with_text(to_number, text)
  │       ├─ Create VoiceResponse (TwiML)
  │       ├─ Twilio.calls.create(...)
  │       └─ Return call SID or None
  │
  ├─ Log results
  │
  └─ Exit with code 0 (success) or 1 (failure)
```

### Flow 2: Scheduler Mode (Continuous)

```
START
  │
  ├─ Parse args: command="schedule"
  │
  ├─ AIDigestService.__init__()
  │   └─ (same as test mode)
  │
  ├─ service.start_scheduler()
  │   │
  │   ├─ schedule.every().day.at(CALL_TIME).do(run_digest)
  │   │
  │   ├─ INFINITE LOOP:
  │   │   ├─ While True:
  │   │   │   ├─ schedule.run_pending()
  │   │   │   │   ├─ If it's CALL_TIME:
  │   │   │   │   │   └─ Call run_digest() (see Flow 1 steps 1-6)
  │   │   │   │   └─ Else:
  │   │   │   │       └─ Do nothing
  │   │   │   │
  │   │   │   └─ time.sleep(60)  # Check every minute
  │   │   │
  │   │   └─ REPEAT next day
  │   │
  │   └─ (Ctrl+C to stop)
  │
  └─ NEVER exits (unless interrupted)
```

### Flow 3: Lambda Deployment

```
START (via CloudWatch Events)
  │
  ├─ AWS Lambda invokes lambda_handler(event, context)
  │
  ├─ Lambda environment loads .env vars
  │   (set via Lambda environment variables)
  │
  ├─ AIDigestService.__init__()
  │   └─ (same as test mode)
  │
  ├─ service.run_digest()
  │   └─ (same as Flow 1 steps 1-6)
  │
  ├─ Lambda returns:
  │   {
  │     "statusCode": 200,
  │     "body": "Digest call placed successfully"
  │   }
  │
  └─ Lambda execution completes
     (CloudWatch checks status, retries on failure)
```

---

## Configuration & Environment Loading

```
.env file (not in git)
  ├─ TWILIO_ACCOUNT_SID
  ├─ TWILIO_AUTH_TOKEN
  ├─ TWILIO_PHONE_NUMBER
  ├─ YOUR_CELL_NUMBER
  ├─ OPENAI_API_KEY
  ├─ CALL_TIME
  ├─ CALL_EVERY_DAY
  ├─ OPENAI_TTS_VOICE
  ├─ OPENAI_TTS_MODEL
  ├─ CLAUDE_MODEL
  ├─ DEBUG
  ├─ LOG_LEVEL
  └─ KEEP_AUDIO_FILES
      │
      ├─ python-dotenv loads .env
      │
      └─ config/settings.py (Pydantic)
          │
          ├─ Validates required fields
          ├─ Provides defaults for optional
          ├─ Type-checks all values
          └─ Returns Settings object
              │
              └─ AIDigestService uses settings
                 ├─ Pass to scraper
                 ├─ Pass to digest_gen
                 ├─ Pass to tts
                 └─ Pass to caller
```

---

## Error Handling Strategy

```
NewsScraper.fetch_all()
  └─ For each source:
     ├─ Try: feedparser.parse()
     └─ Except: Log warning, continue
     (Partial failures are OK)

DigestGenerator.generate()
  ├─ Try: OpenAI API call
  └─ Except: Log error, raise exception
     (Full pipeline stops)

TTSConverter.convert()
  ├─ Try: OpenAI API call + save file
  └─ Except: Log error, raise exception
     (Full pipeline stops)

PhoneCaller.call_with_text()
  ├─ Try: Twilio API call
  └─ Except: Log error, return None
     (run_digest returns False)

AIDigestService.run_digest()
  ├─ Try: Full pipeline
  └─ Except: Log full traceback, return False
     (Graceful failure, exit code 1)

AIDigestService.start_scheduler()
  └─ Catch KeyboardInterrupt for Ctrl+C
```

---

## API Integration Details

### OpenAI SDK Usage (Claude API)

```python
from openai import OpenAI

client = OpenAI(api_key="sk-...")  # API key loaded from .env

# Messages API (Claude)
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1500,
    messages=[
        {"role": "user", "content": "[SYSTEM PROMPT + NEWS]"}
    ]
)

digest = response.content[0].text

# TTS API (same client)
response = client.audio.speech.create(
    model="tts-1-hd",
    voice="onyx",
    input=digest_text
)

audio_content = response.content  # Binary MP3 data
```

### Twilio SDK Usage

```python
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse

client = Client(account_sid, auth_token)

# Create TwiML
response = VoiceResponse()
response.say("Good morning...")
response.say(digest_text)
response.hangup()

# Place call
call = client.calls.create(
    to="+1999888777",
    from_="+1234567890",
    twiml=str(response)
)

call_sid = call.sid  # Unique identifier
```

### Feedparser Usage (RSS)

```python
import feedparser

# Parse RSS feed
feed = feedparser.parse("https://example.com/feed.xml")

# Access entries
for entry in feed.entries[:3]:
    title = entry.get("title", "")
    summary = entry.get("summary", "")
    link = entry.get("link", "")
```

---

## Deployment Architecture

### Local Execution
```
Developer Laptop
  └─ python -m src.main test
     └─ Uses local .env
     └─ Calls your phone immediately
```

### AWS Lambda
```
AWS Account
  ├─ Lambda Function (ai-digest-caller)
  │  └─ Environment variables (.env)
  │
  ├─ CloudWatch Events Rule
  │  └─ Cron: 0 9 * * ? * (9 AM UTC daily)
  │
  └─ CloudWatch Logs
     └─ Logs for debugging
```

### Linux Cron
```
Linux Server
  ├─ /home/user/ai-digest-phone-calls/
  │  └─ .env (with credentials)
  │
  └─ crontab
     └─ 0 9 * * * python -m src.main test
```

### Heroku
```
Heroku Dyno
  ├─ Procfile: worker: python -m src.main schedule
  │
  ├─ Environment variables (.env equiv)
  │  └─ Config vars in dashboard
  │
  └─ Dyno runs 24/7 with scheduler
```

---

## Performance Characteristics

| Operation | Time | Bottleneck |
|-----------|------|-----------|
| RSS scraping (4 sources) | 2-3 sec | Network I/O |
| Claude API call | 1-3 sec | LLM processing |
| OpenAI TTS | 3-5 sec | Voice synthesis |
| Twilio call placement | 1 sec | API latency |
| **Total pipeline** | **7-12 sec** | Claude/TTS |

---

## Scaling Considerations

### Current Limits
- Single process (no parallelization)
- Handles 1 call per day
- No database (stateless)
- No caching

### Future Scaling
- Could parallelize RSS scraping
- Could batch multiple digests
- Could add caching for news
- Could add database for logs
- Could use message queue (SQS)

---

## Security & Best Practices

### Credential Management
✓ Secrets in .env (not in code)  
✓ Pydantic validation of all inputs  
✓ Environment variables in Lambda  
✓ No logging of credentials  

### API Safety
✓ Error handling for all API calls  
✓ Timeout handling (OpenAI, Twilio)  
✓ Rate limiting awareness  
✓ Graceful degradation  

### Code Quality
✓ Type hints (partial)  
✓ Logging at all levels  
✓ Validation of settings  
✓ Modular design  

---

## Testing Strategy

### Unit Tests (Could Be Added)
```python
# Test news scraper with mock feeds
# Test digest generator with fixed input
# Test TTS converter with mock API
# Test caller with MockPhoneCaller
```

### Integration Tests (Current)
```bash
python -m src.main test
  # Runs full pipeline once
  # Places real call (use after setup)
```

### Component Tests
```bash
python -m src.news_scraper
python -m src.digest_generator
python -m src.tts_converter
python -m src.caller
  # Each runs standalone
```

---

## Monitoring & Observability

### Logging
- Structured logs with timestamps
- Levels: DEBUG, INFO, WARNING, ERROR
- All modules log progress

### CloudWatch Integration (Lambda)
- Logs automatically captured
- Can set alarms on error rates
- Traceable via request ID

### Manual Monitoring
- Check logs for errors
- Monitor Twilio account for call status
- Check OpenAI usage for cost spikes
- Verify news sources still working

---

## Cost Optimization Tips

| Strategy | Savings | Trade-off |
|----------|---------|-----------|
| Use tts-1 instead of tts-1-hd | 50% on TTS | Slightly lower quality |
| Reduce max_items per source | Faster, less data | Fewer news items |
| Cache news (if modified) | Less API calls | Stale data possible |
| Use text call instead of audio | Simpler (no S3) | Less control over voice |
| Run at off-peak times | May save (if volume) | Not applicable (1 call/day) |

---

## Future Enhancement Ideas

1. **Email digest** - Send text version via email
2. **Slack notifications** - Post digest to Slack
3. **Web dashboard** - View past digests
4. **Database logging** - Track all calls
5. **Analytics** - Which news sources most mentioned
6. **Personalization** - Custom keywords per user
7. **Multiple calls** - Different recipients
8. **Digest versioning** - Track versions over time
9. **SMS alerts** - Send breaking news via SMS
10. **Voice feedback** - Option to rate digest quality

---

**This document provides a complete mental map of the system for future maintenance and enhancement.**

