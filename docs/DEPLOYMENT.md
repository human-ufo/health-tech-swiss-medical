# 🚀 Guía de Despliegue

## Despliegue en AWS

### 1. Configurar AWS CLI
```bash
aws configure
```

### 2. Habilitar AWS Bedrock
1. Ir a [AWS Bedrock Console](https://console.aws.amazon.com/bedrock/)
2. Navegar a "Model access"
3. Solicitar acceso a "Claude 3 Sonnet"

### 3. Desplegar Infraestructura
```bash
chmod +x infrastructure/scripts/setup_aws.sh
./infrastructure/scripts/setup_aws.sh
```

### 4. Build y Push Docker
```bash
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  862172028272.dkr.ecr.us-east-1.amazonaws.com

docker build -t health-tech-swiss-medical:latest .
docker tag health-tech-swiss-medical:latest \
  862172028272.dkr.ecr.us-east-1.amazonaws.com/health-tech-swiss-medical:latest
docker push 862172028272.dkr.ecr.us-east-1.amazonaws.com/health-tech-swiss-medical:latest
```

## Despliegue Local

### Con Docker Compose
```bash
cp .env.example .env
docker-compose up -d
```

### Sin Docker
```bash
# Terminal 1: API
uvicorn src.api.main:app --reload

# Terminal 2: Streamlit
streamlit run src/ui/app.py
```

## Verificación
```bash
curl http://localhost:8000/api/v1/health
```
