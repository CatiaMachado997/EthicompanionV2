#!/bin/bash

# Script para acesso seguro à aplicação na Cloud Run
# Este script configura autenticação e abre a aplicação no browser

echo "🔐 Configurando acesso seguro à aplicação..."

# Verificar se está logado no gcloud
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q "catiasofiafmachado@ethicompanion.com"; then
    echo "❌ Você não está logado com a conta correta."
    echo "Por favor, execute: gcloud auth login catiasofiafmachado@ethicompanion.com"
    exit 1
fi

# URLs dos serviços
FRONTEND_URL="https://ethic-companion-frontend-243140067122.us-central1.run.app"
BACKEND_URL="https://ethic-companion-backend-243140067122.us-central1.run.app"

echo "✅ Conta autenticada: catiasofiafmachado@ethicompanion.com"
echo "🌐 Frontend URL: $FRONTEND_URL"
echo "🔧 Backend URL: $BACKEND_URL"

# Obter token de acesso
echo "🔑 Obtendo token de acesso..."
ACCESS_TOKEN=$(gcloud auth print-identity-token)

if [ -z "$ACCESS_TOKEN" ]; then
    echo "❌ Erro ao obter token de acesso"
    exit 1
fi

echo "✅ Token obtido com sucesso"

# Testar acesso ao backend
echo "🧪 Testando acesso ao backend..."
BACKEND_RESPONSE=$(curl -s -w "%{http_code}" -H "Authorization: Bearer $ACCESS_TOKEN" "$BACKEND_URL/chat" -X POST -H "Content-Type: application/json" -d '{"text":"test"}')

if [[ "$BACKEND_RESPONSE" == *"200"* ]]; then
    echo "✅ Backend acessível com autenticação"
else
    echo "⚠️  Backend status: $BACKEND_RESPONSE"
fi

# Testar acesso ao frontend
echo "🧪 Testando acesso ao frontend..."
FRONTEND_RESPONSE=$(curl -s -w "%{http_code}" -H "Authorization: Bearer $ACCESS_TOKEN" "$FRONTEND_URL" -o /dev/null)

if [[ "$FRONTEND_RESPONSE" == "200" ]]; then
    echo "✅ Frontend acessível com autenticação"
    echo ""
    echo "🚀 Para acessar sua aplicação:"
    echo "1. Abra seu browser"
    echo "2. Certifique-se de estar logado com: catiasofiafmachado@ethicompanion.com"
    echo "3. Acesse: $FRONTEND_URL"
    echo ""
    echo "🔒 Sua aplicação está segura e acessível apenas para você!"
else
    echo "⚠️  Frontend status: $FRONTEND_RESPONSE"
fi

# Abrir no browser (opcional)
read -p "🌐 Deseja abrir a aplicação no browser agora? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    open "$FRONTEND_URL"
fi
