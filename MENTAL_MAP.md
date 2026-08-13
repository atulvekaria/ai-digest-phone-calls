# 🧠 AI Digest Phone Calls - Mental Map

A comprehensive visual and textual guide to the codebase architecture, data flow, and component interactions.

---

## 📊 System Architecture Overview

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                         AI DIGEST PHONE CALLS SYSTEM                          │
│                                                                                │
│  Scrape AI News → Synthesize Digest → Convert to Speech → Place Phone Call   │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow Pipeline

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 1: NEWS SCRAPING                                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Config: news_sources.py (RSS feed URLs + keywords)                         │
│      ↓                                                                       │
│  NewsScraper.fetch_all()  →  Hits 4 RSS feeds (Anthropic, OpenAI, etc)    │
│      ↓                                                                       │
│  Returns: List[NewsItem]  →  Each has: title, source, summary, link        │
│      ↓                                                                       │
│  Scraper.format_for_digest()  →  Formats as markdown for Claude           │
│      ↓                                                                       │
│  Output: "## Today's AI News\n\n1. Anthropic: New model released...\n..."  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 2: DIGEST SYNTHESIS (Claude LLM)                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Input: Raw news markdown                                                  │
│      ↓                                                                       │
│  DigestGenerator.generate()  →  Calls Claude API                           │
│      ↓                                                                       │
│  Prompt Engineering:                                                        │
│    • Restructures news into 4 sections: CRITICAL, IMPORTANT, MONITOR, ACTION │
│    • Optimizes for voice (short sentences, no URLs, expanded acronyms)      │
│    • Constraints: 8-10 minutes spoken duration, natural pauses             │
│      ↓                                                                       │
│  Claude Model: claude-3-5-sonnet-20241022                                  │
│      ↓                                                                       │
│  Output: Structured text digest (voice-ready, no markdown)                 │
│      ↓                                                                       │
│  Validation: Checks for required sections (CRITICAL, IMPORTANT, etc.)      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 3: TEXT-TO-SPEECH CONVERSION                                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Input: Digest text                                                         │
│      ↓                                                                       │
│  TTSConverter.convert()  →  Calls OpenAI TTS API                           │
│      ↓                                                                       │
│  Parameters:                                                                │
│    • Model: tts-1-hd (high quality) or tts-1 (fast)                       │
│    • Voice: onyx, nova, shimmer, echo, or fable                            │
│      ↓                                                                       │
│  OpenAI TTS Engine  →  Converts text to natural speech                     │
│      ↓                                                                       │
│  Output: MP3 audio file (~2-3 MB)                                          │
│  Saved to: /tmp/ai_digest.mp3                                              │
│      ↓                                                                       │
│  File validation: Logs file size                                            │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 4: PHONE CALL PLACEMENT                                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Input: Digest text or audio file                                          │
│      ↓                                                                       │
│  PhoneCaller.call_with_text()  →  Two methods available:                   │
│    • call_with_text(text)        - Twilio reads text aloud (lower quality) │
│    • call_with_audio(audio_url)  - Streams pre-recorded audio (better)     │
│      ↓                                                                       │
│  Current Method: call_with_text() (simpler, doesn't need S3)               │
│      ↓                                                                       │
│  Twilio API: Creates VoiceResponse (TwiML)                                 │
│    1. Say: "Good morning. Here is your AI digest for today."               │
│    2. Play or Say: Digest content                                          │
│    3. Say: "End of briefing. Have a great day."                            │
│    4. Hangup                                                                │
│      ↓                                                                       │
│  Call Details:                                                              │
│    • From: TWILIO_PHONE_NUMBER (your Twilio number)                        │
│    • To: YOUR_CELL_NUMBER (your personal cell)                             │
│    • Duration: 8-10 minutes                                                │
│      ↓                                                                       │
│  Output: Call SID (success) or error (failure)                             │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🏗️ Module Structure

### Core Application (`src/`)

```
src/
├── main.py (ORCHESTRATOR)
│   └── AIDigestService
│       ├── __init__()           - Instantiate all modules
│       ├── run_digest()         - Main pipeline (5 steps)
│       ├── start_scheduler()    - Daily scheduler loop
│       ├── show_config()        - Display settings
│       └── list_sources()       - List news sources
│
├── news_scraper.py (FETCHER)
│   ├── NewsItem (dataclass)
│   │   ├── title
│   │   ├── source
│   │   ├── summary
│   │   ├── link
│   │   └── published
│   │
│   └── NewsScraper (class)
│       ├── __init__(sources)
│       ├── fetch_all()           - Fetch from all RSS feeds
│       ├── _fetch_source()       - Fetch single RSS + filter by keywords
│       ├── format_for_digest()   - Markdown formatting
│       └── list_sources()        - Print sources
│
├── digest_generator.py (SYNTHESIZER)
│   └── DigestGenerator (class)
│       ├── __init__(api_key, model)
│       ├── generate(news)       - Call Claude API with prompt
│       ├── _build_prompt()      - Construct optimized prompt
│       └── validate_digest()    - Check for required sections
│
├── tts_converter.py (VOICE GENERATOR)
│   └── TTSConverter (class)
│       ├── __init__(api_key, voice, model)
│       ├── convert(text)        - Text → MP3 via OpenAI TTS
│       └── list_voices()        - Show available voices
│
└── caller.py (PHONE CALLER)
    ├── PhoneCaller (class)
    │   ├── __init__(account_sid, auth_token, from_number)
    │   ├── call_with_audio()    - Stream audio file URL
    │   ├── call_with_text()     - Twilio reads text
    │   └── hangup_call()        - End active call
    │
    └── MockPhoneCaller (test stub)
        └── Simulates calls without Twilio
```

### Configuration (`config/`)

```
config/
├── settings.py (ENVIRONMENT LOADER)
│   └── Settings (Pydantic BaseSettings)
│       ├── Twilio vars
│       ├── OpenAI vars
│       ├── Schedule vars
│       ├── Debug vars
│       └── validate()
│
└── news_sources.py (FEED CONFIGURATION)
    └── NEWS_SOURCES (dict)
        ├── "Anthropic" → {url, priority, max_items}
        ├── "OpenAI" → {url, priority, max_items}
        ├── "HuggingFace" → {url, priority, max_items, keywords}
        └── "Google DeepMind" → {url, priority, max_items, keywords}
```

### Deployment (`lambda/` + `deployment/`)

```
lambda/
└── lambda_handler.py
    └── lambda_handler(event, context)
        └── Calls AIDigestService.run_digest()
        └── Returns {statusCode, body}

deployment/
├── lambda_deploy.sh     - Build & deploy to AWS Lambda
├── cron_setup.sh        - Setup Linux cron job
└── Procfile             - Heroku dyno configuration
```

---

## 🔐 Configuration & Secrets

```
.env (NOT in git)
├── Twilio Credentials
│   ├── TWILIO_ACCOUNT_SID        - Account identifier
│   ├── TWILIO_AUTH_TOKEN         - Authentication secret
│   ├── TWILIO_PHONE_NUMBER       - Your Twilio number (outbound)
│   └── YOUR_CELL_NUMBER          - Your phone (inbound)
│
├── OpenAI Credentials
│   └── OPENAI_API_KEY            - API key (Claude + TTS)
│
├── Schedule Settings
│   ├── CALL_TIME                 - When to call (HH:MM, 24-hour)
│   └── CALL_EVERY_DAY            - true/false
│
├── TTS Settings
│   ├── OPENAI_TTS_VOICE          - Speaker voice
│   └── OPENAI_TTS_MODEL          - Quality level
│
├── LLM Settings
│   └── CLAUDE_MODEL              - Model ID
│
└── Debug Settings
    ├── DEBUG
    ├── LOG_LEVEL
    └── KEEP_AUDIO_FILES
```

---

## 🎯 Class Interactions

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         AIDigestService (main.py)                        │
│  THE ORCHESTRATOR - coordinates everything                             │
└─────────────────────────────────────────────────────────────────────────┘
                  │
        ┌─────────┼──────────┬──────────┐
        ↓         ↓          ↓          ↓
    ┌────────┐ ┌────────┐ ┌───────┐ ┌────────┐
    │Scraper │→│Digest  │→│ TTS   │→│Caller  │
    │(RSS)   │ │(LLM)   │ │(Voice)│ │(Phone) │
    └────────┘ └────────┘ └───────┘ └────────┘
        │         │        │          │
        ↓         ↓        ↓          ↓
    RSS Feeds  Claude   OpenAI    Twilio
               API      API       API
```

### Execution Flow

```
1. main.py launches
   └─→ Parse command line args: test | schedule | show-config | list-sources
   └─→ Instantiate AIDigestService()
       └─→ Load settings from .env via get_settings()
       └─→ Create NewsScraper(NEWS_SOURCES)
       └─→ Create DigestGenerator(api_key, model)
       └─→ Create TTSConverter(api_key, voice, model)
       └─→ Create PhoneCaller(twilio_sid, twilio_token, twilio_number)

2. If "test" command:
   └─→ Call service.run_digest() once
   └─→ Exit with status code

3. If "schedule" command:
   └─→ Call service.start_scheduler()
   └─→ Schedule daily job at CALL_TIME via APScheduler
   └─→ Keep running forever, checking schedule every 60 seconds

4. run_digest() pipeline:
   a. NewsScraper.fetch_all()
      └─→ For each feed: feedparser.parse(url)
      └─→ Filter entries by keywords (if configured)
      └─→ Return List[NewsItem]
   
   b. Scraper.format_for_digest()
      └─→ Format as markdown
   
   c. DigestGenerator.generate(news_text)
      └─→ Build prompt with constraints
      └─→ Call OpenAI().messages.create() (Claude API)
      └─→ Return digest text
   
   d. DigestGenerator.validate_digest()
      └─→ Check for required sections
   
   e. TTSConverter.convert(digest)
      └─→ Call OpenAI().audio.speech.create()
      └─→ Save MP3 to disk
      └─→ Return file path
   
   f. PhoneCaller.call_with_text()
      └─→ Create VoiceResponse (TwiML)
      └─→ Call Twilio API
      └─→ Return call SID
```

---

## 📋 Key Classes Deep Dive

### 1. **NewsScraper** (`src/news_scraper.py`)

**Purpose:** Fetch AI news from RSS feeds

**Key Methods:**
- `fetch_all()` - Scrapes all configured sources in parallel
- `_fetch_source(name, config)` - Single source scraper with keyword filtering
- `format_for_digest()` - Converts NewsItem list to markdown

**Data Structures:**
```python
NewsItem:
  - title: str
  - source: str (e.g., "Anthropic")
  - summary: str (first 300 chars)
  - link: str
  - published: ISO datetime

Config format:
{
  "SourceName": {
    "url": "https://...",
    "priority": 1,          # 1=critical, 2=secondary
    "max_items": 3,         # How many entries to fetch
    "keywords": ["optional"] # Filter entries
  }
}
```

**Behavior:**
- Fetches up to N items per source (configurable)
- Filters by keywords if present (title OR summary match)
- Logs success/failure per source
- Returns flattened list of all NewsItem objects

---

### 2. **DigestGenerator** (`src/digest_generator.py`)

**Purpose:** Synthesize news into actionable digest using Claude

**Key Methods:**
- `generate(news_text)` - Call Claude with optimized prompt
- `_build_prompt(news)` - Construct the system prompt
- `validate_digest(digest)` - Check structure

**Prompt Engineering:**
```
User sees:
  1. Role: "You are an AI news briefer for a full-stack engineer"
  2. Format: "Write ONLY for voice (spoken word, not reading)"
  3. Sections: CRITICAL / IMPORTANT / MONITOR / ACTION ITEMS
  4. Constraints:
     - Short sentences (max 15 words)
     - No URLs or markdown
     - Expand acronyms
     - Natural pauses with dashes
     - 8-10 minutes spoken duration
```

**Validation:**
- Checks for all 4 required sections in output
- Logs warning if sections missing
- Returns boolean (pass/fail)

---

### 3. **TTSConverter** (`src/tts_converter.py`)

**Purpose:** Convert text to natural speech via OpenAI TTS

**Key Methods:**
- `convert(text, output_file)` - Text → MP3
- `list_voices()` - Show available voices

**Voices Available:**
- **onyx** - Deep, clear (default)
- **nova** - Bright, energetic
- **shimmer** - Warm, professional
- **echo** - Medium, neutral
- **fable** - Expressive, engaging

**Models Available:**
- **tts-1** - Faster, lower latency
- **tts-1-hd** - Better quality (default)

**Output:**
- Saves MP3 to `/tmp/ai_digest.mp3`
- Returns file path
- Logs file size

---

### 4. **PhoneCaller** (`src/caller.py`)

**Purpose:** Place phone calls via Twilio

**Key Methods:**
- `call_with_text(to_number, text)` - Twilio reads text aloud
- `call_with_audio(to_number, audio_url)` - Streams audio file
- `hangup_call(call_sid)` - End call

**TwiML Response Structure:**
```
<Response>
  <Say>Good morning. Here is your AI digest for today.</Say>
  <Say>[DIGEST TEXT]</Say>
  <Say>End of briefing. Have a great day.</Say>
  <Hangup/>
</Response>
```

**Call Flow:**
1. Create VoiceResponse object
2. Add TwiML instructions (Say/Play/Hangup)
3. Call Twilio API with TwiML
4. Return call SID (unique identifier)

**Error Handling:**
- Returns None if call fails
- Logs exception details

---

### 5. **AIDigestService** (`src/main.py`)

**Purpose:** Orchestrate the entire pipeline

**Key Methods:**
- `__init__()` - Initialize all modules
- `run_digest()` - Execute full pipeline once
- `start_scheduler()` - Run daily at scheduled time
- `show_config()` - Display current settings
- `list_sources()` - Show configured news sources

**Scheduler Details:**
- Uses `schedule` library (pure Python)
- Checks every 60 seconds if it's time to run
- Blocks indefinitely (good for cron, Heroku, Lambda)

**Exit Codes:**
- 0 = Success
- 1 = Failure

---

## 🔗 External API Integrations

### RSS Feeds
```
NewsScraper → feedparser.parse(url)
  ├── Anthropic: https://www.anthropic.com/news/feed.xml
  ├── OpenAI: https://openai.com/blog/feed.rss
  ├── HuggingFace: https://huggingface.co/feed/papers
  └── Google DeepMind: https://blog.google/feed/
```

### Claude API (OpenAI SDK)
```
DigestGenerator → OpenAI(api_key).messages.create()
  ├── Model: claude-3-5-sonnet-20241022
  ├── Max tokens: 1500
  ├── Temperature: default (0.7)
  └── Input: formatted news + prompt
```

### OpenAI TTS API
```
TTSConverter → OpenAI(api_key).audio.speech.create()
  ├── Model: tts-1 or tts-1-hd
  ├── Voice: onyx/nova/shimmer/echo/fable
  └── Output: MP3 audio stream
```

### Twilio API
```
PhoneCaller → Client(account_sid, auth_token).calls.create()
  ├── From: TWILIO_PHONE_NUMBER
  ├── To: YOUR_CELL_NUMBER
  ├── TwiML: VoiceResponse (Say/Play/Hangup)
  └── Returns: Call object with SID
```

---

## 🚀 Deployment Paths

### 1. Local Testing
```
.env (with credentials)
  ↓
python -m src.main test
  ├─ Load .env via config/settings.py
  ├─ Instantiate AIDigestService
  ├─ Call run_digest() once
  ├─ Place call to YOUR_CELL_NUMBER
  └─ Exit
```

### 2. Local Scheduler (Development)
```
python -m src.main schedule
  ├─ Loads settings
  ├─ Starts scheduler
  ├─ Waits for CALL_TIME
  ├─ Runs run_digest()
  └─ Sleeps, repeats tomorrow
```

### 3. AWS Lambda (Production)
```
lambda/lambda_handler.py
  ├─ Triggered by CloudWatch Events (cron)
  ├─ Calls AIDigestService.run_digest()
  ├─ Returns {statusCode, body}
  └─ Lambda environment has .env vars

CloudWatch Rule:
  cron(0 9 * * ? *)  →  9 AM UTC daily
```

### 4. Linux Cron (Production)
```
crontab:
  0 9 * * * python -m src.main test
  ├─ Runs at 9 AM daily
  ├─ Executes run_digest() once
  ├─ Email output to crontab user
  └─ Exit

Setup: ./deployment/cron_setup.sh
```

### 5. Heroku (Production)
```
Procfile: worker: python -m src.main schedule
  ├─ Dyno runs scheduler 24/7
  ├─ Waits for CALL_TIME
  ├─ Runs run_digest() at scheduled time
  └─ Repeats daily

Deployment: git push heroku main
```

---

## 🧪 Testing Strategy

### Unit Tests (By Module)
```
python -m src.news_scraper
  → Fetch and format news

python -m src.digest_generator
  → Generate digest from sample news

python -m src.tts_converter
  → Convert sample text to audio

python -m src.caller
  → Simulate call (mock) or test call (real)
```

### Integration Test
```
python -m src.main test
  → Full pipeline: scrape → digest → tts → call
  → Places real call to YOUR_CELL_NUMBER
  → Best for before deploying
```

### Configuration Test
```
python -m src.main show-config
  → Display all loaded settings
  → Verify .env was read correctly

python -m src.main list-sources
  → Display configured news sources
  → Verify NEWS_SOURCES config
```

---

## 📊 Metrics & Monitoring

### What Gets Logged
```
✓ News fetch: # items per source
✓ Digest generation: token count, duration
✓ TTS conversion: file size, duration
✓ Call placement: call SID, success/failure
✓ Errors: full stack traces
```

### Log Format
```
%(asctime)s - %(name)s - %(levelname)s - %(message)s
2026-08-13 09:00:15 - src.main - INFO - 📱 Generating Daily AI Digest
2026-08-13 09:00:16 - src.news_scraper - INFO - ✓ Anthropic: 3 items
```

### Monitoring Points
- Call success rate (should be ~100%)
- Cost per month (should be ~$3)
- Digest quality (subjective, check daily)
- News source freshness (check headlines)

---

## 🎓 How to Modify The System

### To Add a News Source
1. Edit `config/news_sources.py`
2. Add entry with URL, priority, max_items, keywords
3. Test: `python -m src.main list-sources`

### To Change Call Time
1. Edit `.env`: `CALL_TIME=08:30`
2. Restart scheduler or wait for next scheduled time

### To Change Voice
1. Edit `.env`: `OPENAI_TTS_VOICE=shimmer`
2. Restart or run test: `python -m src.main test`

### To Modify Digest Format
1. Edit `src/digest_generator.py` → `_build_prompt()`
2. Change section headers or constraints
3. Test: `python -m src.main test`

### To Change Deployment Target
- Local: Just run python command
- Lambda: Edit CloudWatch rule
- Cron: Edit crontab
- Heroku: Edit Procfile or dyno settings

---

## 🔍 Debug Tips

### Enable Verbose Logging
```bash
DEBUG=true LOG_LEVEL=DEBUG python -m src.main test
```

### Keep Audio Files
```bash
KEEP_AUDIO_FILES=true python -m src.main test
# Saves to /tmp/ai_digest.mp3
```

### Test Individual Modules
```bash
# News scraper
python -m src.news_scraper

# Digest generator
python -m src.digest_generator

# TTS converter
python -m src.tts_converter

# Caller
python -m src.caller
```

### Mock Call (No Twilio)
```python
from src.caller import MockPhoneCaller
caller = MockPhoneCaller()
call_sid = caller.call_with_text("...", "...")
# Returns mock SID, doesn't actually call
```

---

## 📈 Cost Breakdown

| Service | Component | Cost | Notes |
|---------|-----------|------|-------|
| Twilio | call_with_text() | $0.02/call | ~1 call/day = $0.60/mo |
| OpenAI | Claude API | $0.03/digest | ~1/day = $0.90/mo |
| OpenAI | TTS conversion | $0.015/digest | ~1/day = $0.45/mo |
| AWS Lambda | compute + storage | $0.20/mo | Free tier includes 1M requests |
| AWS S3 | audio hosting (optional) | $0.50/mo | Only if using audio files |
| **Total** | | **~$3.00/mo** | Minimal cost |

---

## 🎯 Key Design Decisions

| Decision | Why | Trade-offs |
|----------|-----|-----------|
| RSS feeds for news | Reliable, no auth needed | Limited to public feeds |
| Claude (OpenAI SDK) | Best reasoning, cheap | API latency (1-3 sec) |
| OpenAI TTS | Natural voice, multiple options | Cost, no offline option |
| Twilio calls | Simple, reliable | Requires phone number |
| `schedule` lib | Pure Python, no dependencies | Not distributed, single-process |
| Voice-ready format | Natural speech delivery | Can't use markdown, special chars |
| Scheduler in Python | Flexible, easy testing | Must keep dyno running (Heroku) |
| Text call vs audio file | Simpler (no S3 needed) | Less flexible, Twilio does TTS |

---

## 🔐 Security Considerations

### Secrets Management
- Never commit `.env` (in `.gitignore`)
- Use environment variables in production
- Rotate API keys regularly
- Lambda: Use IAM roles, not hardcoded keys

### API Key Handling
- OpenAI: Keep in `.env`, never log
- Twilio: Keep in `.env`, never log
- All via `config/settings.py` (Pydantic validation)

### Data Privacy
- News data: Public feeds, no sensitive data
- Call data: Your own phone number
- Twilio: Manages call logs (check their privacy policy)

---

## 📚 Related Documentation

- **README.md** - Project overview and quick start
- **PROJECT_STRUCTURE.md** - File-by-file breakdown
- **QUICK_REFERENCE.md** - Common commands
- **docs/SETUP.md** - Step-by-step setup guide
- **docs/DEPLOYMENT.md** - Deployment options
- **docs/TROUBLESHOOTING.md** - Common issues

---

## 🤔 Mental Map Summary

**High Level:**
1. Scrape RSS feeds for AI news
2. Use Claude to synthesize into digest
3. Convert text to natural speech
4. Call your phone and read it aloud
5. Repeat daily at scheduled time

**Components:**
- `config/` - Secrets & configuration
- `src/` - Main application logic (5 files)
- `lambda/` - AWS Lambda deployment
- `deployment/` - Shell scripts for deployment

**Key Classes:**
- `AIDigestService` - Orchestrator
- `NewsScraper` - Fetches RSS
- `DigestGenerator` - Claude API
- `TTSConverter` - OpenAI TTS
- `PhoneCaller` - Twilio calls

**External APIs:**
- RSS feeds (feedparser)
- Claude (OpenAI SDK)
- OpenAI TTS (OpenAI SDK)
- Twilio (twilio SDK)

**Deployment:**
- Local: `python -m src.main test`
- Schedule: `python -m src.main schedule`
- Lambda: CloudWatch Events → Lambda
- Cron: Scheduled shell command
- Heroku: Dyno with scheduler

---

**Last Updated:** 2026-08-13  
**Version:** 1.0  
**Maintainer:** Claude Code  

