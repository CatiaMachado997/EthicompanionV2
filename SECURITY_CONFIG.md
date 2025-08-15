# 🔐 CONFIGURAÇÃO DE SEGURANÇA - ETHIC COMPANION V2

## Resumo da Segurança Implementada

### ✅ Medidas de Segurança Ativas

1. **Autenticação Obrigatória**
   - ❌ Acesso público desabilitado (`--no-allow-unauthenticated`)
   - ✅ Apenas usuários autorizados podem acessar
   - ✅ Token de identidade Google Cloud necessário

2. **Controle de Acesso (IAM)**
   - ✅ Usuário autorizado: `catiasofiafmachado@ethicompanion.com`
   - ✅ Role: `roles/run.invoker` (permite invocar o serviço)
   - ❌ `allUsers` bloqueado (política organizacional)

3. **Isolamento de Rede**
   - ✅ Ingress configurado para controle de acesso
   - ✅ Serviços executam em ambiente isolado do Google Cloud
   - ✅ Comunicação entre serviços protegida

4. **Configuração de Ambiente**
   - ✅ Variáveis de ambiente seguras
   - ✅ Secrets gerenciados pelo Google Cloud Secret Manager
   - ✅ Chaves API protegidas

## 🔗 URLs dos Serviços

- **Frontend**: https://ethic-companion-frontend-243140067122.us-central1.run.app
- **Backend**: https://ethic-companion-backend-243140067122.us-central1.run.app

## 🛡️ Como Acessar Seguramente

### Método 1: Script Automatizado
```bash
./access_app.sh
```

### Método 2: Browser Direto
1. Certifique-se de estar logado no Google com: `catiasofiafmachado@ethicompanion.com`
2. Acesse o URL do frontend no browser
3. A autenticação será feita automaticamente

### Método 3: Via gcloud CLI
```bash
# Obter token
gcloud auth print-identity-token

# Usar token nas requisições
curl -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
     https://ethic-companion-frontend-243140067122.us-central1.run.app
```

## 🔧 Configuração Técnica

### Cloud Run Services
- **Região**: us-central1
- **Projeto**: ethic-companion-v2
- **Conta de Serviço**: 243140067122-compute@developer.gserviceaccount.com

### Recursos Alocados
- **Frontend**: 512Mi RAM, 0.5 CPU, máx 10 instâncias
- **Backend**: 1Gi RAM, 1 CPU, máx 10 instâncias

### Variáveis de Ambiente Seguras
- `BACKEND_URL`: URL interno seguro do backend
- `NODE_ENV`: production
- Chaves API carregadas via Secret Manager

## 🚨 Troubleshooting

### Se aparecer "Page Not Found":
1. Verifique se está logado com a conta correta
2. Execute: `gcloud auth login catiasofiafmachado@ethicompanion.com`
3. Tente acessar novamente

### Se aparecer "403 Forbidden":
1. Verifique as permissões IAM
2. Execute: `gcloud run services get-iam-policy ethic-companion-frontend --region=us-central1`

### Para logs de debug:
```bash
# Frontend logs
gcloud run services logs read ethic-companion-frontend --region=us-central1 --limit=20

# Backend logs
gcloud run services logs read ethic-companion-backend --region=us-central1 --limit=20
```

## 🔄 Próximos Passos de Segurança (Opcionais)

1. **VPC Connector**: Para isolamento completo de rede
2. **Cloud Armor**: Para proteção DDoS e WAF
3. **Identity-Aware Proxy**: Para controle de acesso mais granular
4. **Custom Domain**: Para usar domínio próprio com SSL
5. **Cloud Monitoring**: Para alertas de segurança

## ✅ Status Atual
- ✅ Backend: Funcionando com autenticação
- ✅ Frontend: Funcionando com autenticação  
- ✅ IAM: Configurado corretamente
- ✅ Secrets: Gerenciados pelo Google Cloud
- ✅ Acesso: Restrito apenas ao usuário autorizado
