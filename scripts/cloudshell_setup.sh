#!/bin/bash
# Script para ejecutar en AWS CloudShell
# Configuración paso a paso

echo "🚀 Swiss Medical Triage System - AWS Setup"
echo ""

# Variables
REGION="us-east-1"
USER_NAME="swiss-medical-dev"

# Paso 1: Crear usuario IAM
echo "1️⃣ Creando usuario IAM..."
aws iam create-user --user-name $USER_NAME 2>/dev/null || echo "✅ Usuario ya existe"

# Paso 2: Crear política
echo "2️⃣ Creando política de permisos..."
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

cat > /tmp/policy.json <<'EOF'
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": ["dynamodb:*"],
            "Resource": "arn:aws:dynamodb:*:*:table/health-tech-*"
        },
        {
            "Effect": "Allow",
            "Action": ["bedrock:*"],
            "Resource": "*"
        }
    ]
}
EOF

aws iam create-policy \
    --policy-name SwissMedicalTriagePolicy \
    --policy-document file:///tmp/policy.json 2>/dev/null || echo "✅ Política ya existe"

# Paso 3: Adjuntar política
echo "3️⃣ Adjuntando política al usuario..."
POLICY_ARN="arn:aws:iam::${ACCOUNT_ID}:policy/SwissMedicalTriagePolicy"
aws iam attach-user-policy \
    --user-name $USER_NAME \
    --policy-arn $POLICY_ARN 2>/dev/null || echo "✅ Política ya adjuntada"

# Paso 4: Crear access key
echo "4️⃣ Creando access keys..."
aws iam create-access-key --user-name $USER_NAME --output json > /tmp/access-key.json 2>/dev/null

if [ -f /tmp/access-key.json ]; then
    echo ""
    echo "✅ CREDENCIALES CREADAS:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    cat /tmp/access-key.json | jq -r '"AWS_ACCESS_KEY_ID=" + .AccessKey.AccessKeyId'
    cat /tmp/access-key.json | jq -r '"AWS_SECRET_ACCESS_KEY=" + .AccessKey.SecretAccessKey'
    echo "AWS_REGION=us-east-1"
    echo "AWS_ACCOUNT_ID=$ACCOUNT_ID"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
fi

# Paso 5: Crear tablas DynamoDB
echo "5️⃣ Creando tablas DynamoDB..."

aws dynamodb create-table \
    --table-name health-tech-patients \
    --attribute-definitions AttributeName=patient_id,AttributeType=S \
    --key-schema AttributeName=patient_id,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST \
    --region $REGION 2>/dev/null && echo "✅ health-tech-patients" || echo "⚠️  health-tech-patients ya existe"

aws dynamodb create-table \
    --table-name health-tech-consultations \
    --attribute-definitions AttributeName=consultation_id,AttributeType=S AttributeName=patient_id,AttributeType=S \
    --key-schema AttributeName=consultation_id,KeyType=HASH \
    --global-secondary-indexes "IndexName=patient_id-index,KeySchema=[{AttributeName=patient_id,KeyType=HASH}],Projection={ProjectionType=ALL}" \
    --billing-mode PAY_PER_REQUEST \
    --region $REGION 2>/dev/null && echo "✅ health-tech-consultations" || echo "⚠️  health-tech-consultations ya existe"

aws dynamodb create-table \
    --table-name health-tech-triage \
    --attribute-definitions AttributeName=triage_id,AttributeType=S AttributeName=patient_id,AttributeType=S \
    --key-schema AttributeName=triage_id,KeyType=HASH \
    --global-secondary-indexes "IndexName=patient_id-index,KeySchema=[{AttributeName=patient_id,KeyType=HASH}],Projection={ProjectionType=ALL}" \
    --billing-mode PAY_PER_REQUEST \
    --region $REGION 2>/dev/null && echo "✅ health-tech-triage" || echo "⚠️  health-tech-triage ya existe"

echo ""
echo "6️⃣ Verificando tablas..."
aws dynamodb list-tables --region $REGION --output table

echo ""
echo "✅ CONFIGURACIÓN COMPLETA"
echo ""
echo "📋 COPIAR ESTAS CREDENCIALES A TU .env LOCAL:"
if [ -f /tmp/access-key.json ]; then
    cat /tmp/access-key.json | jq -r '"AWS_ACCESS_KEY_ID=" + .AccessKey.AccessKeyId'
    cat /tmp/access-key.json | jq -r '"AWS_SECRET_ACCESS_KEY=" + .AccessKey.SecretAccessKey'
    echo "AWS_REGION=us-east-1"
    echo "AWS_ACCOUNT_ID=$ACCOUNT_ID"
fi
echo ""
