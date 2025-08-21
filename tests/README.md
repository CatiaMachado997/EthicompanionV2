# 🧪 Tests Directory

Este diretório contém todos os testes para o Ethic Companion V2.

## 📋 Estrutura dos Testes

### Testes de Integração:
- `test_complete_system.py` - Testes do sistema completo
- `test_end_to_end.py` - Testes end-to-end
- `test_integration.py` - Testes de integração geral
- `teste_completo.py` - Teste completo em português

### Testes de API:
- `test_chat_endpoint.py` - Testes dos endpoints de chat
- `test_chat_client.py` - Testes do cliente de chat
- `test_frontend_integration.py` - Integração frontend-backend

### Testes de Componentes:
- `test_llm.py` / `test_llm_only.py` - Testes do modelo de linguagem
- `test_memory.py` / `test_memory_*` - Testes do sistema de memória
- `test_search_*.py` / `test_tavily_*` - Testes de pesquisa web
- `test_agent_executor.py` - Testes do executor de agentes
- `test_full_agent.py` - Testes do agente completo

### Testes de Roteamento:
- `test_lcel_router.py` - Testes do roteador LCEL
- `test_router_debug.py` - Debug do roteador
- `test_routing_direct.py` - Testes de roteamento direto

### Testes de Backend:
- `test_backend_startup.py` - Inicialização do backend
- `test_web_search_frontend.py` - Interface de pesquisa web

### Testes Simples:
- `simple_test.py` - Testes básicos
- `test_golden_rule.py` - Testes da regra dourada

## 🚀 Como Executar os Testes

### Executar todos os testes:
```bash
python -m pytest tests/
```

### Executar um teste específico:
```bash
python tests/test_complete_system.py
```

### Executar testes por categoria:
```bash
# Testes de memória
python -m pytest tests/test_memory*.py

# Testes de pesquisa
python -m pytest tests/test_*search*.py tests/test_tavily*.py

# Testes de LLM
python -m pytest tests/test_llm*.py
```

## 📝 Configuração Necessária

Antes de executar os testes, certifique-se de ter:

1. **Variáveis de ambiente configuradas** (arquivo `.env`):
   ```bash
   GOOGLE_API_KEY=sua_chave_aqui
   TAVILY_API_KEY=sua_chave_aqui
   ```

2. **Dependências instaladas**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Weaviate rodando** (se necessário):
   ```bash
   docker run -p 8080:8080 -e WEAVIATE_QUERY_DEFAULTS_LIMIT=25 weaviate/weaviate:1.21.8
   ```

## 🔧 Estrutura Recomendada

Para novos testes, siga esta convenção:
- `test_[componente].py` - Testes unitários do componente
- `test_[componente]_integration.py` - Testes de integração
- `test_[funcionalidade]_e2e.py` - Testes end-to-end
