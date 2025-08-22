# 🚀 GUIA DE IMPLEMENTAÇÃO - SISTEMA DE MEMÓRIA HÍBRIDA
# Frontend Next.js + Backend FastAPI + PostgreSQL + Weaviate

## ✨ O QUE FOI IMPLEMENTADO

### 🧠 **Backend (Sistema de Memória Híbrida)**
✅ MemoryManager - Combina PostgreSQL + Weaviate
✅ Endpoints FastAPI para chat com contexto
✅ Agente AI com ferramentas especializadas
✅ Suporte OpenAI + Gemini + Tavily

### 🎨 **Frontend (React/Next.js)**
✅ Hook personalizado useHybridMemoryChat
✅ Componentes de estatísticas de memória
✅ Seletor de modos de contexto
✅ Mensagens com informações de contexto
✅ Interface integrada e responsiva

## 🔧 CONFIGURAÇÃO RÁPIDA

### **Passo 1: Configurar Variáveis de Ambiente**
```bash
# Copiar configuração de exemplo
cp .env.hybrid.example .env

# Editar .env com as tuas chaves:
OPENAI_API_KEY=sk-proj-...
GOOGLE_API_KEY=AIzaSy...
DATABASE_URL=postgresql://user:pass@localhost/ethic_companion
WEAVIATE_URL=http://localhost:8080
TAVILY_API_KEY=tvly-...
```

### **Passo 2: Instalar Dependências**
```bash
# Backend Python
pip install -r requirements.txt
pip install sqlalchemy psycopg2-binary weaviate-client
pip install langchain langchain-openai langchain-google-genai

# Frontend Node.js (já instalado)
npm install
```

### **Passo 3: Configurar Infraestrutura**
```bash
# Opção A: Docker Compose (recomendado)
docker-compose -f docker/docker-compose.yml up -d

# Opção B: Manual
# PostgreSQL
createdb ethic_companion

# Weaviate
docker run -p 8080:8080 semitechnologies/weaviate:latest
```

### **Passo 4: Testar Sistema**
```bash
# Testar backend
python test_hybrid_memory.py

# Iniciar serviços
python main.py              # Backend FastAPI
npm run dev                 # Frontend Next.js
```

## 🎯 COMO USAR

### **Interface Principal:**
1. **💬 Chat Inteligente** - Conversas com memória contextual
2. **🧠 Painel de Memória** - Estatísticas PostgreSQL + Weaviate  
3. **⚙️ Seletor de Contexto** - Híbrida, Recente, Semântica, Nenhuma
4. **📊 Detalhes de Contexto** - Informações sobre memórias usadas

### **Modos de Memória:**
- **🧠 Híbrida** - Combina histórico recente + memórias relevantes (RECOMENDADO)
- **📚 Recente** - Apenas últimas mensagens desta conversa
- **🔍 Semântica** - Apenas memórias relevantes de conversas passadas
- **💭 Nenhuma** - Conversa sem contexto (modo básico)

## 🚀 FUNCIONALIDADES AVANÇADAS

### **Sistema de Sessões:**
- Cada conversa tem ID único
- Memória persistente entre sessões
- Recuperação automática de contexto

### **Ferramentas do Agente:**
- **Análise Ética** - Framework estruturado para dilemas
- **Reflexão Pessoal** - Perguntas guiadas
- **Pesquisa Web** - Informações atuais via Tavily

### **Performance:**
- Operações assíncronas
- Background tasks para não bloquear UI
- Fallbacks automáticos
- Error handling robusto

## 📊 ENDPOINTS DISPONÍVEIS

### **Chat API:**
- `POST /api/chat/message` - Enviar mensagem com contexto
- `GET /api/chat/memory/stats` - Estatísticas de memória
- `GET /api/chat/sessions/{id}/context` - Contexto de sessão

### **Sistema API:**
- `GET /health` - Estado do sistema
- `GET /debug/system-info` - Informações de debug

## 🔍 EXEMPLO DE USO

### **Frontend (React):**
```typescript
const {
  messages, isLoading, sendMessage, 
  memoryStats, contextInfo, contextMode, setContextMode
} = useHybridMemoryChat({
  contextMode: 'hybrid',
  sessionId: 'user_session_123'
});

// Enviar mensagem
await sendMessage("Como devo lidar com este dilema ético?");

// Mudar modo de contexto
setContextMode('semantic_only');
```

### **Backend Response:**
```json
{
  "response": "Vamos analisar este dilema através de várias perspetivas éticas...",
  "session_id": "session_123",
  "context_used": {
    "type": "hybrid",
    "recent_count": 3,
    "semantic_count": 2,
    "has_recent": true,
    "has_semantic": true
  },
  "memory_stats": {
    "postgresql": {"total_messages": 1247, "unique_sessions": 89},
    "weaviate": {"total_vectors": 1156}
  }
}
```

## ⚡ PRÓXIMOS PASSOS

### **Desenvolvimento:**
1. **Testar** sistema básico localmente
2. **Personalizar** prompts do agente
3. **Ajustar** limites de contexto
4. **Implementar** analytics avançadas

### **Produção:**
1. **Deploy** PostgreSQL e Weaviate em cloud
2. **Configurar** variáveis de ambiente
3. **Otimizar** performance
4. **Monitorizar** uso de memória

## 🎨 PERSONALIZAÇÃO

### **Ajustar Contexto:**
```python
# No MemoryManager
context = await memory_manager.get_context(
    session_id=session_id,
    query=query,
    recent_limit=5,    # Mais ou menos mensagens recentes
    semantic_limit=3   # Mais ou menos memórias relevantes
)
```

### **Customizar Interface:**
- Modificar componentes em `src/components/`
- Ajustar estilos em `src/app/globals.css`
- Personalizar cores e temas

## 🔐 SEGURANÇA

### **Variáveis Protegidas:**
- ✅ .env não commitado
- ✅ API keys em ambiente
- ✅ Validação de inputs
- ✅ Error handling seguro

### **Monitorização:**
- Logs detalhados
- Estatísticas de uso
- Health checks automáticos

## 🎯 RESUMO FINAL

Tens agora um **sistema de memória híbrida profissional** que transforma o teu Ethic Companion numa IA verdadeiramente inteligente e personalizada!

### **Principais Vantagens:**
1. **🧠 Memória Inteligente** - Combina episódica + semântica
2. **⚡ Performance** - Assíncrono e otimizado
3. **🎨 Interface Rica** - Componentes React modernos
4. **🔧 Flexível** - Múltiplos modos de contexto
5. **📈 Escalável** - PostgreSQL + Weaviate profissionais

**Está tudo pronto para transformares o teu projeto num assistente de IA de próxima geração!** 🚀

---
*Para dúvidas ou ajustes, consulta os ficheiros de exemplo e testa o sistema passo a passo.*
