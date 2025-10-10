#!/bin/bash
# Script para reanudar recursos AWS

echo "▶️  Reanudando recursos AWS..."
echo ""

REGION="us-east-1"

echo "📋 PASO 1: Reactivar Access Keys"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Listar y reactivar access keys
ACCESS_KEYS=$(aws iam list-access-keys --user-name swiss-medical-dev --query 'AccessKeyMetadata[].AccessKeyId' --output text)

for KEY in $ACCESS_KEYS; do
    aws iam update-access-key \
        --user-name swiss-medical-dev \
        --access-key-id $KEY \
        --status Active 2>/dev/null && echo "✅ Access key $KEY reactivada"
done

echo ""
echo "📋 PASO 2: Verificar tablas DynamoDB"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

TABLES=$(aws dynamodb list-tables --region $REGION --query 'TableNames' --output text)

if [[ $TABLES == *"health-tech-patients"* ]]; then
    echo "✅ Tablas DynamoDB existen"
else
    echo "⚠️  Tablas no encontradas. Recreando..."
    bash infrastructure/scripts/setup_aws.sh
fi

echo ""
echo "📋 PASO 3: Habilitar Bedrock"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "⚠️  ACCIÓN MANUAL REQUERIDA:"
echo "1. Ir a: https://console.aws.amazon.com/bedrock/"
echo "2. Click en 'Model access'"
echo "3. Click en 'Manage model access'"
echo "4. Marcar 'Claude 3 Sonnet'"
echo "5. Click en 'Request model access'"
echo ""

echo "📋 PASO 4: Iniciar servicios locales"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
cd "/home/human/Documents/gen ai/proyecto 1 - gen ai"
source venv/bin/activate
nohup uvicorn src.api.main:app --host 0.0.0.0 --port 8000 > api_output.log 2>&1 &
nohup streamlit run src/ui/app.py --server.port 8501 --server.headless true > streamlit_output.log 2>&1 &

echo "✅ Servicios iniciados"
echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                ✅ SISTEMA REANUDADO                          ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "🌐 Acceso:"
echo "• Streamlit: http://localhost:8501"
echo "• API: http://localhost:8000/docs"
echo ""
