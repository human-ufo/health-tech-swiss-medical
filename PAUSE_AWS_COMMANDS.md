# 🛑 Comandos para Pausar AWS (Ejecutar en CloudShell)

## ⚠️ IMPORTANTE: Ejecuta estos comandos en AWS CloudShell

### 1. Desactivar Access Keys (Previene uso accidental)

```bash
# Listar access keys
aws iam list-access-keys --user-name swiss-medical-dev

# Desactivar cada access key (reemplaza AKIA... con tu key)
aws iam update-access-key \
    --user-name swiss-medical-dev \
    --access-key-id AKIA4RPLVDVYNGS2P5HJ \
    --status Inactive

# Verificar
aws iam list-access-keys --user-name swiss-medical-dev
```

### 2. Deshabilitar Bedrock (CRÍTICO - Principal fuente de costos)

**Esto DEBE hacerse manualmente en la consola:**

1. Ir a: https://console.aws.amazon.com/bedrock/
2. Región: **us-east-1**
3. Click en "**Model access**" (menú izquierdo)
4. Click en "**Manage model access**"
5. **DESMARCAR** todos los modelos (especialmente Claude 3 Sonnet)
6. Click en "**Save changes**"

### 3. (Opcional) Eliminar Datos de DynamoDB

**⚠️ Solo si quieres eliminar los datos de prueba:**

```bash
# Eliminar tablas (OPCIONAL - sin uso = sin costo)
aws dynamodb delete-table --table-name health-tech-patients --region us-east-1
aws dynamodb delete-table --table-name health-tech-consultations --region us-east-1
aws dynamodb delete-table --table-name health-tech-triage --region us-east-1

# Verificar
aws dynamodb list-tables --region us-east-1
```

**Nota:** Las tablas DynamoDB con PAY_PER_REQUEST NO tienen costo fijo. Solo pagas por uso. Si no las usas, no hay costo.

### 4. (Opcional) Eliminar ECR Repository

```bash
# Eliminar repositorio ECR
aws ecr delete-repository \
    --repository-name health-tech-swiss-medical \
    --region us-east-1 \
    --force

# Verificar
aws ecr describe-repositories --region us-east-1
```

---

## ✅ Verificación Final

```bash
echo "=== ESTADO DE RECURSOS AWS ==="
echo ""
echo "Access Keys:"
aws iam list-access-keys --user-name swiss-medical-dev --query 'AccessKeyMetadata[].{KeyId:AccessKeyId,Status:Status}' --output table
echo ""
echo "Tablas DynamoDB:"
aws dynamodb list-tables --region us-east-1 --output table
echo ""
echo "Repositorios ECR:"
aws ecr describe-repositories --region us-east-1 --query 'repositories[].repositoryName' --output table 2>/dev/null || echo "Sin repositorios"
echo ""
echo "✅ Verificación completada"
```

---

## 💰 Costos Después de Pausar

| Servicio | Estado | Costo |
|----------|--------|-------|
| Bedrock | Deshabilitado | $0 |
| DynamoDB | Sin uso | $0 |
| ECR | Sin imágenes | $0 |
| IAM | Activo | $0 (gratis) |
| **TOTAL** | | **$0/mes** |

---

## ▶️ Para Reanudar Después

1. **Reactivar access keys:**
```bash
aws iam update-access-key \
    --user-name swiss-medical-dev \
    --access-key-id AKIA4RPLVDVYNGS2P5HJ \
    --status Active
```

2. **Habilitar Bedrock en consola** (mismo proceso que antes)

3. **Recrear tablas si fueron eliminadas:**
```bash
bash infrastructure/scripts/setup_aws.sh
```

4. **Iniciar servicios locales:**
```bash
cd "/home/human/Documents/gen ai/proyecto 1 - gen ai"
source venv/bin/activate
nohup uvicorn src.api.main:app --host 0.0.0.0 --port 8000 > api_output.log 2>&1 &
nohup streamlit run src/ui/app.py --server.port 8501 --server.headless true > streamlit_output.log 2>&1 &
```
