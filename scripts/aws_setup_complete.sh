#!/bin/bash

# Script completo para configurar AWS desde CLI
# Para ejecutar en AWS CloudShell

set -e

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║   🚀 Configuración Completa AWS - Sistema de Triaje         ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

REGION="us-east-1"
USER_NAME="swiss-medical-dev"
POLICY_NAME="SwissMedicalTriagePolicy"

echo "📋 PASO 1: Crear Usuario IAM"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Crear usuario IAM
aws iam create-user --user-name $USER_NAME 2>/dev/null || echo "Usuario ya existe"

# Crear política personalizada
cat > /tmp/swiss-medical-policy.json <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "dynamodb:*"
            ],
            "Resource": [
                "arn:aws:dynamodb:${REGION}:*:table/health-tech-*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream",
                "bedrock:ListFoundationModels",
                "bedrock:GetFoundationModel"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "ecr:*"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "*"
        }
    ]
}
EOF

# Crear política
aws iam create-policy \
    --policy-name $POLICY_NAME \
    --policy-document file:///tmp/swiss-medical-policy.json 2>/dev/null || echo "Política ya existe"

# Obtener ARN de la política
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
POLICY_ARN="arn:aws:iam::${ACCOUNT_ID}:policy/${POLICY_NAME}"

# Adjuntar política al usuario
aws iam attach-user-policy \
    --user-name $USER_NAME \
    --policy-arn $POLICY_ARN 2>/dev/null || echo "Política ya adjuntada"

echo "✅ Usuario IAM creado: $USER_NAME"
echo ""

echo "📋 PASO 2: Crear Access Keys"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Crear access key
ACCESS_KEY_OUTPUT=$(aws iam create-access-key --user-name $USER_NAME 2>/dev/null || echo "")

if [ -n "$ACCESS_KEY_OUTPUT" ]; then
    ACCESS_KEY_ID=$(echo $ACCESS_KEY_OUTPUT | jq -r '.AccessKey.AccessKeyId')
    SECRET_ACCESS_KEY=$(echo $ACCESS_KEY_OUTPUT | jq -r '.AccessKey.SecretAccessKey')
    
    echo "✅ Access Keys creadas:"
    echo ""
    echo "AWS_ACCESS_KEY_ID=$ACCESS_KEY_ID"
    echo "AWS_SECRET_ACCESS_KEY=$SECRET_ACCESS_KEY"
    echo ""
    echo "⚠️  GUARDA ESTAS CREDENCIALES - No se mostrarán de nuevo"
    echo ""
    
    # Guardar en archivo
    cat > /tmp/aws-credentials.txt <<EOF
# Credenciales AWS para Swiss Medical Triage System
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=$ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY=$SECRET_ACCESS_KEY
AWS_ACCOUNT_ID=$ACCOUNT_ID
EOF
    
    echo "📝 Credenciales guardadas en: /tmp/aws-credentials.txt"
else
    echo "⚠️  No se pudieron crear nuevas access keys (puede que ya existan)"
    echo "Para listar keys existentes: aws iam list-access-keys --user-name $USER_NAME"
fi

echo ""
echo "📋 PASO 3: Crear Tablas DynamoDB"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Tabla de Pacientes
echo "Creando tabla: health-tech-patients..."
aws dynamodb create-table \
    --table-name health-tech-patients \
    --attribute-definitions AttributeName=patient_id,AttributeType=S \
    --key-schema AttributeName=patient_id,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST \
    --region $REGION 2>/dev/null && echo "✅ Tabla health-tech-patients creada" || echo "⚠️  Tabla health-tech-patients ya existe"

# Tabla de Consultas
echo "Creando tabla: health-tech-consultations..."
aws dynamodb create-table \
    --table-name health-tech-consultations \
    --attribute-definitions \
        AttributeName=consultation_id,AttributeType=S \
        AttributeName=patient_id,AttributeType=S \
    --key-schema AttributeName=consultation_id,KeyType=HASH \
    --global-secondary-indexes \
        "IndexName=patient_id-index,KeySchema=[{AttributeName=patient_id,KeyType=HASH}],Projection={ProjectionType=ALL}" \
    --billing-mode PAY_PER_REQUEST \
    --region $REGION 2>/dev/null && echo "✅ Tabla health-tech-consultations creada" || echo "⚠️  Tabla health-tech-consultations ya existe"

# Tabla de Triaje
echo "Creando tabla: health-tech-triage..."
aws dynamodb create-table \
    --table-name health-tech-triage \
    --attribute-definitions \
        AttributeName=triage_id,AttributeType=S \
        AttributeName=patient_id,AttributeType=S \
    --key-schema AttributeName=triage_id,KeyType=HASH \
    --global-secondary-indexes \
        "IndexName=patient_id-index,KeySchema=[{AttributeName=patient_id,KeyType=HASH}],Projection={ProjectionType=ALL}" \
    --billing-mode PAY_PER_REQUEST \
    --region $REGION 2>/dev/null && echo "✅ Tabla health-tech-triage creada" || echo "⚠️  Tabla health-tech-triage ya existe"

echo ""
echo "📋 PASO 4: Verificar Tablas DynamoDB"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

aws dynamodb list-tables --region $REGION

echo ""
echo "📋 PASO 5: Crear ECR Repository"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

aws ecr create-repository \
    --repository-name health-tech-swiss-medical \
    --region $REGION \
    --image-scanning-configuration scanOnPush=true 2>/dev/null && echo "✅ ECR repository creado" || echo "⚠️  ECR repository ya existe"

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    ✅ CONFIGURACIÓN COMPLETA                 ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "📝 RESUMEN:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Usuario IAM: $USER_NAME"
echo "✅ Política: $POLICY_NAME"
echo "✅ Tablas DynamoDB: 3 tablas creadas"
echo "✅ ECR Repository: health-tech-swiss-medical"
echo ""
echo "📋 PRÓXIMOS PASOS:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1. Copiar credenciales de /tmp/aws-credentials.txt"
echo "2. Pegar en tu archivo .env local"
echo "3. Habilitar AWS Bedrock (ver instrucciones abajo)"
echo "4. Reiniciar servicios locales"
echo ""
echo "⚠️  IMPORTANTE - HABILITAR AWS BEDROCK:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1. Ir a: https://console.aws.amazon.com/bedrock/"
echo "2. Click en 'Model access' (menú izquierdo)"
echo "3. Click en 'Manage model access'"
echo "4. Buscar 'Claude 3 Sonnet'"
echo "5. Marcar checkbox y solicitar acceso"
echo ""
echo "💾 Ver credenciales: cat /tmp/aws-credentials.txt"
echo ""
