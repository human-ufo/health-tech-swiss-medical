#!/bin/bash
# Script para verificar acceso a Bedrock

echo "🔍 Verificando acceso a AWS Bedrock..."
echo ""

# Verificar modelos disponibles
echo "📋 Modelos de Claude disponibles:"
aws bedrock list-foundation-models \
    --region us-east-1 \
    --query "modelSummaries[?contains(modelId, 'claude')].{ID:modelId,Name:modelName,Status:modelLifecycle.status}" \
    --output table

echo ""
echo "🔐 Verificando acceso al modelo específico:"
aws bedrock get-foundation-model \
    --model-identifier anthropic.claude-3-sonnet-20240229-v1:0 \
    --region us-east-1 2>&1

echo ""
echo "📊 Estado de acceso a modelos:"
aws bedrock list-foundation-models \
    --region us-east-1 \
    --by-provider anthropic \
    --query "modelSummaries[?contains(modelId, 'claude-3-sonnet')].{ID:modelId,Status:modelLifecycle.status}" \
    --output table
