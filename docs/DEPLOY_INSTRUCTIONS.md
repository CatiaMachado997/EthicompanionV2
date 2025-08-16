# 🚀 Deploy para Google Cloud Run - Instruções

## ✅ Projeto Configurado: `ethic-companion-2025`

### ⚠️ Próximo Passo: Habilitar Billing

**Status**: Projeto `ethic-companion-2025` criado e configurado, mas precisa de billing habilitado.

### 📋 Para continuar com o deploy, precisa fazer o seguinte:

1. **🏦 Habilitar Billing no Google Cloud Console:**
   - Vá para [Google Cloud Console](https://console.cloud.google.com/billing)
   - Selecione o projeto `ethic-companion-2025`
   - No menu lateral, vá para "Billing" (Faturação)
   - Associe uma conta de faturação ao projeto
   - Nota: Google Cloud oferece $300 em créditos grátis para novos utilizadores

2. **🔧 Depois de habilitar billing, execute:**
   ```bash
   # Habilitar APIs necessárias
   gcloud services enable cloudbuild.googleapis.com run.googleapis.com secretmanager.googleapis.com
   ```

3. **🔐 Criar segredos no Secret Manager:**
   ```bash
   # Google API Key
   echo "SUA_GOOGLE_API_KEY" | gcloud secrets create ethic-companion-google-api-key --data-file=-
   
   # Tavily API Key
   echo "SUA_TAVILY_API_KEY" | gcloud secrets create ethic-companion-tavily-api-key --data-file=-
   
   # Weaviate API Key
   echo "SUA_WEAVIATE_API_KEY" | gcloud secrets create ethic-companion-weaviate-api-key --data-file=-
   ```

## 🚀 Deploy via Cloud Code (Método Recomendado)

### Parte 1: Backend

1. **📂 Abrir VS Code no diretório do projeto**
2. **⌨️ Paleta de Comandos**: `Cmd+Shift+P` (Mac) ou `Ctrl+Shift+P` (Windows/Linux)
3. **🔍 Procurar**: "Deploy to Cloud Run"
4. **📝 Configurar**:
   - **Service Name**: `ethic-companion-backend`
   - **Region**: `europe-west1` (ou outra região próxima)
   - **Builder**: Docker
   - **Dockerfile**: `./Dockerfile`
   - **Authentication**: Allow unauthenticated invocations

5. **🔐 Configurar Secrets**:
   - No separador "Secrets", adicionar:
     - `ethic-companion-google-api-key` → `GOOGLE_API_KEY`
     - `ethic-companion-tavily-api-key` → `TAVILY_API_KEY`
     - `ethic-companion-weaviate-api-key` → `WEAVIATE_API_KEY`

6. **🚀 Deploy**: Clicar no botão "Deploy"

## 🎯 Deploy Manual (Alternativo)

Se preferir fazer via terminal:

```bash
# Build e deploy
gcloud run deploy ethic-companion-backend \
  --source . \
  --platform managed \
  --region europe-west1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_CLOUD_PROJECT=ethic-companion-2025 \
  --set-secrets GOOGLE_API_KEY=ethic-companion-google-api-key:latest,TAVILY_API_KEY=ethic-companion-tavily-api-key:latest,WEAVIATE_API_KEY=ethic-companion-weaviate-api-key:latest
```

## 📋 Status Atual

✅ **Projeto configurado**: `ethic-companion-2025`
✅ **Google Cloud Code instalado**
✅ **Dockerfile pronto para produção**
✅ **Sistema de configuração cloud-ready**
⚠️ **Pendente**: Habilitar billing no projeto
⚠️ **Pendente**: Criar secrets no Secret Manager

## 🎯 Próximos Passos

1. Habilitar billing no Google Cloud Console
2. Executar comandos para criar secrets
3. Usar Cloud Code para deploy
4. Obter URL do backend
5. Configurar frontend para usar o URL do backend

O projeto está **tecnicamente pronto** para deploy! 🎉
