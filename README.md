# 🤖 Ethic Companion V2

Um assistente de IA inteligente com memória vetorial e pesquisa em tempo real, construído com FastAPI, Weaviate, Google Gemini e Tavily Search.

## ✨ Funcionalidades

- **💬 Chat Inteligente**: Conversas naturais com IA
- **🔍 Pesquisa em Tempo Real**: Informações atualizadas via Tavily Search
- **🧠 Memória Vetorial**: Contexto de conversas anteriores via Weaviate
- **🎨 Interface Moderna**: Design fluido com tons terrosos
- **⚡ AgentExecutor**: Sistema de ferramentas inteligente

## 🚀 Início Rápido

### Pré-requisitos

- Python 3.11+
- Docker e Docker Compose
- Node.js 18+ (para frontend)

### 1. Configurar Weaviate

```bash
# Iniciar Weaviate com Docker
docker-compose up -d
```

### 2. Configurar Backend

```bash
# Clonar e configurar
cd "Ethic Companion V2"
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt

# Iniciar servidor
./start_server.sh
```

### 3. Configurar Frontend

```bash
# Navegar para o frontend
cd frontend

# Instalar dependências
npm install

# Iniciar servidor de desenvolvimento
npm run dev
```

## 🔧 Configuração

### Variáveis de Ambiente

O projeto usa as seguintes variáveis de ambiente:

- `WEAVIATE_API_KEY`: Chave para Weaviate (padrão: "minha-chave-secreta-dev")
- `GOOGLE_API_KEY`: Chave para Google Gemini
- `TAVILY_API_KEY`: Chave para Tavily Search

### Obter API Keys

1. **Google Gemini**: https://makersuite.google.com/app/apikey
2. **Tavily Search**: https://tavily.com/ (já configurada)

## 📁 Estrutura do Projeto

```
Ethic Companion V2/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── chat.py          # Endpoint principal com AgentExecutor
│   │   └── chat_simple.py   # Endpoint simples (sem LLM)
│   ├── core/
│   │   ├── memory.py        # Gerenciamento de memória vetorial
│   │   └── llm.py           # Integração com Google Gemini
│   └── models/              # Modelos Pydantic
├── frontend/                # Interface Next.js
├── docker-compose.yml       # Configuração Weaviate
├── main.py                  # Servidor FastAPI
├── requirements.txt         # Dependências Python
└── start_server.sh          # Script de inicialização
```

## 🎯 Endpoints

### `/chat` (Principal)
- **Método**: POST
- **Descrição**: Chat completo com AgentExecutor
- **Funcionalidades**: LLM + Pesquisa + Memória

### `/chat-simple` (Alternativo)
- **Método**: POST
- **Descrição**: Chat apenas com pesquisa
- **Funcionalidades**: Apenas Tavily Search

## 🧪 Testes

```bash
# Testar Tavily Search
python test_tavily_simple.py

# Testar integração frontend
python test_frontend_integration.py

# Testar AgentExecutor completo
python test_full_agent.py
```

## 🎨 Interface

A interface inclui:
- **Sidebar**: Navegação e histórico
- **Chat Principal**: Conversas em tempo real
- **Input Inteligente**: Auto-resize e comandos de voz
- **Design Fluido**: Tons terrosos e animações suaves

## 🔄 Fluxo de Funcionamento

1. **Usuário envia mensagem** → Frontend
2. **Frontend → Backend** → Endpoint `/chat`
3. **AgentExecutor analisa** → Escolhe ferramentas
4. **Tavily Search** → Informações atualizadas
5. **Weaviate Memory** → Contexto anterior
6. **Google Gemini** → Resposta inteligente
7. **Resposta → Frontend** → Exibição

## 🛠️ Tecnologias

### Backend
- **FastAPI**: Framework web
- **LangChain**: AgentExecutor e ferramentas
- **Weaviate**: Base de dados vetorial
- **Google Gemini**: Modelo de linguagem
- **Tavily**: Pesquisa em tempo real

### Frontend
- **Next.js**: Framework React
- **Bootstrap 5**: Componentes UI
- **CSS Custom**: Design fluido
- **TypeScript**: Tipagem estática

## 🚀 Deploy

### Desenvolvimento
```bash
./start_server.sh
```

### Produção
```bash
# Configurar variáveis de ambiente
# Usar gunicorn ou uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 📝 Licença

Este projeto é para uso educacional e pessoal.

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

---

**Ethic Companion V2** - Assistente de IA Inteligente 🤖✨ 