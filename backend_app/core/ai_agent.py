"""
Agente AI Principal
Integra LLM com ferramenta            # Comentar OpenAI temporariamente para usar Gemini
            # if openai_api_key:
            #     self.llm = ChatOpenAI(
            #         model="gpt-3.5-turbo",  # Modelo mais acessível
            #         temperature=0.7,
            #         max_tokens=1000,
            #         openai_api_key=openai_api_key
            #     )
            #     print("✅ DEBUG - OpenAI GPT-3.5-turbo inicializado com sucesso")
            #     logger.info("✅ LLM OpenAI inicializado")
            #     returna de memória para conversas inteligentes
"""

import asyncio
import logging
from typing import Dict, Any, Optional, List
import os
from datetime import datetime

# Imports para LLM e ferramentas
try:
    from langchain_openai import ChatOpenAI
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain.schema import HumanMessage, SystemMessage
    from langchain.tools import Tool
    from langchain.agents import AgentExecutor, create_openai_functions_agent
    from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain.memory import ConversationBufferWindowMemory
except ImportError as e:
    logging.warning(f"⚠️ Alguns imports do LangChain falharam: {e}")

logger = logging.getLogger(__name__)

class EthicCompanionAgent:
    """
    Agente AI principal que combina LLM com ferramentas e sistema de memória
    """
    
    def __init__(self):
        """Inicializa o agente com LLM e ferramentas"""
        self.llm = None
        self.agent_executor = None
        self.tools = []
        self._initialize_llm()
        self._initialize_tools()
        self._initialize_agent()
    
    def _initialize_llm(self):
        """Inicializa o modelo de linguagem (Google Gemini - OpenAI temporariamente desativado)"""
        try:
            # Debug: Verificar chaves API
            openai_api_key = os.getenv("OPENAI_API_KEY")
            google_api_key = os.getenv("GOOGLE_API_KEY")
            
            print(f"🔍 DEBUG - OpenAI API Key: {'✅ Carregada' if openai_api_key else '❌ Não encontrada'}")
            print(f"🔍 DEBUG - Google API Key: {'✅ Carregada' if google_api_key else '❌ Não encontrada'}")
            
            # Comentar OpenAI temporariamente para usar Gemini
            # if openai_api_key:
            #     self.llm = ChatOpenAI(
            #         model="gpt-3.5-turbo",  # Modelo mais acessível
            #         temperature=0.7,
            #         max_tokens=1000,
            #         openai_api_key=openai_api_key
            #     )
            #     print("✅ DEBUG - OpenAI GPT-3.5-turbo inicializado com sucesso")
            #     logger.info("✅ LLM OpenAI inicializado")
            #     return
                
        except Exception as e:
            print(f"⚠️ DEBUG - OpenAI desativado temporariamente: {e}")
            logger.warning(f"⚠️ OpenAI desativado temporariamente: {e}")
        
        try:
            # Usar Google Gemini como principal
            if google_api_key:
                self.llm = ChatGoogleGenerativeAI(
                    model="gemini-1.5-flash",  # Modelo mais recente disponível
                    temperature=0.7,
                    google_api_key=google_api_key
                )
                print("✅ DEBUG - Google Gemini 1.5 Flash inicializado como LLM principal")
                logger.info("✅ LLM Google Gemini inicializado")
                return
                
        except Exception as e:
            print(f"❌ DEBUG - Falha ao inicializar Gemini: {e}")
            logger.warning(f"❌ Falha ao inicializar Gemini: {e}")
        
        # Se nenhum LLM foi inicializado
        print("❌ DEBUG - NENHUM LLM DISPONÍVEL - USANDO FALLBACK")
        logger.error("❌ Nenhum LLM disponível")
        self.llm = None
    
    def _initialize_tools(self):
        """Inicializa ferramentas disponíveis para o agente"""
        
        # Ferramenta de pesquisa web (Tavily)
        if os.getenv("TAVILY_API_KEY"):
            try:
                web_search_tool = Tool(
                    name="web_search",
                    description="Pesquisa informações atuais na web. Usa quando precisas de informações recentes ou específicas que não tens.",
                    func=self._web_search
                )
                self.tools.append(web_search_tool)
                logger.info("✅ Ferramenta de pesquisa web ativada")
            except Exception as e:
                logger.warning(f"⚠️ Falha ao configurar pesquisa web: {e}")
        
        # Ferramenta de análise ética
        ethical_analysis_tool = Tool(
            name="ethical_analysis",
            description="Analisa questões éticas complexas usando princípios de filosofia moral e ética aplicada.",
            func=self._ethical_analysis
        )
        self.tools.append(ethical_analysis_tool)
        
        # Ferramenta de reflexão pessoal
        personal_reflection_tool = Tool(
            name="personal_reflection",
            description="Facilita reflexão pessoal e autoconhecimento através de perguntas guiadas.",
            func=self._personal_reflection
        )
        self.tools.append(personal_reflection_tool)
        
        logger.info(f"✅ {len(self.tools)} ferramentas inicializadas")
    
    def _initialize_agent(self):
        """Inicializa o agente executivo com LLM e ferramentas"""
        if not self.llm:
            logger.error("❌ Não é possível criar agente sem LLM")
            return
        
        try:
            # Prompt do sistema para o agente
            system_prompt = """És o Ethic Companion, um assistente de IA especializado em ética, filosofia e desenvolvimento pessoal.

A tua missão é ajudar as pessoas a:
1. 🤔 Refletir sobre questões éticas complexas
2. 🌱 Desenvolver um pensamento crítico mais profundo  
3. 🧭 Navegar dilemas morais com sabedoria
4. 💭 Facilitar autoconhecimento e crescimento pessoal

Características da tua personalidade:
- Empático e compreensivo
- Questionador sem ser julgmental
- Sábio mas humilde
- Prático nas sugestões
- Respeitoso com todas as perspetivas

Usa as ferramentas disponíveis quando apropriado:
- web_search: Para informações atuais ou específicas
- ethical_analysis: Para questões éticas complexas
- personal_reflection: Para facilitar autoconhecimento

Responde sempre em português e mantém um tom caloroso e acessível."""

            # Tentar criar agente com ferramentas (se disponíveis)
            if hasattr(self, 'tools') and self.tools:
                try:
                    # Template do prompt compatível com Gemini
                    prompt = ChatPromptTemplate.from_messages([
                        ("system", system_prompt),
                        MessagesPlaceholder(variable_name="chat_history"),
                        ("human", "{input}"),
                        MessagesPlaceholder(variable_name="agent_scratchpad")
                    ])
                    
                    # Tentar criar agente OpenAI functions (pode funcionar com Gemini)
                    agent = create_openai_functions_agent(self.llm, self.tools, prompt)
                    self.agent_executor = AgentExecutor(
                        agent=agent,
                        tools=self.tools,
                        verbose=True,
                        handle_parsing_errors=True,
                        max_iterations=3,
                        return_intermediate_steps=True
                    )
                    logger.info("✅ Agente com ferramentas inicializado")
                    print("✅ DEBUG - Agente com ferramentas criado com sucesso")
                    
                except Exception as e:
                    print(f"⚠️ DEBUG - Agente com ferramentas falhou, usando LLM direto: {e}")
                    logger.warning(f"⚠️ Falha ao criar agente com ferramentas: {e}")
                    # Fallback para LLM simples
                    self.agent_executor = None
            else:
                self.agent_executor = None
                logger.info("✅ LLM simples inicializado (sem ferramentas)")
                print("✅ DEBUG - LLM simples configurado")
                
        except Exception as e:
            print(f"❌ DEBUG - Erro crítico ao inicializar agente: {e}")
            logger.error(f"❌ Erro ao inicializar agente: {e}")
            self.agent_executor = None
    
    async def process_message(self, message: str, session_id: str) -> Dict[str, Any]:
        """
        Processa uma mensagem do utilizador e retorna resposta
        
        Args:
            message: Mensagem do utilizador
            session_id: ID da sessão para contexto
            
        Returns:
            Dict com resposta e metadados
        """
        try:
            start_time = datetime.now()
            
            # Se temos agente com ferramentas
            if self.agent_executor:
                try:
                    result = await asyncio.get_event_loop().run_in_executor(
                        None, 
                        lambda: self.agent_executor.invoke({
                            "input": message,
                            "chat_history": []  # Memória gerida externamente
                        })
                    )
                    
                    response_text = result.get("output", "Desculpa, não consegui processar a tua mensagem.")
                    tools_used = self._extract_tools_used(result)
                    
                except Exception as e:
                    print(f"🚨 DEBUG - ERRO NO AGENTE EXECUTOR: {e}")
                    print(f"🚨 DEBUG - TIPO DE ERRO: {type(e).__name__}")
                    logger.error(f"❌ Erro no agente executor: {e}")
                    # Fallback para LLM direto
                    response_text = await self._direct_llm_response(message)
                    tools_used = []
            
            # Se só temos LLM direto
            elif self.llm:
                response_text = await self._direct_llm_response(message)
                tools_used = []
            
            # Se não temos nenhum LLM
            else:
                response_text = self._fallback_response(message)
                tools_used = []
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return {
                "response": response_text,
                "session_id": session_id,
                "processing_time": processing_time,
                "tools_used": tools_used,
                "llm_type": self._get_llm_type(),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Erro crítico no processamento: {e}")
            return {
                "response": "Peço desculpa, ocorreu um erro inesperado. Podes tentar reformular a tua pergunta?",
                "session_id": session_id,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def _direct_llm_response(self, message: str) -> str:
        """Resposta direta do LLM sem ferramentas"""
        try:
            system_msg = SystemMessage(content="""És o Ethic Companion, especializado em ética e desenvolvimento pessoal. 
Responde de forma empática, reflexiva e em português.""")
            
            human_msg = HumanMessage(content=message)
            
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.llm.invoke([system_msg, human_msg])
            )
            
            return response.content
            
        except Exception as e:
            logger.error(f"❌ Erro na resposta direta do LLM: {e}")
            return "Desculpa, tive dificuldades em processar a tua mensagem. Podes tentar novamente?"
    
    def _fallback_response(self, message: str) -> str:
        """Resposta de fallback quando nenhum LLM está disponível"""
        return """Olá! Sou o Ethic Companion e estou aqui para ajudar com questões éticas e reflexões pessoais.

Atualmente estou em modo limitado, mas posso oferecer algumas sugestões básicas:

🤔 **Para dilemas éticos**: Considera os princípios de autonomia, beneficência, não-maleficência e justiça.

💭 **Para reflexão pessoal**: Pergunta-te: "Quais são os meus valores fundamentais?" e "Como posso alinhar as minhas ações com esses valores?"

🌱 **Para crescimento**: Pequenos passos consistentes são mais eficazes que grandes mudanças esporádicas.

Podes reformular a tua pergunta ou aguardar que o sistema seja totalmente restaurado."""
    
    def _extract_tools_used(self, agent_result: Dict) -> List[str]:
        """Extrai ferramentas usadas do resultado do agente"""
        tools_used = []
        
        # Esta implementação depende da estrutura específica do LangChain
        # Pode precisar de ajustes baseados na versão
        if "intermediate_steps" in agent_result:
            for step in agent_result["intermediate_steps"]:
                if hasattr(step, 'tool') and step.tool:
                    tools_used.append(step.tool)
        
        return tools_used
    
    def _get_llm_type(self) -> str:
        """Identifica o tipo de LLM em uso"""
        if not self.llm:
            return "none"
        
        if "openai" in str(type(self.llm)).lower():
            return "openai"
        elif "google" in str(type(self.llm)).lower():
            return "gemini"
        else:
            return "unknown"
    
    # IMPLEMENTAÇÕES DAS FERRAMENTAS
    
    def _web_search(self, query: str) -> str:
        """Ferramenta de pesquisa web usando Tavily"""
        try:
            # Implementação simplificada - expandir conforme necessário
            return f"Resultados de pesquisa para '{query}': [Implementar integração Tavily]"
        except Exception as e:
            return f"Erro na pesquisa web: {e}"
    
    def _ethical_analysis(self, dilemma: str) -> str:
        """Ferramenta de análise ética estruturada"""
        try:
            analysis = f"""
**Análise Ética do Dilema:**

**Contexto:** {dilemma}

**Perspetivas Éticas:**
🏛️ **Deontológica (Kant):** Foca no dever e nas regras universais
⚖️ **Consequencialista (Utilitarismo):** Avalia resultados e bem-estar geral  
🌟 **Virtudes (Aristóteles):** Considera o caráter e virtudes morais
🤝 **Ética do Cuidado:** Enfatiza relações e responsabilidade

**Questões para Reflexão:**
- Quais são os stakeholders envolvidos?
- Que valores estão em conflito?
- Quais as consequências de cada opção?
- Que princípios éticos se aplicam?

**Próximos Passos:** Considera estas perspetivas e identifica a tua intuição moral inicial.
"""
            return analysis
        except Exception as e:
            return f"Erro na análise ética: {e}"
    
    def _personal_reflection(self, topic: str) -> str:
        """Ferramenta para facilitar reflexão pessoal"""
        try:
            reflection = f"""
**Reflexão Pessoal sobre: {topic}**

**Perguntas Orientadoras:**
💭 O que sentes quando pensas neste tema?
🎯 Quais são os teus valores relacionados com isto?
🔍 Que experiências passadas influenciam a tua perspetiva?
🌱 Como gostarias de crescer nesta área?
⭐ Que pequeno passo podes dar hoje?

**Sugestão:** Dedica alguns minutos a escrever as tuas respostas. A escrita ajuda a clarificar pensamentos.

**Lembra-te:** Não há respostas certas ou erradas - apenas a tua verdade pessoal neste momento.
"""
            return reflection
        except Exception as e:
            return f"Erro na reflexão pessoal: {e}"
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Retorna status do agente para diagnóstico"""
        return {
            "llm_available": self.llm is not None,
            "llm_type": self._get_llm_type(),
            "agent_executor_available": self.agent_executor is not None,
            "tools_count": len(self.tools),
            "tools_available": [tool.name for tool in self.tools],
            "status": "operational" if self.llm else "limited"
        }

# Instância global do agente
_ai_agent: Optional[EthicCompanionAgent] = None

def get_ai_agent() -> EthicCompanionAgent:
    """
    Dependência FastAPI para obter agente AI
    
    Returns:
        EthicCompanionAgent: Instância do agente configurado
    """
    global _ai_agent
    
    if _ai_agent is None:
        _ai_agent = EthicCompanionAgent()
    
    return _ai_agent

def reinitialize_agent():
    """Reinicializa o agente (útil para atualizações de configuração)"""
    global _ai_agent
    _ai_agent = None
    return get_ai_agent()
