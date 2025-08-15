#!/bin/bash

# Script para deploy da aplicação Ethic Companion V2

# Configurações padrão
BACKEND_PORT=${BACKEND_PORT:-8000}
WEAVIATE_PORT=${WEAVIATE_PORT:-8080}
ENV_MODE=${ENV_MODE:-dev}
DOCKERFILE=${DOCKERFILE:-Dockerfile}

echo "🚀 Iniciando deploy do Ethic Companion V2..."
echo "📊 Configurações:"
echo "   - Modo: $ENV_MODE"
echo "   - Backend Port: $BACKEND_PORT"
echo "   - Weaviate Port: $WEAVIATE_PORT"
echo "   - Dockerfile: $DOCKERFILE"

# Verificar se o arquivo .env existe
if [ ! -f .env ]; then
    echo "❌ Arquivo .env não encontrado!"
    echo "📝 Criando arquivo .env de exemplo..."
    cp env_template.txt .env
    echo "⚠️  Configure suas API keys no arquivo .env antes de continuar"
    exit 1
fi

# Verificar se Docker está rodando
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker não está rodando. Inicie o Docker Desktop primeiro."
    exit 1
fi

# Escolher arquivo docker-compose baseado no modo
COMPOSE_FILE="docker-compose.yml"
if [ "$ENV_MODE" = "dev" ]; then
    COMPOSE_FILE="docker-compose.dev.yml"
fi

# Parar containers existentes
echo "🛑 Parando containers existentes..."
docker-compose -f $COMPOSE_FILE down

# Remover imagens antigas se solicitado
if [ "$1" = "--rebuild" ]; then
    echo "🧹 Removendo imagens antigas..."
    docker-compose -f $COMPOSE_FILE down --rmi all
fi

# Construir e iniciar os serviços
echo "🔨 Construindo e iniciando serviços..."
export BACKEND_PORT WEAVIATE_PORT DOCKERFILE
docker-compose -f $COMPOSE_FILE up --build -d

# Aguardar serviços ficarem prontos
echo "⏳ Aguardando serviços ficarem prontos..."
sleep 30

# Verificar status dos serviços
echo "📊 Verificando status dos serviços..."
docker-compose -f $COMPOSE_FILE ps

# Verificar saúde dos serviços
echo "🏥 Verificando saúde dos serviços..."

# Testar Weaviate
if curl -f http://localhost:$WEAVIATE_PORT/v1/.well-known/ready > /dev/null 2>&1; then
    echo "✅ Weaviate está funcionando na porta $WEAVIATE_PORT"
else
    echo "❌ Weaviate não está respondendo na porta $WEAVIATE_PORT"
fi

# Testar Backend
if curl -f http://localhost:$BACKEND_PORT/docs > /dev/null 2>&1; then
    echo "✅ Backend está funcionando na porta $BACKEND_PORT"
else
    echo "❌ Backend não está respondendo na porta $BACKEND_PORT"
fi

echo ""
echo "🎉 Deploy concluído!"
echo "📍 Serviços disponíveis:"
echo "   - Backend API: http://localhost:$BACKEND_PORT"
echo "   - Documentação API: http://localhost:$BACKEND_PORT/docs"
echo "   - Weaviate: http://localhost:$WEAVIATE_PORT"
echo ""
echo "📝 Para ver logs:"
echo "   docker-compose -f $COMPOSE_FILE logs -f"
echo ""
echo "🛑 Para parar:"
echo "   docker-compose -f $COMPOSE_FILE down"
echo ""
echo "🔧 Para usar portas diferentes:"
echo "   BACKEND_PORT=8001 WEAVIATE_PORT=8081 ./deploy.sh"
echo ""
echo "🏭 Para modo produção:"
echo "   ENV_MODE=prod DOCKERFILE=Dockerfile.prod ./deploy.sh"
