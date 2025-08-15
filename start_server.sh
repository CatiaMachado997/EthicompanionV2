#!/bin/bash

# Script de inicialização do Ethic Companion
echo "🚀 Iniciando Ethic Companion..."

# Ativar ambiente virtual
source venv/bin/activate

# Configurar variáveis de ambiente
export WEAVIATE_API_KEY="minha-chave-secreta-dev"
export GOOGLE_API_KEY="AIzaSyC3KetzSrufPXNsvI49-YGFAYO9mhxBWao"
export TAVILY_API_KEY="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"

# Verificar se as variáveis estão configuradas
echo "✅ WEAVIATE_API_KEY: ${WEAVIATE_API_KEY:0:10}..."
echo "✅ GOOGLE_API_KEY: ${GOOGLE_API_KEY:0:10}..."
echo "✅ TAVILY_API_KEY: ${TAVILY_API_KEY:0:10}..."

# Iniciar o servidor
echo "🌐 Iniciando servidor FastAPI..."
python main.py
