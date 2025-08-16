#!/bin/bash

# Deploy Completo - Backend + Frontend
# Ethic Companion V2

echo "🚀 Iniciando deploy completo da aplicação Ethic Companion V2..."
echo ""

# Passo 1: Deploy Backend
echo "📡 PASSO 1: Deploy do Backend (FastAPI)"
echo "========================================"

gcloud run deploy ethic-companion-backend \
    --source . \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --port 8000 \
    --memory 1Gi \
    --cpu 1 \
    --max-instances 10 \
    --service-account ethic-companion-backend@ethic-companion-v2.iam.gserviceaccount.com \
    --set-env-vars="ENVIRONMENT=production,GOOGLE_CLOUD_PROJECT=ethic-companion-v2"

if [ $? -ne 0 ]; then
    echo "❌ Erro no deploy do backend!"
    exit 1
fi

# Obter URL do backend
BACKEND_URL=$(gcloud run services describe ethic-companion-backend --region us-central1 --format="value(status.url)")
echo "✅ Backend implantado: $BACKEND_URL"
echo ""

# Passo 2: Deploy Frontend
echo "🌐 PASSO 2: Deploy do Frontend (Next.js)"
echo "========================================"

gcloud run deploy ethic-companion-frontend \
    --source . \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --port 3000 \
    --memory 512Mi \
    --cpu 0.5 \
    --max-instances 10 \
    --set-env-vars="BACKEND_URL=$BACKEND_URL,NODE_ENV=production" \
    --dockerfile=Dockerfile.frontend

if [ $? -ne 0 ]; then
    echo "❌ Erro no deploy do frontend!"
    exit 1
fi

# Obter URL do frontend
FRONTEND_URL=$(gcloud run services describe ethic-companion-frontend --region us-central1 --format="value(status.url)")

echo ""
echo "🎉 Deploy completo realizado com sucesso!"
echo "========================================"
echo "Backend:  $BACKEND_URL"
echo "Frontend: $FRONTEND_URL"
echo ""
echo "🌐 Acesse sua aplicação em: $FRONTEND_URL"
echo ""
