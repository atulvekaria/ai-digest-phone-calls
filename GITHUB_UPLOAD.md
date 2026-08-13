# 📤 Upload to GitHub

Complete guide to push your project to GitHub.

---

## Prerequisites

- GitHub account (github.com)
- Git installed on your computer
- Project folder ready

---

## Step 1: Create GitHub Repository (2 minutes)

1. Go to **github.com**
2. Click **+ icon** → **New repository**
3. Fill in:
   - **Repository name:** `ai-digest-phone-calls`
   - **Description:** "Automated voice briefings of daily AI news"
   - **Public** (if you want to share) or **Private**
   - **Add a README:** NO (we already have one)
   - **Add .gitignore:** NO (we already have one)
   - **License:** MIT
4. Click **Create repository**

---

## Step 2: Get Your GitHub URL

You should see something like:

```
https://github.com/YOUR_USERNAME/ai-digest-phone-calls.git
```

**Copy this URL** - you'll need it in 1 minute.

---

## Step 3: Push to GitHub

### Option A: From Command Line (Recommended)

```bash
# Navigate to project folder
cd /path/to/ai-digest-phone-calls

# Initialize git (if not already done)
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: AI digest phone call system"

# Add remote (replace URL with yours from Step 2)
git remote add origin https://github.com/YOUR_USERNAME/ai-digest-phone-calls.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

**Success!** Your code is now on GitHub! 🎉

### Option B: From Cursor IDE (Easier)

1. Open Cursor
2. Open project: `ai-digest-phone-calls`
3. Click **Source Control** (left sidebar, looks like branches icon)
4. Click **Publish to GitHub**
5. Select **Public** or **Private**
6. Done! 🎉

### Option C: GitHub Desktop App (Most Visual)

1. Install GitHub Desktop: `github.com/apps/desktop`
2. Open GitHub Desktop
3. File → Clone Repository
4. Paste URL: `https://github.com/YOUR_USERNAME/ai-digest-phone-calls`
5. Choose folder location
6. Click Clone
7. Make changes
8. Click "Commit to main"
9. Click "Push origin"

---

## Step 4: Verify Upload

1. Go to **github.com/YOUR_USERNAME/ai-digest-phone-calls**
2. You should see:
   - ✅ All files listed
   - ✅ README.md showing
   - ✅ Green "main" branch

---

## Step 5: Update Settings (Optional)

In GitHub repository page:

### Settings → General

- ✅ Description: "Automated voice briefings of daily AI news"
- ✅ Website: Leave blank or add your blog
- ✅ Topics: Add tags like `ai`, `twilio`, `openai`, `automation`

### Settings → Collaborators & teams

- Share with team members if collaborative

### Settings → Secrets (If Deploying from GitHub)

For GitHub Actions CI/CD:
```
TWILIO_ACCOUNT_SID=ACxxx
TWILIO_AUTH_TOKEN=2xxx
OPENAI_API_KEY=sk-proj-xxx
```

---

## Step 6: Share Your Project!

### GitHub Link
Share this link:
```
https://github.com/YOUR_USERNAME/ai-digest-phone-calls
```

### README
Your README.md automatically displays on GitHub homepage. ✅

### Star the Project
Encourage others: "⭐ If this helped you, please star it!"

---

## Making Changes & Syncing

### After you make changes locally:

```bash
# See what changed
git status

# Add changes
git add .

# Commit with message
git commit -m "Add Reddit news source"

# Push to GitHub
git push origin main
```

### Or in Cursor:

1. Click Source Control (left sidebar)
2. Write commit message
3. Click checkmark (commit)
4. Click sync/push

---

## Collaborating

### Invite someone to contribute:

1. Go to repository Settings
2. Collaborators & teams
3. Add their GitHub username
4. They can now push changes

### Clone someone else's repo:

```bash
git clone https://github.com/OTHER_USERNAME/ai-digest-phone-calls.git
cd ai-digest-phone-calls
# Make changes
# Push to YOUR fork
```

---

## Common Git Commands

| Command | What it does |
|---------|-------------|
| `git status` | See changes |
| `git add .` | Stage all changes |
| `git commit -m "msg"` | Save changes locally |
| `git push origin main` | Upload to GitHub |
| `git pull origin main` | Download from GitHub |
| `git log` | See commit history |
| `git branch` | List branches |

---

## Troubleshooting

### ❌ "Permission denied (publickey)"

**Problem:** Git authentication failed

**Fix:**
```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your-email@example.com"

# Add to GitHub:
# Settings → SSH and GPG keys → New SSH key
# Paste your public key
```

### ❌ "fatal: could not read Username"

**Problem:** Git asking for credentials

**Fix:**
```bash
# Use HTTPS instead of SSH
git remote set-url origin https://github.com/YOUR_USERNAME/ai-digest-phone-calls.git

# Or use personal access token:
# github.com/settings/tokens → Generate token
```

### ❌ ".env is in git history"

**Problem:** Accidentally committed secrets!

**Fix:**
```bash
# Remove from git (but keep local)
git rm --cached .env

# Add to .gitignore
echo ".env" >> .gitignore

# Commit
git add .gitignore
git commit -m "Remove .env from tracking"
git push origin main

# Force regenerate secrets!
```

---

## Best Practices

### Don't Commit:
- ❌ `.env` file (secrets!)
- ❌ `__pycache__/` (cache files)
- ❌ `venv/` (virtual environment)
- ❌ `*.mp3` (audio files)

**We included `.gitignore` to handle this automatically!** ✅

### Do Commit:
- ✅ `.env.example` (template)
- ✅ `.gitignore` (rules)
- ✅ `README.md` (documentation)
- ✅ Source code (src/)
- ✅ Config templates (config/)

### Good Commit Messages:
- ✅ "Add Reddit news source"
- ✅ "Fix Twilio auth error"
- ✅ "Improve error handling"
- ❌ "update"
- ❌ "stuff"
- ❌ "lol"

---

## Continuous Integration (Optional)

Create `.github/workflows/test.yml`:

```yaml
name: Tests
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - run: pip install -r requirements.txt
      - run: python -m pytest
```

This runs tests automatically on every push! (Requires `pytest` setup)

---

## Deploy from GitHub (Optional)

### Deploy to Heroku from GitHub:

1. Push to GitHub (done!)
2. Go to heroku.com
3. Dashboard → New → Create new app
4. Deployment → Connect to GitHub
5. Select your repository
6. Click Deploy Branch
7. Done!

### Deploy to AWS Lambda from GitHub:

Use GitHub Actions + AWS credentials.

See `docs/DEPLOYMENT.md` for details.

---

## Celebrate! 🎉

You've successfully:
- ✅ Created a professional GitHub project
- ✅ Uploaded your code
- ✅ Made it open source
- ✅ Shared with the world!

---

## Next Steps

1. ✅ Share your GitHub link with friends
2. ✅ Add a GitHub badge to README
3. ✅ Deploy to production
4. ✅ Help others use your project
5. ✅ Contribute to other projects!

---

## Resources

- **GitHub Docs:** docs.github.com
- **Git Cheat Sheet:** git-scm.com/cheat
- **Open Source Guide:** opensource.guide
- **Licensing:** choosealicense.com

---

**Your project is now on GitHub!** 🚀

Next: Deploy to production (Lambda/Server/Heroku) per `docs/DEPLOYMENT.md`
