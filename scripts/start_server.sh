#!/bin/bash

# Script de inicialização do Ethic Companion
echo "🚀 Iniciando Ethic Companion..."

# Ativar ambiente virtual
source venv/bin/activate

# Configurar variáveis de ambiente
export WEAVIATE_API_KEY="minha-chave-secreta-dev"
# Load environment variables from .env file
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
    echo "✅ Variáveis carregadas do arquivo .env"
else
    echo "❌ Arquivo .env não encontrado! Crie um com as API keys."
    exit 1
fi

# Verificar se as variáveis estão configuradas
echo "✅ WEAVIATE_API_KEY: ${WEAVIATE_API_KEY:0:10}..."
echo "✅ GOOGLE_API_KEY: ${GOOGLE_API_KEY:0:10}..."
echo "✅ TAVILY_API_KEY: ${TAVILY_API_KEY:0:10}..."

# Iniciar o servidor
echo "🌐 Iniciando servidor FastAPI..."
python main.py
