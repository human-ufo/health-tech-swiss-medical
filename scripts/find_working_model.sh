#!/bin/bash
# Script para encontrar modelos de Claude que soporten ON_DEMAND

echo "🔍 Buscando modelos de Claude con soporte ON_DEMAND..."
echo ""

# Listar todos los modelos de Anthropic con ON_DEMAND
aws bedrock list-foundation-models \
    --region us-east-1 \
    --by-provider anthropic \
    --query "modelSummaries[?contains(inferenceTypesSupported, 'ON_DEMAND')].{ModelID:modelId,Name:modelName,Types:inferenceTypesSupported}" \
    --output table

echo ""
echo "📋 Modelos recomendados para usar:"
echo ""

# Buscar Claude 3.5 Sonnet
CLAUDE_35=$(aws bedrock list-foundation-models \
    --region us-east-1 \
    --by-provider anthropic \
    --query "modelSummaries[?contains(modelId, 'claude-3-5-sonnet') && contains(inferenceTypesSupported, 'ON_DEMAND')].modelId" \
    --output text | head -1)

if [ -n "$CLAUDE_35" ]; then
    echo "✅ Claude 3.5 Sonnet encontrado: $CLAUDE_35"
    echo "   Usar en .env: BEDROCK_MODEL_ID=$CLAUDE_35"
else
    echo "⚠️  Claude 3.5 Sonnet no disponible"
fi

# Buscar Claude 3 Sonnet
CLAUDE_3=$(aws bedrock list-foundation-models \
    --region us-east-1 \
    --by-provider anthropic \
    --query "modelSummaries[?contains(modelId, 'claude-3-sonnet') && contains(inferenceTypesSupported, 'ON_DEMAND')].modelId" \
    --output text | head -1)

if [ -n "$CLAUDE_3" ]; then
    echo "✅ Claude 3 Sonnet encontrado: $CLAUDE_3"
    echo "   Usar en .env: BEDROCK_MODEL_ID=$CLAUDE_3"
else
    echo "⚠️  Claude 3 Sonnet no disponible con ON_DEMAND"
fi

# Buscar Claude Instant
CLAUDE_INSTANT=$(aws bedrock list-foundation-models \
    --region us-east-1 \
    --by-provider anthropic \
    --query "modelSummaries[?contains(modelId, 'claude-instant') && contains(inferenceTypesSupported, 'ON_DEMAND')].modelId" \
    --output text | head -1)

if [ -n "$CLAUDE_INSTANT" ]; then
    echo "✅ Claude Instant encontrado: $CLAUDE_INSTANT"
    echo "   Usar en .env: BEDROCK_MODEL_ID=$CLAUDE_INSTANT"
else
    echo "⚠️  Claude Instant no disponible"
fi

echo ""
echo "💡 Copia uno de los modelos de arriba y actualiza tu .env"
