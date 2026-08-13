# 🆘 Troubleshooting Guide

Common issues and how to fix them.

---

## Installation Issues

### ModuleNotFoundError: No module named 'twilio'

**Problem:** Missing dependencies

**Fix:**
```bash
pip install -r requirements.txt
```

### ModuleNotFoundError: No module named 'dotenv'

**Problem:** .env file loader not installed

**Fix:**
```bash
pip install python-dotenv
```

---

## Configuration Issues

### ❌ "Missing required setting: TWILIO_ACCOUNT_SID"

**Problem:** `.env` file not configured

**Check:**
1. Did you create `.env` file?
   ```bash
   cp .env.example .env
   ```

2. Is it in the project root directory?
   ```bash
   ls -la .env
   ```

3. Did you fill in all required values?
   ```bash
   cat .env | grep TWILIO
   ```

### ❌ "Invalid phone number: +1234567890"

**Problem:** Phone number format is wrong

**Fix:**
- Must start with `+` (e.g., `+1999888777`)
- Must include country code (US = 1, UK = 44, etc.)
- No spaces or dashes
- Check Twilio dashboard for correct format

### ❌ "TWILIO_AUTH_TOKEN not found"

**Problem:** Token has extra spaces or copied wrong

**Fix:**
1. Go to Twilio Console
2. Click "Show Auth Token"
3. Copy ENTIRE token (not just part)
4. Paste exactly into `.env`
5. No extra spaces!

---

## Authentication Issues

### ❌ "Twilio authentication failed"

**Problem:** Account SID or Auth Token is wrong

**Fix:**
```bash
# Test Twilio credentials
python -c "
from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()
client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
print('✓ Twilio auth successful!')
"
```

### ❌ "OpenAI API key invalid"

**Problem:** API key is expired or wrong

**Fix:**
1. Go to platform.openai.com/api-keys
2. Delete old keys
3. Create new key
4. Copy to `.env`
5. Test:
   ```bash
   python -c "
   from openai import OpenAI
   import os
   from dotenv import load_dotenv
   
   load_dotenv()
   client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
   print('✓ OpenAI auth successful!')
   "
   ```

---

## Call Issues

### ❌ "Call failed: Invalid phone number"

**Problem:** YOUR_CELL_NUMBER format is wrong

**Fix:**
- Check format: `+1234567890` (with country code)
- Call your own number to verify format:
  ```bash
  python -c "
  import os
  from dotenv import load_dotenv
  load_dotenv()
  print(os.getenv('YOUR_CELL_NUMBER'))
  "
  ```

### ❌ "Call placed but no ring"

**Problem:** Several possibilities

**Fix:**
1. Check Twilio is activated (not trial mode?)
2. Check YOUR_CELL_NUMBER is correct:
   ```bash
   # Try calling yourself manually via Twilio Console
   ```
3. Check phone is not on Do Not Disturb
4. Check phone number has not been blocked

### ❌ "Call rings but no audio"

**Problem:** Audio file not uploaded/accessible

**Fix:**
- For testing: Uses text-to-speech (no audio file needed)
- For production: Need to upload audio to S3 (see DEPLOYMENT.md)

### ❌ "Call keeps hanging up"

**Problem:** Timeout or error in Lambda/server

**Fix:**
1. Check Lambda timeout (should be 60+ seconds)
2. Check logs:
   ```bash
   # Lambda
   aws logs tail /aws/lambda/ai-digest-caller --follow
   
   # Server
   tail -f /var/log/ai-digest.log
   
   # Heroku
   heroku logs --tail
   ```

---

## News Scraping Issues

### ❌ "No news found today!"

**Problem:** RSS feeds are down or empty

**Fix:**
1. Check what sources are configured:
   ```bash
   python -m src.main list-sources
   ```

2. Test individual feed:
   ```bash
   python -c "
   import feedparser
   feed = feedparser.parse('https://www.anthropic.com/news/feed.xml')
   print(f'Found {len(feed.entries)} entries')
   print(feed.entries[0].title if feed.entries else 'No entries')
   "
   ```

3. Add more sources in `config/news_sources.py`

4. Try different feeds:
   - Anthropic: https://www.anthropic.com/news/feed.xml
   - OpenAI: https://openai.com/blog/feed.rss
   - HuggingFace: https://huggingface.co/feed/papers

---

## Digest Generation Issues

### ❌ "Claude API rate limit hit"

**Problem:** Too many API calls too fast

**Fix:**
- Wait a minute before testing again
- For production: already scheduled to call once/day (should be fine)

### ❌ "Digest validation failed"

**Problem:** Claude didn't return expected format

**Fix:**
1. Check Claude still has the model available
2. Try with different model in `.env`:
   ```
   CLAUDE_MODEL=claude-3-sonnet-20240229
   ```
3. Check digest content:
   ```bash
   python -m src.digest_generator
   ```

---

## TTS/Audio Issues

