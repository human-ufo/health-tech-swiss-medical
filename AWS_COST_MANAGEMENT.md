# 💰 Gestión de Costos AWS

## 🛑 Pausar Sistema para Evitar Costos

### Opción 1: Pausar Manualmente (Recomendado)

#### 1. **Deshabilitar Bedrock** (CRÍTICO - Principal fuente de costos)
```
1. Ir a: https://console.aws.amazon.com/bedrock/
2. Región: us-east-1
3. Click en "Model access"
4. Click en "Manage model access"
5. DESMARCAR todos los modelos (especialmente Claude)
6. Click en "Save changes"
```

**Ahorro: ~$100-500/mes** (dependiendo del uso)

#### 2. **Desactivar Access Keys** (Previene uso accidental)
```bash
# En AWS CloudShell
aws iam list-access-keys --user-name swiss-medical-dev

# Para cada access key:
aws iam update-access-key \
    --user-name swiss-medical-dev \
    --access-key-id AKIA... \
    --status Inactive
```

**Ahorro: Previene costos no autorizados**

#### 3. **DynamoDB** (Opcional - Sin uso = Sin costo)
Las tablas con `PAY_PER_REQUEST` **NO tienen costo fijo**.
Solo pagas por:
- Lecturas: $0.25 por millón
- Escrituras: $1.25 por millón
- Almacenamiento: $0.25 por GB/mes

**Si NO usas las tablas, NO hay costo.**

Para eliminar si deseas:
```bash
aws dynamodb delete-table --table-name health-tech-patients --region us-east-1
aws dynamodb delete-table --table-name health-tech-consultations --region us-east-1
aws dynamodb delete-table --table-name health-tech-triage --region us-east-1
```

#### 4. **ECR Repository** (Opcional)
Primeras 500 MB gratis, luego $0.10/GB/mes.

Para eliminar:
```bash
aws ecr delete-repository \
    --repository-name health-tech-swiss-medical \
    --region us-east-1 \
    --force
```

---

### Opción 2: Script Automatizado

```bash
# Ejecutar en AWS CloudShell
bash scripts/pause_aws.sh
```

Este script te guiará paso a paso.

---

## 💵 Costos Actuales Estimados

### Con Sistema Activo (uso moderado)
| Servicio | Costo Mensual | Notas |
|----------|---------------|-------|
| **Bedrock (Claude)** | $0-100 | Depende de tokens usados |
| **DynamoDB** | $0-5 | PAY_PER_REQUEST, solo por uso |
| **ECR** | $0 | Primeros 500 MB gratis |
| **IAM/CloudWatch** | $0 | Gratis |
| **TOTAL** | **$0-105/mes** | Varía según uso |

### Con Sistema Pausado
| Servicio | Costo Mensual | Estado |
|----------|---------------|--------|
| **Bedrock** | $0 | Deshabilitado |
| **DynamoDB** | $0 | Sin uso = sin costo |
| **ECR** | $0 | Sin imágenes |
| **IAM** | $0 | Gratis |
| **TOTAL** | **$0/mes** | ✅ |

---

## ▶️ Reanudar Sistema

### Opción 1: Manual

1. **Reactivar Access Keys**
```bash
aws iam update-access-key \
    --user-name swiss-medical-dev \
    --access-key-id AKIA... \
    --status Active
```

2. **Habilitar Bedrock**
- Ir a consola Bedrock
- Habilitar Claude 3 Sonnet

3. **Verificar Tablas DynamoDB**
```bash
aws dynamodb list-tables --region us-east-1
```

4. **Iniciar Servicios Locales**
```bash
cd "/home/human/Documents/gen ai/proyecto 1 - gen ai"
source venv/bin/activate
nohup uvicorn src.api.main:app --host 0.0.0.0 --port 8000 > api_output.log 2>&1 &
nohup streamlit run src/ui/app.py --server.port 8501 --server.headless true > streamlit_output.log 2>&1 &
```

### Opción 2: Script Automatizado

```bash
bash scripts/resume_aws.sh
```

---

## 📊 Monitorear Costos

### Ver Costos Actuales
```
https://console.aws.amazon.com/billing/
```

### Configurar Alertas de Costo

1. Ir a: https://console.aws.amazon.com/billing/home#/budgets
2. Click "Create budget"
3. Seleccionar "Cost budget"
4. Configurar:
   - Budget amount: $10/mes
   - Alert threshold: 80% ($8)
   - Email notification

---

## 🎯 Recomendaciones

### Para Desarrollo/Testing
✅ **Pausar Bedrock** cuando no estés usando
✅ **Mantener DynamoDB** (sin costo si no hay uso)
✅ **Desactivar access keys** cuando no desarrolles

### Para Producción
✅ Usar **Reserved Capacity** en DynamoDB (ahorro 50-75%)
✅ Configurar **CloudWatch Alarms** para uso de Bedrock
✅ Implementar **caching** para reducir llamadas a Bedrock

---

## 🚨 Eliminar TODO (Limpieza Completa)

**⚠️ ADVERTENCIA: Esto eliminará TODOS los recursos y datos**

```bash
# Eliminar tablas DynamoDB
aws dynamodb delete-table --table-name health-tech-patients --region us-east-1
aws dynamodb delete-table --table-name health-tech-consultations --region us-east-1
aws dynamodb delete-table --table-name health-tech-triage --region us-east-1

# Eliminar ECR repository
aws ecr delete-repository --repository-name health-tech-swiss-medical --region us-east-1 --force

# Eliminar access keys
aws iam delete-access-key --user-name swiss-medical-dev --access-key-id AKIA...

# Desadjuntar política
aws iam detach-user-policy \
    --user-name swiss-medical-dev \
    --policy-arn arn:aws:iam::862172028272:policy/SwissMedicalTriagePolicy

# Eliminar usuario
aws iam delete-user --user-name swiss-medical-dev

# Eliminar política
aws iam delete-policy --policy-arn arn:aws:iam::862172028272:policy/SwissMedicalTriagePolicy
```

---

## 📞 Soporte

Si tienes dudas sobre costos:
- AWS Cost Explorer: https://console.aws.amazon.com/cost-management/
- AWS Support: https://console.aws.amazon.com/support/
