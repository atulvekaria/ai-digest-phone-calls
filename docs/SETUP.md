# 📱 Setup Guide - Daily AI Digest Phone Calls

Complete step-by-step guide to get your first call working.

**Time needed:** 30 minutes  
**Cost:** ~$3/month

---

## Prerequisites

- Python 3.9 or higher
- Git (to clone the repo)
- A phone number (for receiving calls)

---

## Step 1: Get Twilio Account (5 minutes)

1. Go to **twilio.com** and click "Sign up"
2. Create account with your email
3. Verify your phone number (they'll text/call you)
4. Go to **Console → Account**
5. Copy your:
   - **Account SID** (looks like: ACxxxxxxxxxxxxxxxx)
   - **Auth Token** (looks like: 2xxxxxxxxxxxxxxxx)
6. Go to **Phone Numbers → Manage Numbers**
7. Buy a phone number (costs ~$1-2/month)
8. Copy your **Twilio Phone Number** (e.g., +1234567890)

**Save these three values!** You'll need them in 5 minutes.

---

## Step 2: Get OpenAI API Key (3 minutes)

1. Go to **platform.openai.com**
2. Click your profile → "API keys"
3. Click "Create new secret key"
4. **Copy immediately!** (Won't show again)
5. Save it somewhere safe

---

## Step 3: Clone Project (2 minutes)

```bash
git clone https://github.com/YOUR_USERNAME/ai-digest-phone-calls.git
cd ai-digest-phone-calls
```

---

## Step 4: Setup & Configure (5 minutes)

### 4a. Create virtual environment (optional but recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 4b. Install dependencies

```bash
pip install -r requirements.txt
```

### 4c. Create `.env` file with your credentials

```bash
cp .env.example .env
```

Edit `.env` with your values:

```bash
# Paste your actual values here
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=2xxxxxxxxxxxxxxxx
TWILIO_PHONE_NUMBER=+1234567890
YOUR_CELL_NUMBER=+1999888777

OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx

CALL_TIME=09:00
```

---

## Step 5: Test (5 minutes)

```bash
python -m src.main test
```

**What to expect:**

```
🚀 Initializing AI Digest Service...
1️⃣  Scraping AI news...
   Found 12 items
2️⃣  Generating digest via Claude...
   Digest ready
3️⃣  Converting to speech...
   ✓ Audio saved to /tmp/ai_digest.mp3
4️⃣  Placing phone call...
   ✓ Call placed: CA123abc456...

✅ SUCCESS! Call placed: CA123abc456...
```

**Your phone will ring in ~10 seconds.**

When it rings, you should hear something like:

> "Good morning. Here is your AI digest for today. [digest content]... End of briefing. Have a great day."

**Congratulations!** 🎉 Your first call works!

---

## Step 6: Configure Commands

### Show configuration

```bash
python -m src.main show-config
```

### List news sources

```bash
python -m src.main list-sources
```

### Run in scheduler (runs daily at scheduled time)

```bash
python -m src.main schedule
```

Keep this terminal open. (Use `ctrl+c` to stop)

---

## Step 7: Deploy to Production (10 minutes)

Choose one deployment option below:

### Option A: AWS Lambda (Recommended) ⭐

Most reliable, cheapest ($1-2/month).

```bash
# Install AWS CLI
pip install awscli

# Configure AWS credentials
aws configure

# Deploy
./deployment/lambda_deploy.sh
```

Then set up CloudWatch trigger (see `docs/DEPLOYMENT.md`).

### Option B: Your Linux Server

Cheapest if you already have a server.

```bash
# Copy project to server
scp -r ai-digest-phone-calls/ user@server:/opt/

# SSH into server
ssh user@server

# Setup cron job
cd /opt/ai-digest-phone-calls
./deployment/cron_setup.sh
```

Your digest will call at 9 AM every day.

### Option C: Heroku

$7-10/month but easiest if unfamiliar with AWS.

```bash
# Install Heroku CLI
brew install heroku  # or: sudo snap install heroku

# Login
heroku login

# Create app
heroku create your-ai-digest

# Set environment variables
heroku config:set TWILIO_ACCOUNT_SID=ACxxx
heroku config:set TWILIO_AUTH_TOKEN=2xxx
# ... set all vars from .env

# Deploy
git push heroku main

# Scale
heroku ps:scale worker=1
```

---

## Troubleshooting

### ❌ "Invalid phone number"

Check format in `.env`:
- Must start with `+` (e.g., `+1999888777`)
- Must include country code

### ❌ "Authentication failed"

Check your Twilio credentials:
- Account SID starts with `AC`
- Auth Token starts with `2`
- Copy-paste exactly (no extra spaces)

### ❌ "OpenAI API key invalid"

- Check key starts with `sk-proj-`
- Try generating a new one: platform.openai.com/api-keys
- Don't share this key!

### ❌ "No news found"

RSS feeds might be down. Check:

```bash
python -m src.main list-sources
```

Add more sources in `config/news_sources.py`.

### ❌ "ModuleNotFoundError"

Make sure you installed dependencies:

```bash
pip install -r requirements.txt
```

---

## Customization

### Change call time

Edit `.env`:

```
CALL_TIME=07:30  # Any time HH:MM
```

### Change TTS voice

Edit `.env`:

```
OPENAI_TTS_VOICE=shimmer  # Options: onyx, nova, shimmer, echo, fable
```

Different voices:
- `onyx` - Deep, clear (default)
- `nova` - Bright, energetic
- `shimmer` - Warm, professional
- `echo` - Medium, neutral
- `fable` - Expressive, engaging

### Add news sources

Edit `config/news_sources.py`:

```python
"Your Blog": {
    "url": "https://your-blog.com/feed.xml",
    "priority": 1,
    "max_items": 3
}
```

---

## What's Next?

1. ✅ Get first test call working
2. ✅ Deploy to production (AWS Lambda or your server)
3. ✅ Test actual scheduled call (wait until tomorrow!)
4. ✅ Customize news sources
5. ✅ Adjust TTS voice if desired

---

## Getting Help

- Check `docs/TROUBLESHOOTING.md` for common issues
- Check `docs/DEPLOYMENT.md` for production setup
- See `README.md` for project overview

---

**You're all set!** Tomorrow at 9 AM, you'll get your first automated digest call. ☎️