### ❌ "OpenAI TTS API error"

**Problem:** API error in text-to-speech conversion

**Fix:**
1. Check API quota: platform.openai.com/account/billing/overview
2. Try shorter text (if digest is too long)
3. Check voice name is correct:
   ```
   OPENAI_TTS_VOICE=onyx  # Must be one of: onyx, nova, shimmer, echo, fable
   ```

### ❌ "Audio file too large"

**Problem:** Digest text is too long

**Fix:**
- Shorten digest (max ~10 minutes spoken)
- Reduce number of news sources in `config/news_sources.py`
- Reduce `max_items` per source

---

## Scheduler/Cron Issues

### ❌ "Digest not calling at scheduled time"

**Fix:**
1. Check scheduler is running:
   ```bash
   # If running locally
   python -m src.main schedule
   ```

2. Check cron job exists:
   ```bash
   crontab -l | grep ai-digest
   ```

3. Check logs:
   ```bash
   # Last 50 lines
   tail -50 /var/log/syslog | grep CRON
   
   # Or check specific log
   tail -f /var/log/ai-digest.log
   ```

4. Test manually:
   ```bash
   python -m src.main test
   ```

### ❌ "Wrong time of day"

**Problem:** Call time is in wrong timezone

**Fix:**
1. Check your timezone:
   ```bash
   date
   timedatectl
   ```

2. Update CALL_TIME in `.env`:
   ```
   CALL_TIME=09:00  # Local time for your server
   ```

3. Restart service:
   - If cron: restart cron daemon
   - If Lambda: rerun trigger (immediate effect)

---

## Lambda Specific Issues

### ❌ "Lambda function timeout"

**Problem:** Digest generation takes too long

**Fix:**
1. Increase timeout in Lambda Console:
   - Configuration → General settings → Timeout: 90 seconds

2. Reduce number of news sources:
   - Edit `config/news_sources.py`
   - Reduce `max_items`

### ❌ "Lambda function missing dependencies"

**Problem:** Package not built correctly

**Fix:**
```bash
# Rebuild and redeploy
./deployment/lambda_deploy.sh
```

### ❌ "Lambda env variables not working"

**Problem:** Variables not set

**Fix:**
1. Verify in Lambda Console:
   - Configuration → Environment variables
   - Check all required vars are there
2. Redeploy if you just added them:
   ```bash
   ./deployment/lambda_deploy.sh
   ```

---

## Server/VPS Issues

### ❌ "Permission denied creating .env"

**Problem:** Directory permissions issue

**Fix:**
```bash
chmod 755 /opt/ai-digest-phone-calls
chmod 600 /opt/ai-digest-phone-calls/.env
```

### ❌ "Cron email with errors"

**Problem:** Cron job errors being mailed to you

**Fix:**
1. Check the error:
   ```bash
   tail -f /var/log/ai-digest.log
   ```

2. Fix the issue
3. Retest:
   ```bash
   source venv/bin/activate
   python -m src.main test
   ```

### ❌ "SSH key permission too open"

**Problem:** Security warning when using cron

**Fix:**
```bash
chmod 600 ~/.ssh/id_rsa
chmod 644 ~/.ssh/id_rsa.pub
```

---

## Heroku Specific Issues

### ❌ "Slug too large"

**Problem:** Code too large to deploy

**Fix:**
```bash
# Remove venv before pushing
rm -rf venv
git add .
git commit -m "Remove venv"
git push heroku main
```

### ❌ "Worker not running"

**Problem:** Service crashed

**Fix:**
```bash
# Check status
heroku ps

# View logs
heroku logs --tail

# Restart
heroku ps:restart
```

### ❌ "Env var not picking up"

**Problem:** Environment variable not set in Heroku

**Fix:**
```bash
# Set variable
heroku config:set TWILIO_ACCOUNT_SID=ACxxx

# Verify
heroku config

# Restart app
heroku ps:restart
```

---

## Debugging

### Enable Debug Mode

In `.env`:
```
DEBUG=true
LOG_LEVEL=DEBUG
```

Run:
```bash
python -m src.main test
```

Much more verbose output!

### Check What's Happening

```bash
# Show configuration
python -m src.main show-config

# List news sources
python -m src.main list-sources

# Run test digest
python -m src.main test
```

### Check Each Component

```bash
# Test news scraper
python -m src.news_scraper

# Test digest generator
python -m src.digest_generator

# Test TTS converter
python -m src.tts_converter

# Test Twilio
python -m src.caller
```

---

## Still Stuck?

1. Check the logs (see above)
2. Read SETUP.md again (step by step)
3. Try a fresh test:
   ```bash
   python -m src.main test
   ```
4. Open an issue on GitHub with:
   - Error message
   - Your command
   - Last 20 lines of logs
   - Your setup (Lambda/Server/Heroku)

---

**Happy debugging!** Most issues are configuration-related. Double-check `.env` first. 🔍
