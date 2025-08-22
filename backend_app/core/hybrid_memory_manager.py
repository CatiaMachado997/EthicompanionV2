"""
Sistema de Memória Híbrida - MemoryManager
Combina PostgreSQL (memória episódica) com Weaviate (memória semântica)
"""

import asyncio
import logging
from typing import List, Dict, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import text
import weaviate
import json

logger = logging.getLogger(__name__)

class MemoryManager:
    """
    Gestor de memória híbrida que combina:
    - PostgreSQL: Armazenamento episódico sequencial das conversas
    - Weaviate: Pesquisa semântica baseada em embeddings vetoriais
    """
    
    def __init__(self, db_session: Session, weaviate_client: weaviate.Client):
        """
        Inicializa o MemoryManager com clientes para ambas as bases de dados
        
        Args:
            db_session: Sessão SQLAlchemy para PostgreSQL
            weaviate_client: Cliente configurado do Weaviate
        """
        self.db = db_session
        self.weaviate = weaviate_client
        self.collection_name = "ConversationMemory"
        
        # Garantir que a coleção existe no Weaviate
        self._ensure_weaviate_schema()
    
    def _ensure_weaviate_schema(self):
        """Cria o esquema do Weaviate se não existir"""
        try:
            # Verificar se a coleção já existe
            if not self.weaviate.schema.exists(self.collection_name):
                schema = {
                    "class": self.collection_name,
                    "description": "Memórias de conversas para pesquisa semântica",
                    "vectorizer": "none",  # Sem vectorizer automático para teste
                    "properties": [
                        {
                            "name": "content",
                            "dataType": ["text"],
                            "description": "Conteúdo combinado da conversa"
                        },
                        {
                            "name": "session_id",
                            "dataType": ["string"],
                            "description": "ID da sessão da conversa"
                        },
                        {
                            "name": "timestamp",
                            "dataType": ["date"],
                            "description": "Timestamp da conversa"
                        },
                        {
                            "name": "user_message",
                            "dataType": ["text"],
                            "description": "Mensagem original do utilizador"
                        },
                        {
                            "name": "assistant_message", 
                            "dataType": ["text"],
                            "description": "Resposta do assistente"
                        }
                    ]
                }
                
                self.weaviate.schema.create_class(schema)
                logger.info(f"✅ Coleção {self.collection_name} criada no Weaviate")
            else:
                logger.info(f"✅ Coleção {self.collection_name} já existe no Weaviate")
                
        except Exception as e:
            logger.error(f"❌ Erro ao configurar esquema Weaviate: {e}")
    
    def add_message(self, session_id: str, user_message: str, assistant_message: str) -> bool:
        """
        Guarda uma troca de mensagens em ambas as bases de dados
        
        Args:
            session_id: Identificador único da sessão
            user_message: Mensagem do utilizador
            assistant_message: Resposta do assistente
            
        Returns:
            bool: True se guardado com sucesso, False caso contrário
        """
        try:
            timestamp = datetime.now()
            
            # 1. POSTGRESQL - Guardar mensagens individuais na tabela chat_history
            self._save_to_postgresql(session_id, user_message, assistant_message, timestamp)
            
            # 2. WEAVIATE - Criar documento combinado para pesquisa semântica
            self._save_to_weaviate(session_id, user_message, assistant_message, timestamp)
            
            logger.info(f"✅ Conversa guardada - Sessão: {session_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao guardar conversa: {e}")
            self.db.rollback()
            return False
    
    def _save_to_postgresql(self, session_id: str, user_message: str, assistant_message: str, timestamp: datetime):
        """Guarda mensagens individuais no PostgreSQL"""
        try:
            # Inserir mensagem do utilizador
            user_query = text("""
                INSERT INTO chat_history (session_id, user_message, assistant_message, timestamp, message_type)
                VALUES (:session_id, :user_message, NULL, :timestamp, 'user')
            """)
            
            self.db.execute(user_query, {
                'session_id': session_id,
                'user_message': user_message,
                'timestamp': timestamp
            })
            
            # Inserir resposta do assistente
            assistant_query = text("""
                INSERT INTO chat_history (session_id, user_message, assistant_message, timestamp, message_type)
                VALUES (:session_id, NULL, :assistant_message, :timestamp, 'assistant')
            """)
            
            self.db.execute(assistant_query, {
                'session_id': session_id,
                'assistant_message': assistant_message,
                'timestamp': timestamp
            })
            
            self.db.commit()
            logger.debug(f"💾 Mensagens guardadas no PostgreSQL - Sessão: {session_id}")
            
        except Exception as e:
            logger.error(f"❌ Erro PostgreSQL: {e}")
            self.db.rollback()
            raise
    
    def _save_to_weaviate(self, session_id: str, user_message: str, assistant_message: str, timestamp: datetime):
        """Cria documento combinado e guarda no Weaviate"""
        try:
            # Combinar mensagens num documento único para pesquisa semântica
            combined_content = f"""Utilizador: {user_message}

Assistente: {assistant_message}"""
            
            # Preparar objeto para Weaviate
            data_object = {
                "content": combined_content,
                "session_id": session_id,
                "timestamp": timestamp.isoformat(),
                "user_message": user_message,
                "assistant_message": assistant_message
            }
            
            # Guardar no Weaviate com vetorização automática
            result = self.weaviate.data_object.create(
                data_object=data_object,
                class_name=self.collection_name
            )
            
            logger.debug(f"🔍 Documento vetorizado no Weaviate - ID: {result}")
            
        except Exception as e:
            logger.error(f"❌ Erro Weaviate: {e}")
            raise
    
    async def get_context(self, session_id: str, query: str, recent_limit: int = 5, semantic_limit: int = 3) -> str:
        """
        Recupera contexto híbrido combinando histórico recente e memórias relevantes
        
        Args:
            session_id: ID da sessão atual
            query: Pergunta/contexto para pesquisa semântica
            recent_limit: Número de mensagens recentes a recuperar
            semantic_limit: Número de resultados semânticos a recuperar
            
        Returns:
            str: Contexto formatado combinando ambos os tipos de memória
        """
        try:
            # Executar ambas as pesquisas em paralelo para melhor performance
            recent_task = asyncio.create_task(self._get_recent_history(session_id, recent_limit))
            semantic_task = asyncio.create_task(self._get_semantic_memories(query, semantic_limit, session_id))
            
            recent_history, semantic_memories = await asyncio.gather(recent_task, semantic_task)
            
            # Formatar contexto final
            context = self._format_context(recent_history, semantic_memories)
            
            logger.info(f"🧠 Contexto recuperado - Sessão: {session_id}, Recentes: {len(recent_history)}, Semânticas: {len(semantic_memories)}")
            return context
            
        except Exception as e:
            logger.error(f"❌ Erro ao recuperar contexto: {e}")
            return "Contexto não disponível devido a erro interno."
    
    async def _get_recent_history(self, session_id: str, limit: int) -> List[Dict]:
        """Recupera histórico recente do PostgreSQL"""
        try:
            query = text("""
                SELECT user_message, assistant_message, timestamp, message_type
                FROM chat_history 
                WHERE session_id = :session_id 
                ORDER BY timestamp DESC 
                LIMIT :limit
            """)
            
            result = self.db.execute(query, {
                'session_id': session_id,
                'limit': limit * 2  # *2 porque cada troca tem 2 mensagens
            })
            
            messages = []
            for row in result:
                if row.message_type == 'user' and row.user_message:
                    messages.append({
                        'type': 'user',
                        'content': row.user_message,
                        'timestamp': row.timestamp
                    })
                elif row.message_type == 'assistant' and row.assistant_message:
                    messages.append({
                        'type': 'assistant', 
                        'content': row.assistant_message,
                        'timestamp': row.timestamp
                    })
            
            # Inverter para ordem cronológica
            return list(reversed(messages))
            
        except Exception as e:
            logger.error(f"❌ Erro ao recuperar histórico recente: {e}")
            return []
    
    async def _get_semantic_memories(self, query: str, limit: int, current_session_id: str) -> List[Dict]:
        """Recupera memórias semanticamente relevantes do Weaviate"""
        try:
            # Pesquisa semântica no Weaviate
            result = self.weaviate.query.get(
                self.collection_name, 
                ["content", "session_id", "timestamp", "user_message", "assistant_message"]
            ).with_near_text({
                "concepts": [query],
                "certainty": 0.7  # Threshold para relevância
            }).with_limit(limit + 5).do()  # +5 para filtrar sessão atual
            
            memories = []
            objects = result.get("data", {}).get("Get", {}).get(self.collection_name, [])
            
            for obj in objects:
                # Filtrar memórias da sessão atual (para evitar redundância)
                if obj.get("session_id") != current_session_id:
                    memories.append({
                        'content': obj.get("content", ""),
                        'session_id': obj.get("session_id", ""),
                        'timestamp': obj.get("timestamp", ""),
                        'user_message': obj.get("user_message", ""),
                        'assistant_message': obj.get("assistant_message", "")
                    })
                    
                    if len(memories) >= limit:
                        break
            
            return memories
            
        except Exception as e:
            logger.error(f"❌ Erro na pesquisa semântica: {e}")
            return []
    
    def _format_context(self, recent_history: List[Dict], semantic_memories: List[Dict]) -> str:
        """Formata o contexto final combinando ambos os tipos de memória"""
        context_parts = []
        
        # SECÇÃO 1: Histórico Recente
        if recent_history:
            context_parts.append("📚 **HISTÓRICO RECENTE DA CONVERSA**")
            context_parts.append("=" * 50)
            
            for msg in recent_history:
                if msg['type'] == 'user':
                    context_parts.append(f"🙋 **Utilizador:** {msg['content']}")
                else:
                    context_parts.append(f"🤖 **Assistente:** {msg['content']}")
                context_parts.append("")
        else:
            context_parts.append("📚 **HISTÓRICO RECENTE DA CONVERSA**")
            context_parts.append("(Nenhum histórico recente disponível)")
            context_parts.append("")
        
        # SECÇÃO 2: Memórias Relevantes
        if semantic_memories:
            context_parts.append("🧠 **MEMÓRIAS RELEVANTES DE CONVERSAS ANTERIORES**")
            context_parts.append("=" * 50)
            
            for i, memory in enumerate(semantic_memories, 1):
                context_parts.append(f"**Memória {i}** (Sessão: {memory['session_id']})")
                context_parts.append(f"🙋 **Utilizador:** {memory['user_message']}")
                context_parts.append(f"🤖 **Assistente:** {memory['assistant_message']}")
                context_parts.append("")
        else:
            context_parts.append("🧠 **MEMÓRIAS RELEVANTES DE CONVERSAS ANTERIORES**")
            context_parts.append("(Nenhuma memória relevante encontrada)")
            context_parts.append("")
        
        return "\n".join(context_parts)
    
    def get_memory_stats(self) -> Dict:
        """Retorna estatísticas sobre o sistema de memória"""
        try:
            # Stats PostgreSQL
            pg_query = text("""
                SELECT 
                    COUNT(*) as total_messages,
                    COUNT(DISTINCT session_id) as unique_sessions,
                    MAX(timestamp) as last_message
                FROM chat_history
            """)
            
            pg_result = self.db.execute(pg_query).fetchone()
            
            # Stats Weaviate
            wv_result = self.weaviate.query.aggregate(self.collection_name).with_meta_count().do()
            wv_count = wv_result.get("data", {}).get("Aggregate", {}).get(self.collection_name, [{}])[0].get("meta", {}).get("count", 0)
            
            return {
                "postgresql": {
                    "total_messages": pg_result.total_messages or 0,
                    "unique_sessions": pg_result.unique_sessions or 0,
                    "last_message": pg_result.last_message.isoformat() if pg_result.last_message and hasattr(pg_result.last_message, 'isoformat') else str(pg_result.last_message) if pg_result.last_message else None
                },
                "weaviate": {
                    "total_vectors": wv_count,
                    "collection_name": self.collection_name
                },
                "status": "operational"
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao obter estatísticas: {e}")
            return {"status": "error", "message": str(e)}
    
    def close(self):
        """Fecha as ligações às bases de dados"""
        try:
            if self.db:
                self.db.close()
            logger.info("🔒 MemoryManager fechado")
        except Exception as e:
            logger.error(f"❌ Erro ao fechar MemoryManager: {e}")
