# ⚡ Quick Reference Guide

Bookmark this page for common commands and links!

---

## 🚀 Quick Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Test the system
python -m src.main test

# Run scheduler (daily at 9 AM)
python -m src.main schedule

# Show configuration
python -m src.main show-config

# List news sources
python -m src.main list-sources

# Deploy to Lambda
./deployment/lambda_deploy.sh

# Setup cron job
./deployment/cron_setup.sh
```

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `README.md` | Project overview |
| `.env.example` | Copy to `.env` and fill in credentials |
| `src/main.py` | Entry point |
| `config/news_sources.py` | Edit to add/remove news sources |
| `docs/SETUP.md` | Getting started guide |
| `docs/DEPLOYMENT.md` | Production deployment |
| `docs/TROUBLESHOOTING.md` | Common issues |

---

## 🔐 Setup Checklist

- [ ] Sign up Twilio (twilio.com)
- [ ] Get Twilio Account SID
- [ ] Get Twilio Auth Token
- [ ] Get Twilio Phone Number
- [ ] Get OpenAI API Key (platform.openai.com)
- [ ] Create `.env` from `.env.example`
- [ ] Fill in all .env variables
- [ ] Run: `pip install -r requirements.txt`
- [ ] Test: `python -m src.main test`
- [ ] Receive test call!
- [ ] Deploy to production

---

## 🌐 External Links

| Service | Link | Purpose |
|---------|------|---------|
| Twilio | twilio.com | Phone calls |
| OpenAI | platform.openai.com | Claude API + TTS |
| AWS Lambda | aws.amazon.com/lambda | Serverless deployment |
| GitHub | github.com | Code hosting |
| Heroku | heroku.com | Alternative hosting |

---

## 💰 Cost

| Item | Cost |
|------|------|
| Twilio | $0.60/mo |
| OpenAI | $1.50/mo |
| AWS Lambda | $0.20/mo |
| S3 (optional) | $0.50/mo |
| **TOTAL** | **~$3/mo** |

---

## 📞 File Structure (Minimal)

```
ai-digest-phone-calls/
├── .env (your secrets)
├── src/
│   ├── main.py
│   ├── news_scraper.py
│   ├── digest_generator.py
│   ├── tts_converter.py
│   └── caller.py
├── config/
│   ├── settings.py
│   └── news_sources.py
└── docs/
    ├── SETUP.md
    ├── DEPLOYMENT.md
    └── TROUBLESHOOTING.md
```

---

## 🔄 Daily Workflow

**After setup:**

Your digest will:
1. Call at 9 AM (configurable)
2. Scrape AI news
3. Generate digest via Claude
4. Convert to speech
5. Read it to you
6. Hang up
7. Repeat tomorrow! 📱

No action needed from you!

---

## 🆘 Help

- **Setup issues?** → `docs/SETUP.md`
- **Deployment help?** → `docs/DEPLOYMENT.md`
- **Errors?** → `docs/TROUBLESHOOTING.md`
- **Code questions?** → Use Cursor AI (Cmd+Shift+L)
- **GitHub upload?** → `GITHUB_UPLOAD.md`

---

## 📊 Metrics to Track

Keep track of:
- Cost per month (should be ~$3)
- Call success rate (should be ~100%)
- News sources added (more = better variety)
- Digest quality (subjective - adjust as needed)

---

## 🎯 Next Milestones

1. ✅ Get first test call working
2. ✅ Deploy to production
3. ✅ Customize news sources
4. ✅ Share on GitHub
5. ✅ Get others to try it
6. 🚀 Add email notifications
7. 🚀 Add Slack integration
8. 🚀 Build web dashboard

---

## 🔧 Customization Quick Links

**Change call time?**
→ Edit `.env`: `CALL_TIME=08:00`

**Change voice?**
→ Edit `.env`: `OPENAI_TTS_VOICE=nova`

**Add news source?**
→ Edit `config/news_sources.py`

**Change digest format?**
→ Edit `src/digest_generator.py`

---

## 📱 Cursor IDE Tips

| Action | Shortcut |
|--------|----------|
| AI Chat | Cmd+Shift+L (Mac) or Ctrl+Shift+L (Windows) |
| Code Lens | Cmd+K or Ctrl+K |
| Terminal | Ctrl+` |
| Search | Cmd+F or Ctrl+F |
| Find & Replace | Cmd+H or Ctrl+H |

---

## 🚀 Deployment Quick Links

**AWS Lambda:**
```bash
./deployment/lambda_deploy.sh
```
Then set CloudWatch trigger.

**Linux Cron:**
```bash
./deployment/cron_setup.sh
```
Auto-configured!

**Heroku:**
```bash
git push heroku main
```
Then scale worker.

---

## ✅ Success Checklist

- [ ] First test call received
- [ ] Credentials stored in `.env`
- [ ] `.env` added to `.gitignore`
- [ ] Project pushed to GitHub
- [ ] Deployed to production
- [ ] Call scheduled for 9 AM tomorrow
- [ ] Custom news sources added
- [ ] Shared with a friend!

---

**Bookmark this page!** Reference it whenever you need quick answers. 📚

Questions? See the appropriate doc or use Cursor AI. 🤖
