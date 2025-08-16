#!/bin/bash

# 🚀 Script de Deploy Automático para Ethic Companion V2
# Execute este script DEPOIS de habilitar billing no projeto ethic-companion-2025

echo "🌟 =========================================="
echo "🚀 Ethic Companion V2 - Deploy Automático"
echo "🌟 =========================================="

# Verificar se estamos no projeto correto
PROJECT_ID=$(gcloud config get-value project)
if [ "$PROJECT_ID" != "ethic-companion-2025" ]; then
    echo "❌ Projeto incorreto. Configurando projeto correto..."
    gcloud config set project ethic-companion-2025
fi

echo "📋 Projeto atual: $(gcloud config get-value project)"

# Verificar se as APIs estão habilitadas
echo
echo "🔧 Habilitando APIs necessárias..."
gcloud services enable cloudbuild.googleapis.com run.googleapis.com secretmanager.googleapis.com artifactregistry.googleapis.com

if [ $? -ne 0 ]; then
    echo "❌ Erro ao habilitar APIs. Verifique se o billing está habilitado:"
    echo "   https://console.cloud.google.com/billing/projects"
    exit 1
fi

echo "✅ APIs habilitadas com sucesso!"

# Criar secrets (se não existirem)
echo
echo "🔐 Configurando secrets..."

# Verificar se o ficheiro .env existe
if [ ! -f ".env" ]; then
    echo "❌ Ficheiro .env não encontrado!"
    echo "📝 Crie um ficheiro .env com suas API keys:"
    echo "   GOOGLE_API_KEY=sua_google_api_key"
    echo "   TAVILY_API_KEY=sua_tavily_api_key"
    echo "   WEAVIATE_API_KEY=sua_weaviate_api_key"
    exit 1
fi

# Carregar variáveis do .env
set -a
source .env
set +a

# Criar secrets se não existirem
create_secret_if_not_exists() {
    local secret_name=$1
    local env_var=$2
    local value=${!env_var}
    
    if [ -z "$value" ] || [ "$value" = "your_${env_var,,}_here" ]; then
        echo "⚠️  $env_var não está configurada no .env"
        return 1
    fi
    
    # Verificar se o secret já existe
    if gcloud secrets describe $secret_name >/dev/null 2>&1; then
        echo "✅ Secret $secret_name já existe"
    else
        echo "🔐 Criando secret $secret_name..."
        echo "$value" | gcloud secrets create $secret_name --data-file=-
        if [ $? -eq 0 ]; then
            echo "✅ Secret $secret_name criado com sucesso"
        else
            echo "❌ Erro ao criar secret $secret_name"
            return 1
        fi
    fi
}

create_secret_if_not_exists "ethic-companion-google-api-key" "GOOGLE_API_KEY"
create_secret_if_not_exists "ethic-companion-tavily-api-key" "TAVILY_API_KEY"
create_secret_if_not_exists "ethic-companion-weaviate-api-key" "WEAVIATE_API_KEY"

echo
echo "🚀 Fazendo deploy para Cloud Run..."

# Deploy para Cloud Run
gcloud run deploy ethic-companion-backend \
  --source . \
  --platform managed \
  --region europe-west1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_CLOUD_PROJECT=ethic-companion-2025 \
  --set-secrets GOOGLE_API_KEY=ethic-companion-google-api-key:latest,TAVILY_API_KEY=ethic-companion-tavily-api-key:latest,WEAVIATE_API_KEY=ethic-companion-weaviate-api-key:latest \
  --port 8000 \
  --memory 1Gi \
  --cpu 1 \
  --timeout 300

if [ $? -eq 0 ]; then
    echo
    echo "🎉 Deploy concluído com sucesso!"
    echo
    echo "📋 Para obter o URL do serviço:"
    echo "   gcloud run services describe ethic-companion-backend --platform managed --region europe-west1 --format 'value(status.url)'"
    echo
    echo "🧪 Para testar o serviço:"
    echo "   SERVICE_URL=\$(gcloud run services describe ethic-companion-backend --platform managed --region europe-west1 --format 'value(status.url)')"
    echo "   curl \$SERVICE_URL/docs"
else
    echo "❌ Erro no deploy. Verifique os logs acima."
    exit 1
fi

echo
echo "✅ Ethic Companion V2 está agora online! 🎉"
echo "🌟 =========================================="
