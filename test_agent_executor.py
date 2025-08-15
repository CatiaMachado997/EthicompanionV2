#!/usr/bin/env python3
"""
Teste do AgentExecutor do LangChain
"""

import os
from app.api.chat import agent_executor, memory_manager

async def test_agent_executor():
    print("🧪 Testando AgentExecutor...")
    
    try:
        # Teste 1: Pergunta simples
        print("\n1. Teste: Pergunta simples")
        result1 = await agent_executor.ainvoke({
            "input": "Olá! Como vais?"
        })
        print(f"✅ Resposta: {result1['output']}")
        
        # Teste 2: Pergunta sobre factos atuais (deve usar DuckDuckGo)
        print("\n2. Teste: Pergunta sobre factos atuais")
        result2 = await agent_executor.ainvoke({
            "input": "Quem é o presidente de Portugal?"
        })
        print(f"✅ Resposta: {result2['output']}")
        
        # Teste 3: Pergunta sobre conversas passadas (deve usar memória)
        print("\n3. Teste: Pergunta sobre conversas passadas")
        result3 = await agent_executor.ainvoke({
            "input": "Lembras-te do que falámos antes?"
        })
        print(f"✅ Resposta: {result3['output']}")
        
        print("\n🎉 Todos os testes do AgentExecutor passaram!")
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Configurar variáveis de ambiente se necessário
    if not os.getenv('GOOGLE_API_KEY'):
        print("⚠️  GOOGLE_API_KEY não definida")
    if not os.getenv('WEAVIATE_API_KEY'):
        print("⚠️  WEAVIATE_API_KEY não definida")
    
    import asyncio
    asyncio.run(test_agent_executor())
