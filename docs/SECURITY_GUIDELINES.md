# 🔐 SECURITY_GUIDELINES.md

## ⚠️ IMPORTANTE - SEGURANÇA DE API KEYS

### ❌ NUNCA FAÇA:
- Commitar API keys diretamente no código
- Usar valores reais em arquivos de exemplo
- Expor chaves em logs ou prints
- Compartilhar chaves em screenshots ou documentação

### ✅ SEMPRE FAÇA:
- Use arquivos `.env` para development local
- Configure `.env` no `.gitignore`
- Use Google Cloud Secret Manager para produção
- Use placeholders em arquivos de exemplo

## 📋 Checklist de Segurança Antes do Commit

```bash
# 1. Verificar se não há API keys expostas
grep -r "AIza\|tvly-\|sk-\|gsk_" . --exclude-dir=node_modules --exclude-dir=.git

# 2. Verificar .gitignore
cat .gitignore | grep -E "\.env|\.json"

# 3. Verificar se .env não está commitado
git status | grep -v ".env"
```

## 🛡️ Configuração Segura

### Development Local:
```bash
# Copiar template
cp .env.example .env

# Editar com suas chaves reais
nano .env
```

### Produção (Google Cloud):
```bash
# Criar secrets
gcloud secrets create google-api-key --data-file=<(echo "SUA_CHAVE_REAL")
gcloud secrets create tavily-api-key --data-file=<(echo "SUA_CHAVE_REAL")
```

## 🔍 Verificações Automáticas

### Pre-commit Hook:
```bash
#!/bin/bash
# .git/hooks/pre-commit

# Verificar API keys expostas
if grep -r "AIza\|tvly-[a-zA-Z0-9]\|sk-[a-zA-Z0-9]" . --exclude-dir=node_modules --exclude-dir=.git; then
    echo "❌ API keys detectadas no código!"
    echo "Remove as chaves antes do commit."
    exit 1
fi

echo "✅ Verificação de segurança passou"
```

## 📞 Em Caso de Exposição Acidental

1. **Imediatamente**: Revogue a API key no provedor
2. **Gere nova chave**: Crie uma substituta
3. **Limpe histórico**: Use git filter-branch se necessário
4. **Atualize secrets**: Configure nova chave nos ambientes

## 🎯 Responsabilidades

- **Desenvolvedor**: Nunca commitir chaves
- **CI/CD**: Usar secrets seguros
- **Produção**: Google Cloud Secret Manager
- **Monitoramento**: Alertas para exposição de chaves

---

**🚨 LEMBRE-SE: Uma API key exposta pode comprometer todo o projeto!**
