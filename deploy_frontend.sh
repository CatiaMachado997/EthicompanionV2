#!/bin/bash

# Deploy do Frontend Next.js para Cloud Run
# Este script faz o deploy do frontend após o backend estar pronto

echo "🚀 Iniciando deploy do Frontend Ethic Companion V2..."

# Verificar se o backend está funcionando
echo "📡 Verificando se o backend está ativo..."
BACKEND_URL=$(gcloud run services describe ethic-companion-backend --region=us-central1 --format="value(status.url)" 2>/dev/null)

if [ -z "$BACKEND_URL" ]; then
    echo "❌ Backend não encontrado. Deploy do backend primeiro!"
    exit 1
fi

echo "✅ Backend encontrado: $BACKEND_URL"

# Deploy do frontend
echo "🔧 Fazendo deploy do frontend..."
gcloud run deploy ethic-companion-frontend \
    --source . \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --port 3000 \
    --memory 512Mi \
    --cpu 0.5 \
    --max-instances 50 \
    --set-env-vars="BACKEND_URL=$BACKEND_URL,NODE_ENV=production" \
    --dockerfile=Dockerfile.frontend

echo "🎉 Deploy do frontend concluído!"

# Mostrar URLs
echo ""
echo "📋 URLs da aplicação:"
echo "Backend:  $BACKEND_URL"
FRONTEND_URL=$(gcloud run services describe ethic-companion-frontend --region=us-central1 --format="value(status.url)" 2>/dev/null)
echo "Frontend: $FRONTEND_URL"
echo ""
echo "🌐 Aplicação completa disponível em: $FRONTEND_URL"
