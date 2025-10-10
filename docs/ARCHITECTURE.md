# 🏗️ Arquitectura del Sistema

## Visión General

El Sistema de Triaje Médico Inteligente utiliza una arquitectura de microservicios basada en agentes de IA, diseñada para ser escalable, mantenible y desplegable en AWS.

## Componentes Principales

### 1. Capa de Presentación

#### Streamlit UI (`src/ui/`)
- **Propósito**: Interfaz web interactiva para usuarios finales
- **Tecnología**: Streamlit
- **Páginas**:
  - Home: Dashboard principal
  - Patient Management: CRUD de pacientes
  - Triage Assessment: Evaluación de triaje
  - Consultation History: Historial de consultas

### 2. Capa de API

#### FastAPI REST API (`src/api/`)
- **Propósito**: Exponer funcionalidades del sistema via HTTP
- **Endpoints**:
  - `/api/v1/health`: Health checks
  - `/api/v1/patients`: Gestión de pacientes
  - `/api/v1/triage`: Evaluación de triaje
  - `/api/v1/consultations`: Gestión de consultas

### 3. Capa de Agentes IA

#### Coordinator Agent (LangGraph)
```python
Flujo del Coordinador:
┌─────────────────┐
│  Triage Request │
└────────┬────────┘
         │
    ┌────▼─────┐
    │  Fetch   │
    │ Patient  │
    │ History  │
    └────┬─────┘
         │
    ┌────▼─────┐
    │ Perform  │
    │  Triage  │
    │Assessment│
    └────┬─────┘
         │
    ┌────▼─────┐
    │   Save   │
    │ Results  │
    └────┬─────┘
         │
    ┌────▼─────┐
    │  Return  │
    │ Response │
    └──────────┘
```

#### Triage Agent
- **Modelo**: Claude 3 Sonnet (AWS Bedrock)
- **Función**: Evaluar síntomas y asignar prioridad
- **Entrada**: Síntomas, signos vitales, historial
- **Salida**: Nivel de triaje, recomendaciones

### 4. Capa de Servicios

#### Patient Service
- Gestión de pacientes
- Cálculo de edad
- Historial médico

#### Consultation Service
- Gestión de consultas
- Actualización de estados

#### DynamoDB Service
- Abstracción de operaciones DynamoDB
- CRUD genérico
- Queries por índices

### 5. Capa de Datos

#### DynamoDB Tables

**Tabla: health-tech-patients**
```
Primary Key: patient_id (String)
Attributes:
  - first_name, last_name
  - date_of_birth, gender, blood_type
  - phone, email, address
  - allergies[], chronic_conditions[], current_medications[]
  - created_at, updated_at, is_active
```

**Tabla: health-tech-consultations**
```
Primary Key: consultation_id (String)
GSI: patient_id-index
Attributes:
  - patient_id
  - chief_complaint, symptoms_description
  - status, assigned_doctor, assigned_specialty
  - triage_result{}
  - created_at, updated_at, completed_at
```

**Tabla: health-tech-triage**
```
Primary Key: triage_id (String)
GSI: patient_id-index
Attributes:
  - patient_id
  - triage_level, priority_score
  - assessment_summary, recommended_action
  - recommended_specialty, recommended_tests[]
  - risk_factors[], warning_signs[]
  - created_at
```

## Flujo de Datos

### Flujo de Evaluación de Triaje

```
Usuario (Streamlit)
    │
    ▼
FastAPI Endpoint (/api/v1/triage/assess)
    │
    ▼
Coordinator Agent (LangGraph)
    │
    ├──▶ Patient Service → DynamoDB (get patient)
    │
    ├──▶ Triage Agent → AWS Bedrock (Claude)
    │
    └──▶ DynamoDB Service → DynamoDB (save triage)
    │
    ▼
Response (TriageResponse)
    │
    ▼
Usuario (Streamlit)
```

## Patrones de Diseño

### 1. Service Layer Pattern
Separación entre lógica de negocio (services) y acceso a datos (DynamoDB)

### 2. Repository Pattern
`DynamoDBService` actúa como repositorio genérico

### 3. Agent Pattern
Agentes especializados con responsabilidades únicas

### 4. Coordinator Pattern
`CoordinatorAgent` orquesta múltiples agentes con LangGraph

### 5. Factory Pattern
Creación de agentes con configuración centralizada

## Escalabilidad

### Horizontal Scaling
- API stateless, puede escalar horizontalmente
- DynamoDB auto-scaling con PAY_PER_REQUEST
- Agentes sin estado compartido

### Vertical Scaling
- Ajuste de recursos de contenedores
- Optimización de modelos LLM

### Caching
- Potencial para Redis/ElastiCache
- Cache de historiales de pacientes

## Seguridad

### Autenticación & Autorización
- AWS IAM roles para servicios
- Potencial para Cognito/OAuth2

### Encriptación
- DynamoDB encryption at rest
- HTTPS/TLS en tránsito

### Validación
- Pydantic models para validación de datos
- Input sanitization

## Monitoreo

### Logs
- CloudWatch Logs
- Structured logging con Python logging

### Metrics
- CloudWatch Metrics
- LangSmith para agentes

### Tracing
- LangSmith tracing
- Potencial para AWS X-Ray

## Despliegue

### Containerización
```
Docker Image
├── Python 3.11 base
├── Dependencies (requirements.txt)
├── Application code (src/)
└── Configuration (.env)
```

### AWS Services
- **ECS/Fargate**: Contenedores serverless
- **ECR**: Registry de imágenes
- **DynamoDB**: Base de datos
- **Bedrock**: LLM inference
- **CloudFormation**: IaC

### CI/CD Pipeline
```
GitHub Push
    │
    ▼
GitHub Actions (CI)
    ├─▶ Lint & Test
    ├─▶ Security Scan
    └─▶ Build Docker
    │
    ▼
GitHub Actions (CD)
    ├─▶ Push to ECR
    ├─▶ Deploy Infrastructure
    └─▶ Update Services
```

## Mejoras Futuras

### Corto Plazo
- [ ] Autenticación de usuarios
- [ ] Rate limiting
- [ ] Cache de resultados

### Mediano Plazo
- [ ] Más agentes especializados
- [ ] Integración con sistemas hospitalarios
- [ ] Notificaciones en tiempo real

### Largo Plazo
- [ ] Machine Learning personalizado
- [ ] Análisis predictivo
- [ ] Multi-región deployment
