# 🏥 Sistema de Triaje Médico Inteligente - Swiss Medical Group

Sistema agéntico de inteligencia artificial para evaluación y priorización de pacientes en servicios de salud, desarrollado con LangChain, LangGraph y AWS Bedrock.

[![CI](https://github.com/humanufo-hash/health-tech-swiss-medical/actions/workflows/ci.yml/badge.svg)](https://github.com/humanufo-hash/health-tech-swiss-medical/actions/workflows/ci.yml)
[![CD](https://github.com/humanufo-hash/health-tech-swiss-medical/actions/workflows/cd.yml/badge.svg)](https://github.com/humanufo-hash/health-tech-swiss-medical/actions/workflows/cd.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📋 Descripción del Proyecto

Este proyecto implementa un **sistema multi-agente de IA** para realizar triaje médico automatizado, ayudando a priorizar pacientes según la severidad de sus síntomas y condiciones médicas. El sistema utiliza modelos de lenguaje avanzados (Claude 3 Sonnet via AWS Bedrock) orquestados con LangGraph para proporcionar evaluaciones médicas precisas y recomendaciones de acción.

### 🎯 Caso de Uso

**Contexto:** Swiss Medical Group necesita optimizar el proceso de triaje en sus centros de atención, reduciendo tiempos de espera y mejorando la asignación de recursos médicos.

**Solución:** Sistema agéntico que:
- Evalúa síntomas y signos vitales del paciente
- Consulta historial médico automáticamente
- Asigna nivel de prioridad según protocolos médicos
- Recomienda especialidad médica y estudios necesarios
- Identifica factores de riesgo y señales de alerta

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                     STREAMLIT UI                            │
│              (Interfaz de Usuario Web)                      │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                    FASTAPI REST API                         │
│              (Endpoints de Negocio)                         │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│              COORDINATOR AGENT (LangGraph)                  │
│         Orquesta el flujo multi-agente                      │
└──────┬──────────────┬──────────────┬───────────────────────┘
       │              │              │
   ┌───▼───┐     ┌───▼───┐     ┌───▼────┐
   │Triage │     │History│     │Recommend│
   │Agent  │     │Agent  │     │Agent    │
   └───┬───┘     └───┬───┘     └───┬────┘
       │             │              │
       └─────────────┴──────────────┘
                     │
        ┌────────────▼────────────┐
        │   AWS BEDROCK (Claude)  │
        │   LLM Backend           │
        └────────────┬────────────┘
                     │
        ┌────────────▼────────────┐
        │   AWS DYNAMODB          │
        │   Base de Datos NoSQL   │
        └─────────────────────────┘
```

## 🚀 Stack Tecnológico

### Backend & IA
- **Python 3.11+**: Lenguaje principal
- **FastAPI**: Framework web moderno y rápido
- **LangChain**: Framework para aplicaciones LLM
- **LangGraph**: Orquestación de agentes multi-agente
- **LangSmith**: Monitoreo y debugging de agentes
- **AWS Bedrock**: Servicio de LLM (Claude 3 Sonnet)

### Base de Datos & Cloud
- **AWS DynamoDB**: Base de datos NoSQL serverless
- **AWS ECR**: Registry de contenedores Docker
- **AWS CloudFormation**: Infraestructura como código

### Frontend & UI
- **Streamlit**: Framework para aplicaciones de datos interactivas

### DevOps & CI/CD
- **Docker**: Containerización
- **GitHub Actions**: CI/CD pipelines
- **pytest**: Testing framework
- **black, flake8, mypy**: Code quality tools

## 📁 Estructura del Proyecto

```
health-tech-swiss-medical/
├── .github/
│   └── workflows/          # CI/CD pipelines
│       ├── ci.yml          # Continuous Integration
│       ├── cd.yml          # Continuous Deployment
│       └── test.yml        # Tests automatizados
├── infrastructure/
│   ├── cloudformation/     # Templates de CloudFormation
│   └── scripts/            # Scripts de setup
├── src/
│   ├── agents/             # Agentes de IA
│   │   ├── base_agent.py
│   │   ├── triage_agent.py
│   │   └── coordinator_agent.py
│   ├── api/                # FastAPI application
│   │   ├── main.py
│   │   └── routes/
│   ├── models/             # Modelos de datos (Pydantic)
│   │   ├── patient.py
│   │   ├── triage.py
│   │   └── consultation.py
│   ├── services/           # Lógica de negocio
│   │   ├── dynamodb_service.py
│   │   ├── patient_service.py
│   │   └── consultation_service.py
│   ├── ui/                 # Streamlit UI
│   │   ├── app.py
│   │   └── pages/
│   └── config.py           # Configuración
├── tests/                  # Tests unitarios e integración
├── docker-compose.yml      # Orquestación local
├── Dockerfile              # Imagen Docker
├── requirements.txt        # Dependencias Python
└── README.md              # Este archivo
```

## 🛠️ Instalación y Configuración

### Prerrequisitos

- Python 3.11 o superior
- Cuenta AWS (Free Tier compatible)
- Git
- Docker (opcional)

### 1. Clonar el Repositorio

```bash
git clone git@github.com:humanufo-hash/health-tech-swiss-medical.git
cd health-tech-swiss-medical
```

### 2. Configurar Entorno Virtual

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configurar Variables de Entorno

```bash
cp .env.example .env
```

Editar `.env` con tus credenciales:

```env
# AWS Configuration
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=tu_access_key
AWS_SECRET_ACCESS_KEY=tu_secret_key
AWS_ACCOUNT_ID=862172028272

# AWS Bedrock
BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
BEDROCK_REGION=us-east-1

# LangSmith (Opcional)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=tu_langsmith_key
```

### 4. Configurar Infraestructura AWS

```bash
# Dar permisos de ejecución al script
chmod +x infrastructure/scripts/setup_aws.sh

# Ejecutar setup
./infrastructure/scripts/setup_aws.sh
```

**Importante:** Debes habilitar acceso a AWS Bedrock manualmente:
1. Ve a la [consola de AWS Bedrock](https://console.aws.amazon.com/bedrock/)
2. Navega a "Model access"
3. Solicita acceso a "Claude 3 Sonnet"
4. Espera aprobación (usualmente instantánea)

### 5. Crear Tablas DynamoDB

```bash
# Opción 1: Via CloudFormation (recomendado)
aws cloudformation deploy \
  --template-file infrastructure/cloudformation/dynamodb.yml \
  --stack-name swiss-medical-triage-stack \
  --region us-east-1

# Opción 2: Via Python
python -c "from src.services.dynamodb_service import DynamoDBService; DynamoDBService().create_tables()"
```

## 🚀 Ejecución

### Opción 1: Ejecución Local

#### Iniciar API

```bash
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

API disponible en: http://localhost:8000
Documentación interactiva: http://localhost:8000/docs

#### Iniciar UI Streamlit

```bash
streamlit run src/ui/app.py
```

UI disponible en: http://localhost:8501

### Opción 2: Docker Compose

```bash
docker-compose up -d
```

Servicios disponibles:
- API: http://localhost:8000
- Streamlit: http://localhost:8501
- DynamoDB Local: http://localhost:8002

## 📊 Uso del Sistema

### 1. Registrar un Paciente

**Via UI:**
1. Ir a "Gestión de Pacientes" → "Nuevo Paciente"
2. Completar formulario
3. Guardar

**Via API:**
```bash
curl -X POST "http://localhost:8000/api/v1/patients/" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Juan",
    "last_name": "Pérez",
    "date_of_birth": "1985-05-15",
    "gender": "male",
    "phone": "+541145678900",
    "allergies": ["Penicilina"],
    "chronic_conditions": ["Hipertensión"]
  }'
```

### 2. Realizar Evaluación de Triaje

**Via UI:**
1. Ir a "Evaluación de Triaje"
2. Ingresar ID del paciente
3. Agregar síntomas y signos vitales
4. Iniciar evaluación
5. Ver resultados con recomendaciones

**Via API:**
```bash
curl -X POST "http://localhost:8000/api/v1/triage/assess" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "PAT-XXXXXXXX",
    "symptoms": [
      {
        "name": "Dolor de pecho",
        "severity": 8,
        "duration_hours": 2
      }
    ],
    "vital_signs": {
      "temperature": 37.2,
      "blood_pressure": "140/90",
      "heart_rate": 95
    }
  }'
```

### 3. Consultar Historial

**Via UI:**
1. Ir a "Historial de Consultas y Triajes"
2. Buscar por ID de paciente
3. Ver evaluaciones previas

## 🧪 Testing

### Ejecutar Tests

```bash
# Todos los tests
pytest

# Con cobertura
pytest --cov=src --cov-report=html

# Solo tests unitarios
pytest tests/test_models.py tests/test_services.py

# Solo tests de API
pytest tests/test_api.py
```

### Tests de Integración

```bash
# Iniciar DynamoDB local
docker run -p 8000:8000 amazon/dynamodb-local

# Ejecutar tests de integración
pytest tests/integration/
```

## 🔄 CI/CD

El proyecto incluye pipelines de GitHub Actions:

### CI Pipeline (`.github/workflows/ci.yml`)
- ✅ Linting (flake8, black)
- ✅ Type checking (mypy)
- ✅ Tests unitarios
- ✅ Security scanning (Trivy)
- ✅ Build Docker image

### CD Pipeline (`.github/workflows/cd.yml`)
- 🚀 Deploy a AWS ECR
- 🗄️ Crear tablas DynamoDB
- 📦 Deploy de infraestructura

### Configurar Secrets en GitHub

En tu repositorio GitHub, ve a Settings → Secrets → Actions y agrega:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

## 📈 Monitoreo con LangSmith

LangSmith permite monitorear y debuggear los agentes de IA:

1. Crear cuenta en [LangSmith](https://smith.langchain.com/)
2. Obtener API key
3. Configurar en `.env`:
```env
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=tu_key
LANGCHAIN_PROJECT=swiss-medical-triage
```

4. Ver traces en el dashboard de LangSmith

## 🎯 Características Implementadas

### ✅ Requisitos Técnicos de la JD

- [x] **Python avanzado**: Uso de type hints, async/await, decoradores
- [x] **LangChain & LangGraph**: Agentes multi-agente orquestados
- [x] **LangSmith**: Integración para monitoreo (opcional)
- [x] **FastAPI**: API REST completa con documentación automática
- [x] **Microservicios**: Arquitectura modular y escalable
- [x] **AWS Cloud**: Bedrock, DynamoDB, ECR
- [x] **Git/GitHub**: Control de versiones y CI/CD
- [x] **Metodologías ágiles**: Estructura de proyecto profesional
- [x] **Bases de datos**: DynamoDB (NoSQL)
- [x] **Testing**: pytest con cobertura

### 🤖 Agentes Implementados

1. **Triage Agent**: Evalúa síntomas y asigna prioridad
2. **History Agent**: Consulta historial médico del paciente
3. **Coordinator Agent**: Orquesta el flujo con LangGraph

### 📊 Funcionalidades

- Gestión completa de pacientes (CRUD)
- Evaluación de triaje con IA
- Historial de consultas y triajes
- Recomendaciones médicas automatizadas
- Identificación de factores de riesgo
- Interfaz web intuitiva

## 🔐 Seguridad

- Variables de entorno para credenciales
- No se hardcodean API keys
- Validación de datos con Pydantic
- Security scanning en CI/CD
- AWS IAM roles y políticas

## 📝 Licencia

MIT License - Ver [LICENSE](LICENSE) para más detalles

## 👤 Autor

**Omar Mena**
- GitHub: [@humanufo-hash](https://github.com/humanufo-hash)
- AWS Account: 862172028272

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📞 Soporte

Para preguntas o soporte:
- Abrir un [Issue](https://github.com/humanufo-hash/health-tech-swiss-medical/issues)
- Contactar via GitHub

## 🙏 Agradecimientos

- Swiss Medical Group por la inspiración del caso de uso
- AWS por los servicios cloud
- LangChain por el framework de agentes
- Anthropic por Claude 3

---

**Desarrollado con ❤️ para Swiss Medical Group**
