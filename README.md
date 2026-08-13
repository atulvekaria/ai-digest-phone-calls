# 📱 Daily AI Digest Phone Calls

Automated voice briefings of the latest AI/LLM news every morning at 9 AM.

**What it does:**
1. Scrapes today's AI news from Anthropic, OpenAI, HuggingFace
2. Uses Claude to synthesize into an actionable digest
3. Converts text-to-speech with natural AI voice
4. Calls your phone and reads it aloud
5. Runs daily at 9 AM (hands-free)

**Cost:** ~$3/month | **Setup time:** 30 minutes

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Twilio account (free trial: $15)
- OpenAI API key
- Your phone number

### 1. Clone & Setup (5 min)

```bash
git clone https://github.com/YOUR_USERNAME/ai-digest-phone-calls.git
cd ai-digest-phone-calls
pip install -r requirements.txt
```

### 2. Configure (5 min)

```bash
cp .env.example .env
# Edit .env with your credentials:
# TWILIO_ACCOUNT_SID=AC...
# TWILIO_AUTH_TOKEN=2x...
# etc.
```

### 3. Test (5 min)

```bash
python -m src.main test
```

You should receive a call in 10 seconds! 📞

### 4. Deploy (10 min)

**Option A: AWS Lambda (recommended)**
```bash
./deployment/lambda_deploy.sh
```

**Option B: Your Server**
```bash
crontab -e
# Add: 0 9 * * * /usr/bin/python3 /path/to/src/main.py
```

---

## 📁 Project Structure

```
ai-digest-phone-calls/
├── README.md                 # You are here
├── requirements.txt          # Python dependencies
├── .env.example             # Template for credentials
├── .gitignore              # GitHub ignore rules
│
├── src/
│   ├── __init__.py
│   ├── main.py             # Entry point (orchestration)
│   ├── news_scraper.py     # Fetch AI news from RSS
│   ├── digest_generator.py # Claude synthesis
│   ├── tts_converter.py    # Text-to-speech (OpenAI)
│   └── caller.py           # Twilio phone calls
│
├── config/
│   ├── __init__.py
│   ├── settings.py         # Configuration loader
│   └── news_sources.py     # RSS feed URLs
│
├── lambda/
│   └── lambda_handler.py   # AWS Lambda entry point
│
├── deployment/
│   ├── lambda_deploy.sh    # Deploy to AWS Lambda
│   ├── cron_setup.sh       # Setup cron job
│   └── Procfile            # Heroku deployment
│
└── docs/
    ├── SETUP.md            # Detailed setup guide
    ├── DEPLOYMENT.md       # Deployment options
    ├── TROUBLESHOOTING.md  # Common issues
    └── ARCHITECTURE.md     # How it all works
```

---

## 📋 What You Get Each Morning

```
🔴 CRITICAL (Red Alert)
- Any breaking API changes
- Pricing changes affecting your costs

🟡 IMPORTANT (Test This Week)
- New model capabilities
- Speed improvements

🟢 MONITOR (Interesting)
- Research papers
- New tools worth trying

💡 ACTION ITEMS
- Specific tests to run
- Deadlines for deprecations
```

**Duration:** 8-10 minutes (spoken, hands-free)

---

## 🔧 Configuration

All secrets go in `.env` (NOT in code):

```bash
# Twilio
TWILIO_ACCOUNT_SID=ACxxxxxxx
TWILIO_AUTH_TOKEN=2xxxxxx
TWILIO_PHONE_NUMBER=+1234567890
YOUR_CELL_NUMBER=+1999888777

# OpenAI
OPENAI_API_KEY=sk-proj-xxxxx

# Schedule
CALL_TIME=09:00
CALL_EVERY_DAY=true

# Optional
OPENAI_TTS_VOICE=onyx  # onyx, nova, shimmer, echo, fable
DEBUG=false
```

See `.env.example` for all options.

---

## 💰 Cost Estimate

| Service | Cost | Purpose |
|---------|------|---------|
| Twilio | $0.60/mo | Phone calls (~$0.02 each) |
| OpenAI | $1.50/mo | Claude + TTS (~$0.05/day) |
| AWS Lambda | $0.20/mo | Serverless compute |
| S3 (optional) | $0.50/mo | Audio file hosting |
| **TOTAL** | **~$3/month** | 🎉 |

---

## 🚀 Deployment Options

### Option 1: AWS Lambda (Recommended) ⭐
- **Cost:** ~$2/month
- **Reliability:** 99.99% uptime
- **Setup:** 10 minutes
- **Command:** `./deployment/lambda_deploy.sh`

### Option 2: Your Linux Server
- **Cost:** VPS cost + $2 Twilio/OpenAI
- **Reliability:** Depends on your server
- **Setup:** 5 minutes (cron job)
- **Command:** `./deployment/cron_setup.sh`

### Option 3: Heroku
- **Cost:** ~$7/month (free tier discontinued)
- **Reliability:** Good
- **Setup:** 10 minutes
- **Command:** `git push heroku main`

See `docs/DEPLOYMENT.md` for detailed instructions.

---

## 🧪 Testing

```bash
# Run digest once, right now
python -m src.main test

# Run in foreground (shows logs)
python -m src.main

# Show configuration (don't call)
python -m src.main --show-config

# List available news sources
python -m src.main --list-sources
```

---

## 📚 Documentation

- **[SETUP.md](docs/SETUP.md)** - Step-by-step getting started
- **[DEPLOYMENT.md](docs/DEPLOYMENT.md)** - Deployment to production
- **[TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)** - Common issues & fixes
- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - How the system works

---

## 🛠️ Customization

### Add More News Sources

Edit `config/news_sources.py`:

```python
NEWS_SOURCES = {
    "Anthropic": "https://www.anthropic.com/news/feed.xml",
    "OpenAI": "https://openai.com/blog/feed.rss",
    "Your Blog": "https://your-blog.com/feed.xml",  # Add yours
}
```

### Change Voice

In `.env`:
```bash
OPENAI_TTS_VOICE=shimmer  # Options: onyx, nova, shimmer, echo, fable
```

### Change Call Time

In `.env`:
```bash
CALL_TIME=08:30  # Any time in HH:MM format
```

### Modify Digest Format

Edit `src/digest_generator.py` to customize how Claude structures the digest.

---

## 🤝 Contributing

Found a bug? Want to add features?

1. Fork the repo
2. Create a branch: `git checkout -b feature/my-feature`
3. Make changes
4. Push: `git push origin feature/my-feature`
5. Open a Pull Request

---

## 📞 Support

- **Setup issues?** See `docs/TROUBLESHOOTING.md`
- **Deployment help?** See `docs/DEPLOYMENT.md`
- **Questions?** Open an issue on GitHub

---

## 📄 License

MIT License - feel free to use, modify, and distribute.

---

## 🎉 You're All Set!

Next step: Follow [SETUP.md](docs/SETUP.md) to get your first call working.

**Questions?** Open an issue or check the docs.

Good luck staying ahead in AI! 🚀
