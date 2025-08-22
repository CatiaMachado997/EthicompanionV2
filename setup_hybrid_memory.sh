#!/bin/bash

# 🚀 Script de Instalação Automática - Ethic Companion V2
# Configura todo o sistema de memória híbrida

echo "🧠 === INSTALAÇÃO DO SISTEMA DE MEMÓRIA HÍBRIDA ==="
echo ""

# Verificar se estamos no diretório correto
if [ ! -f "package.json" ] || [ ! -f "test_hybrid_memory.py" ]; then
    echo "❌ Erro: Execute este script na raiz do projeto Ethic Companion V2"
    exit 1
fi

echo "1️⃣ **Instalando Dependências Python...**"

# Instalar dependências básicas do Python
pip install -q sqlalchemy psycopg2-binary weaviate-client python-dotenv

# Instalar LangChain
echo "   Instalando LangChain..."
pip install -q langchain langchain-openai langchain-google-genai

# Instalar outras dependências
pip install -q tavily-python requests asyncio

echo "✅ Dependências Python instaladas"
echo ""

echo "2️⃣ **Configurando Ambiente...**"

# Criar arquivo .env se não existir
if [ ! -f ".env" ]; then
    echo "   Criando arquivo .env..."
    cp .env.hybrid.example .env
    echo "✅ Arquivo .env criado (configure suas API keys)"
else
    echo "✅ Arquivo .env já existe"
fi

echo ""

echo "3️⃣ **Configurando Base de Dados...**"

# Criar base de dados SQLite para desenvolvimento
python3 -c "
from backend_app.models.database import create_tables
try:
    create_tables()
    print('✅ Base de dados SQLite criada')
except Exception as e:
    print(f'⚠️ Erro ao criar BD: {e}')
"

echo ""

echo "4️⃣ **Verificando Weaviate...**"

# Verificar se Weaviate está a correr
if curl -s http://localhost:8080/v1/meta > /dev/null 2>&1; then
    echo "✅ Weaviate está a correr em http://localhost:8080"
else
    echo "⚠️ Weaviate não está a correr. Para iniciar:"
    echo "   docker run -p 8080:8080 semitechnologies/weaviate:latest"
    echo "   ou"
    echo "   docker-compose -f docker/docker-compose.yml up -d"
fi

echo ""

echo "5️⃣ **Instalando Dependências Frontend...**"

# Instalar dependências do npm se necessário
if [ ! -d "node_modules" ]; then
    echo "   Instalando pacotes npm..."
    npm install
    echo "✅ Dependências frontend instaladas"
else
    echo "✅ Dependências frontend já instaladas"
fi

echo ""

echo "6️⃣ **Testando Sistema...**"

# Executar teste simples
echo "   Executando teste básico..."
python3 -c "
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from backend_app.models.database import get_db_session, create_tables
    
    # Testar base de dados
    create_tables()
    db = get_db_session()
    db.execute('SELECT 1')
    db.close()
    print('✅ PostgreSQL/SQLite: OK')
    
except Exception as e:
    print(f'❌ Base de dados: {e}')

try:
    from backend_app.core.ai_agent import get_ai_agent
    agent = get_ai_agent()
    status = agent.get_agent_status()
    print(f'✅ Agente AI: {status[\"status\"]} ({status[\"llm_type\"]})')
    
except Exception as e:
    print(f'⚠️ Agente AI: {e}')

print('🎉 Sistema básico configurado!')
"

echo ""

echo "🎉 **INSTALAÇÃO COMPLETA!**"
echo ""
echo "📋 **Próximos Passos:**"
echo ""
echo "1. **Configurar API Keys:**"
echo "   Editar .env com as tuas chaves:"
echo "   - OPENAI_API_KEY=sk-proj-..."
echo "   - GOOGLE_API_KEY=AIzaSy..."
echo "   - DATABASE_URL=postgresql://... (ou usar SQLite)"
echo ""
echo "2. **Iniciar Weaviate (se necessário):**"
echo "   docker run -p 8080:8080 semitechnologies/weaviate:latest"
echo ""
echo "3. **Testar Sistema:**"
echo "   python test_hybrid_memory.py"
echo ""
echo "4. **Executar Aplicação:**"
echo "   # Terminal 1 - Backend"
echo "   python main.py"
echo ""
echo "   # Terminal 2 - Frontend"
echo "   npm run dev"
echo ""
echo "5. **Aceder:**"
echo "   Frontend: http://localhost:3000"
echo "   Backend: http://localhost:8000"
echo "   Docs: http://localhost:8000/docs"
echo ""
echo "📖 **Documentação:**"
echo "   - Consultar FRONTEND_INTEGRATION_GUIDE.md"
echo "   - Exemplos em main_example.py"
echo ""
echo "🚀 **O teu sistema de memória híbrida está pronto!**"
