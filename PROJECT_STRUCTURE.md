# 📁 Project Structure

Complete overview of all files and directories.

```
ai-digest-phone-calls/
│
├── README.md                        # 📖 Start here - project overview
├── CONTRIBUTING.md                  # 🤝 How to contribute
├── PROJECT_STRUCTURE.md             # 📁 This file
├── requirements.txt                 # 📦 Python dependencies
├── .env.example                     # 🔐 Template for secrets
├── .gitignore                       # 🚫 Git ignore rules
│
├── src/                             # 🔧 Main application code
│   ├── __init__.py
│   ├── main.py                      # Entry point (orchestration)
│   ├── news_scraper.py              # Fetch AI news from RSS feeds
│   ├── digest_generator.py          # Claude synthesis to digest
│   ├── tts_converter.py             # Text-to-speech (OpenAI)
│   └── caller.py                    # Phone calls (Twilio)
│
├── config/                          # ⚙️  Configuration
│   ├── __init__.py
│   ├── settings.py                  # Load .env variables
│   └── news_sources.py              # RSS feeds configuration
│
├── lambda/                          # ☁️  AWS Lambda deployment
│   └── lambda_handler.py            # Lambda entry point
│
├── deployment/                      # 🚀 Deployment scripts
│   ├── lambda_deploy.sh             # Deploy to AWS Lambda
│   ├── cron_setup.sh                # Setup Linux cron job
│   └── Procfile                     # Heroku deployment config
│
├── docs/                            # 📚 Documentation
│   ├── SETUP.md                     # Quick start guide (30 min)
│   ├── DEPLOYMENT.md                # Production deployment options
│   ├── TROUBLESHOOTING.md           # Common issues & fixes
│   └── ARCHITECTURE.md              # System design (if created)
│
└── .github/                         # 🐙 GitHub specific
    └── ISSUE_TEMPLATE/
        └── bug_report.md            # Bug report template
```

---

## File Descriptions

### Root Level

| File | Purpose |
|------|---------|
| `README.md` | Project overview, quick start, features |
| `CONTRIBUTING.md` | Guidelines for contributing |
| `requirements.txt` | Python dependencies (install with pip) |
| `.env.example` | Template for .env (copy and fill in) |
| `.gitignore` | Files to ignore in git (secrets, cache) |

### `src/` - Main Application

| File | Purpose |
|------|---------|
| `main.py` | Orchestrates: scrape → digest → tts → call |
| `news_scraper.py` | Fetches AI news from RSS feeds |
| `digest_generator.py` | Uses Claude to synthesize news |
| `tts_converter.py` | Converts digest to speech (OpenAI TTS) |
| `caller.py` | Places phone calls (Twilio) |

### `config/` - Configuration

| File | Purpose |
|------|---------|
| `settings.py` | Loads environment variables from .env |
| `news_sources.py` | Configurable list of RSS feeds |

### `lambda/` - AWS Lambda

| File | Purpose |
|------|---------|
| `lambda_handler.py` | Entry point for Lambda function |

### `deployment/` - Deployment Scripts

| File | Purpose |
|------|---------|
| `lambda_deploy.sh` | Builds and deploys to AWS Lambda |
| `cron_setup.sh` | Sets up Linux cron job for daily call |
| `Procfile` | Heroku deployment config |

### `docs/` - Documentation

| File | Purpose |
|------|---------|
| `SETUP.md` | Step-by-step setup guide (30 min) |
| `DEPLOYMENT.md` | Production deployment options |
| `TROUBLESHOOTING.md` | Common issues and solutions |

---

## Data Flow

```
RSS Feeds (Anthropic, OpenAI, HuggingFace)
    ↓
[news_scraper.py] - Fetches latest articles
    ↓
List of news items
    ↓
[digest_generator.py] - Synthesizes with Claude
    ↓
Structured digest (CRITICAL / IMPORTANT / MONITOR / ACTIONS)
    ↓
[tts_converter.py] - Converts to speech (OpenAI TTS)
    ↓
Audio MP3 file
    ↓
[caller.py] - Places phone call (Twilio)
    ↓
📱 Your phone rings at 9 AM!
```

---

## Module Interactions

