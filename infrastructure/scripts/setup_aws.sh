#!/bin/bash

# Setup script for AWS infrastructure
# This script creates all necessary AWS resources for the Swiss Medical Triage System

set -e

echo "🚀 Setting up AWS infrastructure for Swiss Medical Triage System"

# Variables
REGION=${AWS_REGION:-us-east-1}
STACK_NAME="swiss-medical-triage-stack"

# Check AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI is not installed. Please install it first."
    exit 1
fi

# Check AWS credentials
echo "✅ Checking AWS credentials..."
aws sts get-caller-identity > /dev/null 2>&1 || {
    echo "❌ AWS credentials not configured. Please run 'aws configure'"
    exit 1
}

echo "✅ AWS credentials verified"

# Deploy CloudFormation stack
echo "📦 Deploying DynamoDB tables via CloudFormation..."
aws cloudformation deploy \
    --template-file infrastructure/cloudformation/dynamodb.yml \
    --stack-name $STACK_NAME \
    --region $REGION \
    --no-fail-on-empty-changeset

echo "✅ CloudFormation stack deployed"

# Enable Bedrock model access (manual step required)
echo "⚠️  MANUAL STEP REQUIRED:"
echo "Please enable AWS Bedrock model access in the AWS Console:"
echo "1. Go to AWS Bedrock console: https://console.aws.amazon.com/bedrock/"
echo "2. Navigate to 'Model access' in the left sidebar"
echo "3. Request access to 'Claude 3 Sonnet' model"
echo "4. Wait for approval (usually instant for free tier)"

# Create ECR repository (optional, for container deployment)
echo "📦 Creating ECR repository..."
aws ecr describe-repositories --repository-names health-tech-swiss-medical --region $REGION > /dev/null 2>&1 || {
    aws ecr create-repository \
        --repository-name health-tech-swiss-medical \
        --region $REGION \
        --image-scanning-configuration scanOnPush=true
    echo "✅ ECR repository created"
}

echo ""
echo "✅ AWS infrastructure setup complete!"
echo ""
echo "Next steps:"
echo "1. Copy .env.example to .env and fill in your AWS credentials"
echo "2. Enable Bedrock model access (see manual step above)"
echo "3. Run 'pip install -r requirements.txt' to install dependencies"
echo "4. Run 'uvicorn src.api.main:app --reload' to start the API"
echo "5. Run 'streamlit run src/ui/app.py' to start the UI"
