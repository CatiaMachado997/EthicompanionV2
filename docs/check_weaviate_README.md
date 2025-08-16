# 🔍 Check Weaviate Script

Script Python para verificar o estado da base de dados vetorial Weaviate do Ethic Companion V2.

## 📋 Funcionalidades

- ✅ Carrega configurações do arquivo `.env`
- ✅ Conecta-se ao Weaviate local (com ou sem autenticação)
- ✅ Lista todas as coleções disponíveis
- ✅ Conta objetos na coleção `MemoryItem`
- ✅ Mostra exemplos dos primeiros itens armazenados
- ✅ Tratamento completo de erros

## 🚀 Como Usar

```bash
# Executar o script
python check_weaviate.py

# Ou torná-lo executável
chmod +x check_weaviate.py
./check_weaviate.py
```

## 📊 Saída Esperada

```
🧠 Check Weaviate - Verificação da Base de Dados Vetorial
============================================================
🔧 Carregando variáveis de ambiente...
   📍 URL: http://localhost:8080
   🔑 API Key: ⚠️  Não configurada

🔗 Conectando ao Weaviate em http://localhost:8080...
   🔓 Conectando sem autenticação...
   ✅ Conexão estabelecida!
   📊 Versão do Weaviate: 1.30.14

🗃️  Verificando coleção 'MemoryItem'...
   📋 Coleções disponíveis:
      - MemoryItem
   ✅ Coleção 'MemoryItem' encontrada!
   📊 Total de objetos: 9

   🔍 Primeiros itens da memória:
      1. Gosto de trabalhar com Python e IA
      2. User: Olá, como estás? Assistant: Olá!...
      ... e mais 7 itens

============================================================
🎯 RESULTADO FINAL: 9 itens encontrados na coleção MemoryItem
✅ A base de dados de memória contém 9 items.
```

## ⚙️ Configuração

O script lê as seguintes variáveis do arquivo `.env`:

- `WEAVIATE_URL` - URL do Weaviate (padrão: http://localhost:8080)
- `WEAVIATE_API_KEY` - Chave de API (opcional para desenvolvimento local)

## 🔧 Pré-requisitos

1. **Weaviate rodando localmente:**
   ```bash
   docker run -d -p 8080:8080 -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true semitechnologies/weaviate:latest
   ```

2. **Dependências Python:**
   ```bash
   pip install weaviate-client python-dotenv
   ```

## 🚨 Resolução de Problemas

### Erro de Conexão
```
❌ Falha na conexão com o Weaviate!
```
**Solução:** Certifica-te de que o Weaviate está rodando na porta 8080.

### Erro de Autenticação
```
❌ Erro inesperado: Meta endpoint! Unexpected status code: 401
```
**Solução:** Comenta a linha `WEAVIATE_API_KEY` no arquivo `.env` para desenvolvimento sem autenticação.

### Coleção Não Encontrada
```
⚠️  Coleção 'MemoryItem' não encontrada!
```
**Solução:** Normal para primeira execução. A coleção será criada automaticamente quando o primeiro item for adicionado através do chat.

## 🎯 Utilização

Este script é útil para:
- ✅ Verificar se a memória vetorial está funcionando
- ✅ Contar quantas conversas foram armazenadas
- ✅ Debug do sistema de memória
- ✅ Monitorização do estado da base de dados
