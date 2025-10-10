#!/bin/bash
# Script para pausar recursos AWS y evitar costos

echo "⏸️  Pausando recursos AWS para evitar costos..."
echo ""

REGION="us-east-1"

echo "📋 PASO 1: Deshabilitar acceso a modelos Bedrock"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "⚠️  ACCIÓN MANUAL REQUERIDA:"
echo "1. Ir a: https://console.aws.amazon.com/bedrock/"
echo "2. Click en 'Model access'"
echo "3. Click en 'Manage model access'"
echo "4. DESMARCAR todos los modelos"
echo "5. Click en 'Save changes'"
echo ""

echo "📋 PASO 2: Eliminar datos de DynamoDB (opcional)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "⚠️  Las tablas con PAY_PER_REQUEST solo cobran por uso"
echo "Si NO hay tráfico, NO hay costo"
echo ""
read -p "¿Deseas ELIMINAR las tablas DynamoDB? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Eliminando tablas..."
    aws dynamodb delete-table --table-name health-tech-patients --region $REGION 2>/dev/null && echo "✅ health-tech-patients eliminada"
    aws dynamodb delete-table --table-name health-tech-consultations --region $REGION 2>/dev/null && echo "✅ health-tech-consultations eliminada"
    aws dynamodb delete-table --table-name health-tech-triage --region $REGION 2>/dev/null && echo "✅ health-tech-triage eliminada"
else
    echo "⏭️  Tablas DynamoDB mantenidas (sin costo si no hay uso)"
fi

echo ""
echo "📋 PASO 3: Eliminar imágenes ECR (opcional)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
read -p "¿Deseas ELIMINAR el repositorio ECR? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Eliminando repositorio ECR..."
    aws ecr delete-repository \
        --repository-name health-tech-swiss-medical \
        --region $REGION \
        --force 2>/dev/null && echo "✅ Repositorio ECR eliminado"
else
    echo "⏭️  Repositorio ECR mantenido"
fi

echo ""
echo "📋 PASO 4: Desactivar Access Keys (recomendado)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
read -p "¿Deseas DESACTIVAR las access keys del usuario? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Listar access keys
    ACCESS_KEYS=$(aws iam list-access-keys --user-name swiss-medical-dev --query 'AccessKeyMetadata[].AccessKeyId' --output text)
    
    for KEY in $ACCESS_KEYS; do
        aws iam update-access-key \
            --user-name swiss-medical-dev \
            --access-key-id $KEY \
            --status Inactive 2>/dev/null && echo "✅ Access key $KEY desactivada"
    done
else
    echo "⏭️  Access keys mantenidas activas"
fi

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                  ✅ RECURSOS AWS PAUSADOS                    ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "💰 COSTOS ACTUALES ESTIMADOS:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "• DynamoDB (sin uso): \$0.00/mes"
echo "• Bedrock (deshabilitado): \$0.00/mes"
echo "• ECR (sin imágenes): \$0.00/mes"
echo "• Access Keys (inactivas): \$0.00/mes"
echo ""
echo "📝 PARA REACTIVAR EL SISTEMA:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1. Reactivar access keys en IAM"
echo "2. Habilitar Bedrock en la consola"
echo "3. Recrear tablas DynamoDB (si fueron eliminadas)"
echo "4. Ejecutar: bash scripts/resume_aws.sh"
echo ""
