#!/bin/bash
# Deploy to AWS Lambda
# Usage: ./deployment/lambda_deploy.sh

set -e

echo "🚀 Deploying to AWS Lambda..."

# Check for AWS CLI
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI not found. Install with: pip install awscli"
    exit 1
fi

# Build package
echo "📦 Building deployment package..."

mkdir -p lambda_package
cd lambda_package

# Copy source files
cp -r ../src .
cp -r ../config .
cp ../lambda/lambda_handler.py .
cp ../.env .

# Install dependencies
pip install -r ../requirements.txt -t .

# Create deployment zip
zip -r ../function.zip .

cd ..

# Upload to Lambda
echo "📤 Uploading to AWS Lambda..."

# Create or update function
aws lambda update-function-code \
    --function-name ai-digest-caller \
    --zip-file fileb://function.zip \
    --region us-east-1

echo "✅ Deployment complete!"
echo ""
echo "Next steps:"
echo "1. Set up CloudWatch Events trigger:"
echo "   - Go to CloudWatch → Rules → Create rule"
echo "   - Schedule: cron(0 9 * * ? *)"  # 9 AM UTC daily
echo "   - Target: Lambda function 'ai-digest-caller'"
echo ""
echo "2. Set environment variables in Lambda console:"
echo "   - TWILIO_ACCOUNT_SID"
echo "   - TWILIO_AUTH_TOKEN"
echo "   - OPENAI_API_KEY"
echo "   - etc. (see .env.example)"

# Cleanup
rm -rf lambda_package
rm -f function.zip