```
┌─────────────────────────────────────────┐
│         main.py (Orchestrator)          │
│                                         │
│  • Loads settings                       │
│  • Coordinates workflow                 │
│  • Handles scheduler                    │
│  • Error handling                       │
└─────────────────────────────────────────┘
            │   │   │   │
    ┌───────┘   │   │   └──────────┐
    │           │   │              │
    ↓           ↓   ↓              ↓
┌─────────┐ ┌──────┐ ┌──────┐ ┌─────────┐
│ Scraper │→│Digest│→│ TTS  │→│ Caller  │
│ (RSS)   │ │(LLM) │ │(Voice)│ │(Phone) │
└─────────┘ └──────┘ └──────┘ └─────────┘
    ↓           ↓      ↓           ↓
[News APIs]  [Claude] [OpenAI]  [Twilio]
```

---

## Environment Variables

All credentials go in `.env` (never commit!):

```
TWILIO_ACCOUNT_SID=ACxxxxxxx
TWILIO_AUTH_TOKEN=2xxxxxx
TWILIO_PHONE_NUMBER=+1234567890
YOUR_CELL_NUMBER=+1999888777
OPENAI_API_KEY=sk-proj-xxx
CALL_TIME=09:00
```

See `.env.example` for all options.

---

## Key Classes

### `NewsScraper` (src/news_scraper.py)
- Fetches RSS feeds
- Filters by keywords
- Formats for Claude

### `DigestGenerator` (src/digest_generator.py)
- Calls Claude API
- Synthesizes news into digest
- Validates structure

### `TTSConverter` (src/tts_converter.py)
- Calls OpenAI TTS API
- Generates MP3 audio
- Supports multiple voices

### `PhoneCaller` (src/caller.py)
- Calls Twilio API
- Places phone calls
- Handles errors

### `AIDigestService` (src/main.py)
- Coordinates all modules
- Implements scheduler
- Error handling

---

## Execution Paths

### Test Mode
```
python -m src.main test
├─ Scrapes news
├─ Generates digest
├─ Converts to speech
├─ Places ONE call immediately
└─ Exit
```

### Scheduler Mode
```
python -m src.main schedule
├─ Start scheduler
├─ Wait for scheduled time (9 AM)
├─ Run digest pipeline
├─ Sleep
└─ Repeat daily
```

### Show Config
```
python -m src.main show-config
├─ Print all settings
└─ Exit
```

### List Sources
```
python -m src.main list-sources
├─ Print all RSS feeds
└─ Exit
```

---

## Deployment Paths

### Local Testing
```
.env (with credentials)
↓
python -m src.main test
↓
Call placed to YOUR_CELL_NUMBER
```

### AWS Lambda
```
lambda/lambda_handler.py
↓
CloudWatch Events (daily at 9 AM)
↓
Lambda runs AIDigestService.run_digest()
↓
Call placed
```

### Linux Cron
```
deployment/cron_setup.sh
↓
crontab: 0 9 * * * python -m src.main test
↓
Cron daemon runs at 9 AM daily
↓
Call placed
```

### Heroku
```
deployment/Procfile: worker: python -m src.main schedule
↓
git push heroku main
↓
Dyno runs scheduler 24/7
↓
Calls at 9 AM daily
```

---

## How to Navigate

**First time?**
→ Start with `README.md` → `docs/SETUP.md`

**Want to deploy?**
→ `docs/DEPLOYMENT.md` for your platform

**Something broken?**
→ `docs/TROUBLESHOOTING.md`

**Want to contribute?**
→ `CONTRIBUTING.md`

**Need to modify?**
→ Find relevant file in `src/` and edit

**Want to add news source?**
→ Edit `config/news_sources.py`

---

## Testing Individual Components

```bash
# Test news scraper
python -m src.news_scraper

# Test digest generator
python -m src.digest_generator

# Test TTS converter
python -m src.tts_converter

# Test Twilio caller
python -m src.caller

# Full pipeline
python -m src.main test
```

---

## Dependencies

See `requirements.txt`:
- `twilio` - Phone calls
- `openai` - Claude API + TTS
- `feedparser` - RSS feeds
- `schedule` - Scheduling
- `python-dotenv` - .env loading
- `pydantic` - Settings validation

---

**Ready to dive in?** Start with README.md! 🚀
