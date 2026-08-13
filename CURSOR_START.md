# 🔮 Opening in Cursor

Cursor is an AI-first code editor - perfect for this project!

---

## Option 1: Open Folder in Cursor (Recommended)

### On Mac/Linux

```bash
# Navigate to project
cd /path/to/ai-digest-phone-calls

# Open in Cursor
cursor .
```

Or drag folder onto Cursor icon.

### On Windows

```cmd
cd C:\path\to\ai-digest-phone-calls
cursor .
```

Or right-click folder → "Open with Cursor"

---

## Option 2: Clone Directly to Cursor

1. Open Cursor
2. File → "Open Folder"
3. Navigate to: `/mnt/user-data/outputs/ai-digest-phone-calls`
4. Click "Open"

---

## What You'll See

```
ai-digest-phone-calls/
├── README.md                   ← Start here
├── src/                        ← Main code
│   ├── main.py                 ← Entry point
│   ├── news_scraper.py         ← Fetch news
│   ├── digest_generator.py     ← Claude
│   ├── tts_converter.py        ← Audio
│   └── caller.py               ← Phone calls
├── config/                     ← Settings
├── docs/                       ← Documentation
├── deployment/                 ← Deploy scripts
└── .env.example                ← Copy and configure
```

---

## First Steps in Cursor

1. **Copy `.env.example` to `.env`**
   - Right-click `.env.example`
   - "Copy"
   - New file → `.env`
   - Paste content
   - Fill in your credentials

2. **Open Terminal** (Ctrl + `)
   ```bash
   pip install -r requirements.txt
   python -m src.main test
   ```

3. **Read README.md** (Left side panel)

4. **Use Cursor's AI**
   - Highlight code → Cmd+K (Mac) or Ctrl+K (Windows)
   - Ask questions:
     - "What does this function do?"
     - "How do I add a new news source?"
     - "Help me debug this error"

---

## Useful Cursor Shortcuts

| Action | Mac | Windows/Linux |
|--------|-----|---------------|
| Open Command Palette | Cmd+Shift+P | Ctrl+Shift+P |
| AI Chat | Cmd+Shift+L | Ctrl+Shift+L |
| Code Lens (AI) | Cmd+K | Ctrl+K |
| Find | Cmd+F | Ctrl+F |
| Terminal | Ctrl+` | Ctrl+` |
| Run File | Cmd+R | Ctrl+R |

---

## Using Cursor's AI Features

### Ask about code
```
Highlight the news_scraper.py file
Press Cmd+K
Type: "Explain how this fetches news"
```

### Get help debugging
```
Highlight error message
Press Cmd+K
Type: "What does this error mean?"
```

### Generate new features
```
Press Cmd+Shift+L for chat
Type: "How would I add email notifications?"
```

---

## Next Steps

1. ✅ Open project in Cursor
2. ✅ Install dependencies: `pip install -r requirements.txt`
3. ✅ Configure `.env` with your credentials
4. ✅ Test: `python -m src.main test`
5. ✅ Deploy to GitHub
6. ✅ Deploy to production (Lambda/Server/Heroku)

---

## Tips for Cursor

- **Use tabs** at top to switch between files
- **Sidebar** on left shows file tree
- **Terminal** at bottom for running commands
- **AI Chat** (Cmd+Shift+L) for questions
- **Search** (Cmd+F) to find things fast
- **Git** integration built-in (Source Control tab)

---

## GitHub Upload from Cursor

1. Open terminal: Ctrl+`
2. Initialize git:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: AI digest phone call system"
   ```

3. Create GitHub repo:
   - Go to github.com
   - Click "New repository"
   - Name: `ai-digest-phone-calls`
   - Copy the git URL

4. Push from Cursor terminal:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/ai-digest-phone-calls.git
   git push -u origin main
   ```

Or use Cursor's built-in Git UI:
- Click "Source Control" (left sidebar)
- Publish to GitHub

---

## Project Already GitHub-Ready

This project includes:
- ✅ `.gitignore` (excludes secrets, cache)
- ✅ `README.md` (clear overview)
- ✅ `CONTRIBUTING.md` (for collaborators)
- ✅ Issue templates (for bug reports)
- ✅ MIT License (permissive)

Just push and share! 🚀

---

## Questions?

- **About code:** Use Cursor AI (Cmd+Shift+L)
- **About setup:** Read `docs/SETUP.md`
- **About deployment:** Read `docs/DEPLOYMENT.md`
- **About errors:** Read `docs/TROUBLESHOOTING.md`

---

**Ready?** Open Cursor and dive in! 🔮
