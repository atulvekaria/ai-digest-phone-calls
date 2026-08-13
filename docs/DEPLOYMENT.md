# 🚀 Deployment Guide

Production deployment options for daily digest calls.

---

## Option 1: AWS Lambda (Recommended) ⭐

**Pros:**
- Serverless (no server to manage)
- Auto-scaling
- $0.20/month
- 99.99% uptime

**Cons:**
- Slight AWS learning curve
- Cold starts (~2 second delay)

### Steps

#### 1. Create Lambda Function

1. Go to AWS Console → Lambda
2. Click "Create function"
3. Name: `ai-digest-caller`
4. Runtime: Python 3.11
5. Click "Create"

#### 2. Deploy Code

```bash
# In project directory
./deployment/lambda_deploy.sh
```

Or manually:

```bash
mkdir lambda_package
cd lambda_package

pip install -r ../requirements.txt -t .
cp -r ../src .
cp -r ../config .
cp ../lambda/lambda_handler.py .

zip -r ../function.zip .

cd ..
aws lambda update-function-code \
    --function-name ai-digest-caller \
    --zip-file fileb://function.zip \
    --region us-east-1
```

#### 3. Set Environment Variables

In Lambda Console → Configuration → Environment variables:

```
TWILIO_ACCOUNT_SID=ACxxxxx
TWILIO_AUTH_TOKEN=2xxxxx
TWILIO_PHONE_NUMBER=+1234567890
YOUR_CELL_NUMBER=+1999888777
OPENAI_API_KEY=sk-proj-xxxxx
CLAUDE_MODEL=claude-3-5-sonnet-20241022
CALL_TIME=09:00
OPENAI_TTS_VOICE=onyx
```

#### 4. Increase Timeout

In Lambda Console → Configuration → General settings:
- Timeout: 60 seconds (digest takes ~30 seconds)
- Memory: 256 MB (default is fine)

#### 5. Create CloudWatch Trigger

1. In Lambda → Add trigger
2. Select "EventBridge (CloudWatch Events)"
3. Click "Create new rule"
4. Name: `ai-digest-daily`
5. Type: Schedule expression
6. Expression: `cron(0 9 * * ? *)`  (9 AM UTC every day)
7. Click "Add"

#### 6. Test

In Lambda Console → Test:
- Create test event (name: "test", leave default)
- Click "Test"
- Should see: "Digest call placed successfully"

**Done!** Digest will call daily at 9 AM UTC.

---

## Option 2: Your Linux Server

**Pros:**
- Full control
- No vendor lock-in
- Works on any VPS

**Cons:**
- Server must be running
- Manual updates
- Need to manage credentials

### Steps

#### 1. Copy Project to Server

```bash
scp -r ai-digest-phone-calls/ user@your-server:/opt/
ssh user@your-server
```

#### 2. Install on Server

```bash
cd /opt/ai-digest-phone-calls

# Setup Python environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create .env
cp .env.example .env
nano .env  # Edit with your values
```

#### 3. Setup Cron Job

```bash
./deployment/cron_setup.sh
```

Or manually:

```bash
crontab -e

# Add this line:
0 9 * * * cd /opt/ai-digest-phone-calls && /opt/ai-digest-phone-calls/venv/bin/python -m src.main test >> /var/log/ai-digest.log 2>&1
```

#### 4. Verify

```bash
# Check cron is set
crontab -l | grep ai-digest

# Check logs
tail -f /var/log/ai-digest.log

# Test manually
source venv/bin/activate
python -m src.main test
```

**Done!** Digest will call at 9 AM every day.

---

## Option 3: Heroku

**Note:** Heroku free tier ended March 2023. Cheapest paid option is ~$7/month.

**Pros:**
- Simple deployment (git push)
- Automatic restarts
- Good for learning

**Cons:**
- $7-10/month
- Slower than Lambda
- Less reliable than AWS

### Steps

#### 1. Install Heroku CLI

```bash
# macOS
brew install heroku

# Linux
sudo snap install heroku --classic

# Windows
# Download from heroku.com/download
```

#### 2. Login

```bash
heroku login
```

#### 3. Create Heroku App

```bash
cd ai-digest-phone-calls
heroku create your-unique-app-name
```

#### 4. Set Environment Variables

```bash
heroku config:set TWILIO_ACCOUNT_SID=ACxxxxx
heroku config:set TWILIO_AUTH_TOKEN=2xxxxx
heroku config:set TWILIO_PHONE_NUMBER=+1234567890
heroku config:set YOUR_CELL_NUMBER=+1999888777
heroku config:set OPENAI_API_KEY=sk-proj-xxxxx
# ... continue for all variables
```

Verify:
```bash
heroku config
```

#### 5. Deploy

```bash
git push heroku main
```

#### 6. Start Worker

```bash
heroku ps:scale worker=1
```

#### 7. Check Logs

```bash
heroku logs --tail
```

**Done!** Your digest is live on Heroku.

---

## Monitoring

### Lambda

Check CloudWatch Logs:
```bash
aws logs tail /aws/lambda/ai-digest-caller --follow
```

Or in AWS Console:
- Lambda → ai-digest-caller → Monitor → Logs

### Server (Cron)

Check logs:
```bash
tail -f /var/log/ai-digest.log
```

### Heroku

Check logs:
```bash
heroku logs --tail
```

---

## Cost Comparison

| Option | Monthly | Notes |
|--------|---------|-------|
| **Lambda** | ~$2 | Cheapest, most reliable |
| **Server** | VPS cost + $2 | If you have VPS already |
| **Heroku** | $7-10 | Easiest for non-devops |

---

## Troubleshooting Deployment

### Lambda

**Error: "Unable to locate credentials"**
- Run: `aws configure`
- Enter your AWS Access Key ID and Secret Access Key

**Error: "Function not found"**
- Make sure function name is `ai-digest-caller`
- Or change in lambda_deploy.sh

**Digest not being called**
- Check CloudWatch Events rule exists
- Check Lambda function timeout (should be 60s)
- Check environment variables are set

### Server

**Cron not running**
- Check cron is running: `systemctl status cron` (Linux)
- Check permissions: `chmod +x deployment/cron_setup.sh`
- Check logs: `tail -f /var/log/ai-digest.log`

**Permission denied**
- Make sure .env is readable
- Make sure venv directory is writable

### Heroku

**"Slug too large"**
- Delete `venv` directory before pushing
- Remove unnecessary files

**"Worker not running"**
- Check: `heroku ps`
- Restart: `heroku ps:restart`

---

## Updating Production

### Lambda

1. Make code changes locally
2. Run: `./deployment/lambda_deploy.sh`

### Server

1. SSH into server
2. `cd /opt/ai-digest-phone-calls`
3. `git pull origin main`
4. Test: `source venv/bin/activate && python -m src.main test`

### Heroku

1. Make code changes locally
2. Commit: `git add . && git commit -m "Update"`
3. Deploy: `git push heroku main`

---

## Scaling

### Lambda
- Already scales automatically
- No action needed

### Server
- Add more servers and load balance
- Or upgrade VPS resources

### Heroku
- Upgrade from free to professional dyno
- Costs more but more reliable

---

**Questions?** See TROUBLESHOOTING.md or open an issue on GitHub.
