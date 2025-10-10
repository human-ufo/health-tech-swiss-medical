# 🚀 Comandos para AWS CloudShell

Copia y pega estos comandos uno por uno en tu AWS CloudShell.

## 📋 PASO 1: Crear Usuario IAM

```bash
# Crear usuario
aws iam create-user --user-name swiss-medical-dev
```

## 📋 PASO 2: Crear Política de Permisos

```bash
# Obtener Account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
echo "Account ID: $ACCOUNT_ID"

# Crear archivo de política
cat > /tmp/policy.json <<'EOF'
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "dynamodb:*"
            ],
            "Resource": [
                "arn:aws:dynamodb:*:*:table/health-tech-*"
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
                "logs:*"
            ],
            "Resource": "*"
        }
    ]
}
EOF

# Crear política
aws iam create-policy \
    --policy-name SwissMedicalTriagePolicy \
    --policy-document file:///tmp/policy.json
```

## 📋 PASO 3: Adjuntar Política al Usuario

```bash
# Adjuntar política
POLICY_ARN="arn:aws:iam::${ACCOUNT_ID}:policy/SwissMedicalTriagePolicy"
aws iam attach-user-policy \
    --user-name swiss-medical-dev \
    --policy-arn $POLICY_ARN
```

## 📋 PASO 4: Crear Access Keys (IMPORTANTE)

```bash
# Crear access key y guardar
aws iam create-access-key --user-name swiss-medical-dev --output json | tee /tmp/credentials.json

# Mostrar credenciales en formato .env
echo ""
echo "=== COPIAR ESTAS CREDENCIALES A TU .env LOCAL ==="
cat /tmp/credentials.json | jq -r '"AWS_ACCESS_KEY_ID=" + .AccessKey.AccessKeyId'
cat /tmp/credentials.json | jq -r '"AWS_SECRET_ACCESS_KEY=" + .AccessKey.SecretAccessKey'
echo "AWS_REGION=us-east-1"
echo "AWS_ACCOUNT_ID=$ACCOUNT_ID"
echo "BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0"
echo "BEDROCK_REGION=us-east-1"
echo "=================================================="
```

## 📋 PASO 5: Crear Tabla DynamoDB - Pacientes

```bash
aws dynamodb create-table \
    --table-name health-tech-patients \
    --attribute-definitions AttributeName=patient_id,AttributeType=S \
    --key-schema AttributeName=patient_id,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST \
    --region us-east-1 \
    --tags Key=Project,Value=SwissMedicalTriage
```

## 📋 PASO 6: Crear Tabla DynamoDB - Consultas

```bash
aws dynamodb create-table \
    --table-name health-tech-consultations \
    --attribute-definitions \
        AttributeName=consultation_id,AttributeType=S \
        AttributeName=patient_id,AttributeType=S \
    --key-schema AttributeName=consultation_id,KeyType=HASH \
    --global-secondary-indexes \
        "IndexName=patient_id-index,KeySchema=[{AttributeName=patient_id,KeyType=HASH}],Projection={ProjectionType=ALL}" \
    --billing-mode PAY_PER_REQUEST \
    --region us-east-1 \
    --tags Key=Project,Value=SwissMedicalTriage
```

## 📋 PASO 7: Crear Tabla DynamoDB - Triaje

```bash
aws dynamodb create-table \
    --table-name health-tech-triage \
    --attribute-definitions \
        AttributeName=triage_id,AttributeType=S \
        AttributeName=patient_id,AttributeType=S \
    --key-schema AttributeName=triage_id,KeyType=HASH \
    --global-secondary-indexes \
        "IndexName=patient_id-index,KeySchema=[{AttributeName=patient_id,KeyType=HASH}],Projection={ProjectionType=ALL}" \
    --billing-mode PAY_PER_REQUEST \
    --region us-east-1 \
    --tags Key=Project,Value=SwissMedicalTriage
```

## 📋 PASO 8: Verificar Tablas Creadas

```bash
# Listar tablas
aws dynamodb list-tables --region us-east-1

# Ver detalles de cada tabla
aws dynamodb describe-table --table-name health-tech-patients --region us-east-1 --query 'Table.TableStatus'
aws dynamodb describe-table --table-name health-tech-consultations --region us-east-1 --query 'Table.TableStatus'
aws dynamodb describe-table --table-name health-tech-triage --region us-east-1 --query 'Table.TableStatus'
```

## 📋 PASO 9: Crear ECR Repository (Opcional)

```bash
aws ecr create-repository \
    --repository-name health-tech-swiss-medical \
    --region us-east-1 \
    --image-scanning-configuration scanOnPush=true \
    --tags Key=Project,Value=SwissMedicalTriage
```

## 📋 PASO 10: Verificar Modelos Bedrock Disponibles

```bash
# Listar modelos de Claude disponibles
aws bedrock list-foundation-models \
    --region us-east-1 \
    --query "modelSummaries[?contains(modelId, 'claude')].{ID:modelId,Name:modelName}" \
    --output table
```

## ✅ VERIFICACIÓN FINAL

```bash
echo "=== RESUMEN DE CONFIGURACIÓN ==="
echo ""
echo "Usuario IAM:"
aws iam get-user --user-name swiss-medical-dev --query 'User.UserName' --output text
echo ""
echo "Tablas DynamoDB:"
aws dynamodb list-tables --region us-east-1 --query 'TableNames' --output table
echo ""
echo "ECR Repository:"
aws ecr describe-repositories --region us-east-1 --query 'repositories[?repositoryName==`health-tech-swiss-medical`].repositoryUri' --output text
echo ""
echo "✅ Configuración completada!"
```

## 🔐 GUARDAR CREDENCIALES

```bash
# Ver credenciales nuevamente
cat /tmp/credentials.json | jq -r '"AWS_ACCESS_KEY_ID=" + .AccessKey.AccessKeyId'
cat /tmp/credentials.json | jq -r '"AWS_SECRET_ACCESS_KEY=" + .AccessKey.SecretAccessKey'
echo "AWS_REGION=us-east-1"
echo "AWS_ACCOUNT_ID=$ACCOUNT_ID"
```

---

## ⚠️ IMPORTANTE: HABILITAR AWS BEDROCK

**Esto NO se puede hacer desde CLI, debes hacerlo manualmente:**

1. Ir a: https://console.aws.amazon.com/bedrock/
2. Región: **us-east-1** (N. Virginia)
3. Click en "Model access" (menú izquierdo)
4. Click en "Manage model access"
5. Buscar "**Anthropic - Claude 3 Sonnet**"
6. Marcar el checkbox
7. Click en "Request model access"
8. Esperar aprobación (usualmente instantánea)

**Sin este paso, los agentes de IA NO funcionarán.**

---

## 📝 PRÓXIMOS PASOS

1. ✅ Copiar las credenciales mostradas
2. ✅ Pegar en tu archivo `.env` local
3. ✅ Habilitar Bedrock en la consola web
4. ✅ Reiniciar servicios locales:
   ```bash
   pkill -f streamlit && pkill -f uvicorn
   cd "/home/human/Documents/gen ai/proyecto 1 - gen ai"
   source venv/bin/activate
   nohup streamlit run src/ui/app.py --server.port 8501 --server.headless true > streamlit_output.log 2>&1 &
   nohup uvicorn src.api.main:app --host 0.0.0.0 --port 8000 > api_output.log 2>&1 &
   ```
5. ✅ Probar el sistema: `python scripts/test_system.py`
