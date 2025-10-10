# ⚡ Quick Start Guide

## 5 Minutos para Empezar

### 1. Clonar y Setup (1 min)
```bash
git clone git@github.com:humanufo-hash/health-tech-swiss-medical.git
cd health-tech-swiss-medical
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configurar AWS (2 min)
```bash
cp .env.example .env
# Editar .env con tus credenciales AWS
nano .env
```

### 3. Crear Tablas DynamoDB (1 min)
```bash
./infrastructure/scripts/setup_aws.sh
```

### 4. Iniciar Aplicación (1 min)
```bash
# Terminal 1
uvicorn src.api.main:app --reload

# Terminal 2
streamlit run src/ui/app.py
```

### 5. Usar la Aplicación
- **API**: http://localhost:8000/docs
- **UI**: http://localhost:8501

## Primer Uso

1. **Crear Paciente**: Ir a "Gestión de Pacientes" → Registrar
2. **Evaluar Triaje**: Ir a "Evaluación de Triaje" → Ingresar síntomas
3. **Ver Resultados**: Sistema muestra nivel de prioridad y recomendaciones

## Troubleshooting Rápido

**Error de AWS credentials:**
```bash
aws configure
```

**Error de Bedrock:**
- Habilitar modelo en consola AWS Bedrock

**Error de DynamoDB:**
```bash
python -c "from src.services.dynamodb_service import DynamoDBService; DynamoDBService().create_tables()"
```

## Documentación Completa
Ver [README.md](README.md) para guía detallada.
