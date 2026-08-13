#!/bin/bash
# Setup cron job for daily digest
# Usage: ./deployment/cron_setup.sh

set -e

echo "⏰ Setting up cron job..."

# Get full path to project
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_PATH="$(which python3)"

# Check if already exists
if crontab -l 2>/dev/null | grep -q "ai-digest-phone-calls"; then
    echo "ℹ️  Cron job already exists. Removing old entry..."
    crontab -l | grep -v "ai-digest-phone-calls" | crontab -
fi

# Create cron entry (9 AM daily, local time)
CRON_ENTRY="0 9 * * * cd $PROJECT_DIR && $PYTHON_PATH -m src.main test >> $PROJECT_DIR/logs/digest.log 2>&1"

# Add to crontab
(crontab -l 2>/dev/null; echo "$CRON_ENTRY") | crontab -

echo "✅ Cron job created!"
echo ""
echo "Details:"
echo "  Time: 09:00 every day"
echo "  Command: python -m src.main test"
echo "  Logs: $PROJECT_DIR/logs/digest.log"
echo ""
echo "To verify:"
echo "  crontab -l | grep ai-digest"
echo ""
echo "To remove later:"
echo "  crontab -e"
echo "  (delete the line with 'ai-digest-phone-calls')"

# Create logs directory
mkdir -p "$PROJECT_DIR/logs"
touch "$PROJECT_DIR/logs/digest.log"

echo ""
echo "✓ All set! Your digest will call at 9 AM tomorrow."
