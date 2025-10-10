"""Guide to setup AWS for the system."""
print("""
╔══════════════════════════════════════════════════════════════╗
║   🔧 GUÍA DE CONFIGURACIÓN AWS - Sistema de Triaje          ║
╚══════════════════════════════════════════════════════════════╝

📋 PASO 1: OBTENER CREDENCIALES AWS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Ir a: https://console.aws.amazon.com/iam/
2. Click en "Users" → Tu usuario
3. Click en "Security credentials"
4. En "Access keys" → "Create access key"
5. Seleccionar "Command Line Interface (CLI)"
6. Copiar:
   - Access Key ID
   - Secret Access Key

📋 PASO 2: CONFIGURAR CREDENCIALES LOCALMENTE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Editar el archivo .env:

nano .env

Agregar tus credenciales:

AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=AKIAXXXXXXXXXXXXXXXX
AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
AWS_ACCOUNT_ID=862172028272

📋 PASO 3: HABILITAR AWS BEDROCK (CRÍTICO)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Ir a: https://console.aws.amazon.com/bedrock/
2. Click en "Model access" (menú izquierdo)
3. Click en "Manage model access"
4. Buscar "Claude 3 Sonnet"
5. Marcar el checkbox
6. Click en "Request model access"
7. Esperar aprobación (usualmente instantánea)

⚠️  IMPORTANTE: Sin este paso, los agentes de IA NO funcionarán.

📋 PASO 4: CREAR TABLAS DYNAMODB
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Opción A - Automático (recomendado):

chmod +x infrastructure/scripts/setup_aws.sh
./infrastructure/scripts/setup_aws.sh

Opción B - Manual con AWS CLI:

aws dynamodb create-table \\
  --table-name health-tech-patients \\
  --attribute-definitions AttributeName=patient_id,AttributeType=S \\
  --key-schema AttributeName=patient_id,KeyType=HASH \\
  --billing-mode PAY_PER_REQUEST \\
  --region us-east-1

aws dynamodb create-table \\
  --table-name health-tech-consultations \\
  --attribute-definitions \\
    AttributeName=consultation_id,AttributeType=S \\
    AttributeName=patient_id,AttributeType=S \\
  --key-schema AttributeName=consultation_id,KeyType=HASH \\
  --global-secondary-indexes \\
    "IndexName=patient_id-index,KeySchema=[{AttributeName=patient_id,KeyType=HASH}],Projection={ProjectionType=ALL}" \\
  --billing-mode PAY_PER_REQUEST \\
  --region us-east-1

aws dynamodb create-table \\
  --table-name health-tech-triage \\
  --attribute-definitions \\
    AttributeName=triage_id,AttributeType=S \\
    AttributeName=patient_id,AttributeType=S \\
  --key-schema AttributeName=triage_id,KeyType=HASH \\
  --global-secondary-indexes \\
    "IndexName=patient_id-index,KeySchema=[{AttributeName=patient_id,KeyType=HASH}],Projection={ProjectionType=ALL}" \\
  --billing-mode PAY_PER_REQUEST \\
  --region us-east-1

📋 PASO 5: VERIFICAR CONFIGURACIÓN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Verificar credenciales
aws sts get-caller-identity

# Verificar tablas
aws dynamodb list-tables --region us-east-1

# Verificar Bedrock
aws bedrock list-foundation-models --region us-east-1 \\
  --query "modelSummaries[?contains(modelId, 'claude')].modelId"

📋 PASO 6: REINICIAR SERVICIOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Detener servicios actuales
pkill -f streamlit
pkill -f uvicorn

# Reiniciar con nuevas credenciales
source venv/bin/activate
nohup streamlit run src/ui/app.py --server.port 8501 --server.headless true > streamlit_output.log 2>&1 &
nohup uvicorn src.api.main:app --host 0.0.0.0 --port 8000 > api_output.log 2>&1 &

📋 PASO 7: PROBAR EL SISTEMA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Seed datos de prueba
python scripts/seed_data.py

# Probar sistema completo
python scripts/test_system.py

# Acceder a la UI
Abrir navegador en: http://localhost:8501

💰 COSTOS ESTIMADOS (AWS Free Tier)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- DynamoDB: GRATIS (25 GB, 25 WCU, 25 RCU)
- Bedrock: GRATIS primeros 3 meses (con límites)
- Total estimado: $0-10 USD/mes (uso moderado)

✅ ¡LISTO! Tu sistema estará completamente funcional.

""")
