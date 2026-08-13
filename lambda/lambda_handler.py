"""
AWS Lambda handler for daily AI digest.

Deploy to Lambda and set CloudWatch Events rule to trigger daily at 9 AM UTC.
"""

import os
import sys
import logging

# Add src to path for Lambda
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.main import AIDigestService

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """
    AWS Lambda handler function.
    Triggered by CloudWatch Events rule (daily at specified time).
    
    Args:
        event: CloudWatch Events event
        context: Lambda context
    
    Returns:
        Response dict with statusCode and body
    """
    try:
        logger.info("Starting AI Digest Lambda function...")
        
        service = AIDigestService()
        success = service.run_digest()
        
        if success:
            return {
                "statusCode": 200,
                "body": "Digest call placed successfully"
            }
        else:
            return {
                "statusCode": 500,
                "body": "Digest call failed"
            }
    
    except Exception as e:
        logger.error(f"Lambda error: {e}", exc_info=True)
        return {
            "statusCode": 500,
            "body": str(e)
        }


if __name__ == "__main__":
    # For local testing: python lambda_handler.py
    response = lambda_handler({}, None)
    print(response)
