# 🚨 Billing Configuration Required

## Status Atual
- ✅ Projeto: `ethic-companion-2025` criado
- ❌ Billing: Não está habilitado (contas fechadas)

## 💳 Como Habilitar Billing

### Opção 1: Google Cloud Console (Recomendado)
1. **Abrir**: [Google Cloud Console - Billing](https://console.cloud.google.com/billing)
2. **Criar Nova Conta de Billing**:
   - Clique em "Create Account"
   - Escolha "Individual" ou "Business"
   - Adicione método de pagamento (cartão de crédito)
   - **Nota**: Google oferece $300 em créditos grátis
3. **Associar ao Projeto**:
   - Vá para "Link a billing account to project"
   - Selecione `ethic-companion-2025`
   - Associe à conta de billing criada

### Opção 2: Reativar Conta Existente
Se você já tem uma conta mas está fechada:
1. **Abrir**: [Google Cloud Console - Billing](https://console.cloud.google.com/billing)
2. **Selecionar conta**: `My Billing Account` ou `My Billing Account 1`
3. **Reativar**: Adicionar/atualizar método de pagamento
4. **Associar**: Linkar ao projeto `ethic-companion-2025`

## 🔄 Depois de Configurar Billing

Execute este comando para verificar:
```bash
gcloud beta billing projects describe ethic-companion-2025
```

Deveria mostrar `billingEnabled: true`

## 🚀 Deploy Automático

Depois do billing estar habilitado, execute:
```bash
./deploy_cloud_run.sh
```

Ou use o Cloud Code no VS Code:
1. `Cmd+Shift+P` (Mac) ou `Ctrl+Shift+P` (Windows/Linux)
2. "Deploy to Cloud Run"
3. Configurar serviço e secrets

## 📞 Suporte

Se precisar de ajuda com billing:
- [Google Cloud Support](https://cloud.google.com/support)
- [Billing Documentation](https://cloud.google.com/billing/docs)

O projeto está **tecnicamente pronto** - só falta o billing! 🎯
