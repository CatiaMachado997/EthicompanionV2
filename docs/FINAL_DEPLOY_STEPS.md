# 🎯 Deploy para ethic-companion-2025 (PROJECT_NUMBER: 284317188668)

## ✅ Status Atual
- **Projeto**: `ethic-companion-2025`
- **Project Number**: `284317188668`
- **Conta**: `catia9714@gmail.com`
- **Acesso**: ✅ Completo

## 🏦 Configurar Billing

### 📋 Passos no Google Cloud Console:

1. **Abrir página de billing** (já aberta no Simple Browser):
   - URL: https://console.cloud.google.com/billing/linkedprojects?project=ethic-companion-2025

2. **Configurar billing account**:
   - Se não tem billing account: Clique "Create Billing Account"
   - Se tem billing account: Selecione uma existente
   - Adicione método de pagamento (cartão de crédito)
   - **Nota**: Google oferece $300 em créditos grátis

3. **Associar ao projeto**:
   - Certifique-se que `ethic-companion-2025` está linked à billing account

## 🚀 Depois do Billing Configurado

Execute estes comandos em sequência:

```bash
# 1. Habilitar APIs
gcloud services enable cloudbuild.googleapis.com run.googleapis.com secretmanager.googleapis.com

# 2. Executar deploy automático
./deploy_cloud_run.sh
```

## 🎯 Deploy via Cloud Code (Alternativa)

1. **Command Palette**: `Cmd+Shift+P`
2. **Procurar**: "Deploy to Cloud Run"
3. **Configurar**:
   - Service Name: `ethic-companion-backend`
   - Region: `europe-west1`
   - Project: `ethic-companion-2025`
   - Authentication: Allow unauthenticated

## 📋 O Projeto Está 100% Pronto!

Só falta configurar o billing e depois é só fazer deploy! 🎉

### 🔐 API Keys Necessárias:
- GOOGLE_API_KEY
- TAVILY_API_KEY  
- WEAVIATE_API_KEY

Certifique-se que estão no ficheiro `.env` antes de executar o deploy.
