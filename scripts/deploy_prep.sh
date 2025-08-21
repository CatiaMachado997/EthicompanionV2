#!/bin/bash

# 🚀 Deploy Script para Ethic Companion V2
# Este script prepara o projeto para deployment no Google Cloud Run

echo "🌟 =========================================="
echo "🚀 Ethic Companion V2 - Deploy Preparation"
echo "🌟 =========================================="

# Verificar se estamos no diretório correto
if [ ! -f "main.py" ]; then
    echo "❌ Erro: Execute este script na raiz do projeto (onde está o main.py)"
    exit 1
fi

echo
echo "📋 Verificando configuração do projeto..."

# Verificar se os arquivos necessários existem
files_to_check=("Dockerfile" "Dockerfile.prod" "docker-compose.yml" "requirements.txt" "backend_app/core/config.py")
for file in "${files_to_check[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file encontrado"
    else
        echo "❌ $file não encontrado"
        exit 1
    fi
done

echo
echo "🔧 Verificando configuração de ambiente..."

# Verificar se o .env existe (para desenvolvimento)
if [ -f ".env" ]; then
    echo "✅ Arquivo .env encontrado (desenvolvimento local)"
else
    echo "⚠️  Arquivo .env não encontrado - usando .env.example como referência"
    if [ -f ".env.example" ]; then
        echo "📄 Para desenvolvimento local, copie .env.example para .env e configure as API keys"
    fi
fi

echo
echo "🐳 Construindo imagem Docker para produção..."

# Build da imagem Docker de produção
docker build -f Dockerfile.prod -t ethic-companion-v2:prod .

if [ $? -eq 0 ]; then
    echo "✅ Imagem Docker construída com sucesso"
else
    echo "❌ Erro ao construir imagem Docker"
    exit 1
fi

echo
echo "📊 Informações da imagem:"
docker images ethic-companion-v2:prod

echo
echo "🧪 Testando imagem Docker localmente..."
echo "💡 Para testar localmente:"
echo "   docker run -p 8000:8000 --env-file .env ethic-companion-v2:prod"

echo
echo "☁️  Próximos passos para deploy no Google Cloud:"
echo
echo "1. 🔐 Configurar segredos no Secret Manager:"
echo "   gcloud secrets create ethic-companion-google-api-key --data-file=<(echo 'SUA_GOOGLE_API_KEY')"
echo "   gcloud secrets create ethic-companion-tavily-api-key --data-file=<(echo 'SUA_TAVILY_API_KEY')"
echo "   gcloud secrets create ethic-companion-weaviate-api-key --data-file=<(echo 'SUA_WEAVIATE_API_KEY')"
echo
echo "2. 🏷️  Tag da imagem para Container Registry:"
echo "   docker tag ethic-companion-v2:prod gcr.io/SEU_PROJECT_ID/ethic-companion-v2:latest"
echo "   docker push gcr.io/SEU_PROJECT_ID/ethic-companion-v2:latest"
echo
echo "3. 🚀 Deploy no Cloud Run:"
echo "   gcloud run deploy ethic-companion-v2 \\"
echo "     --image gcr.io/SEU_PROJECT_ID/ethic-companion-v2:latest \\"
echo "     --platform managed \\"
echo "     --region us-central1 \\"
echo "     --allow-unauthenticated \\"
echo "     --set-env-vars GOOGLE_CLOUD_PROJECT=SEU_PROJECT_ID \\"
echo "     --port 8000"

echo
echo "🔧 Configuração atual do ambiente:"
echo "   📁 Diretório: $(pwd)"
echo "   🐍 Python: $(python --version 2>/dev/null || echo 'Python não encontrado')"
echo "   🐳 Docker: $(docker --version 2>/dev/null || echo 'Docker não encontrado')"

echo
echo "✅ Deploy preparation completo!"
echo "🌟 O projeto está pronto para produção!"
echo "🌟 =========================================="
