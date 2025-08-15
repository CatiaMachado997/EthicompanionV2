import weaviate
import os
from backend_app.core.config import get_api_key, get_weaviate_config

class VectorMemory:
    """
    Classe para gerenciar memória vetorial usando Weaviate
    """
    
    def __init__(self):
        """
        Inicializa a conexão com Weaviate e cria o schema se necessário
        """
        # Obtém configuração do Weaviate baseada no ambiente
        weaviate_config = get_weaviate_config()
        
        # Conecta ao Weaviate
        try:
            if weaviate_config["scheme"] == "https":
                # Produção - conexão remota com HTTPS
                self.client = weaviate.connect_to_custom(
                    http_host=weaviate_config["host"],
                    http_port=weaviate_config["port"],
                    http_secure=True,
                    auth_credentials=weaviate.auth.AuthApiKey(weaviate_config["api_key"]),
                    skip_init_checks=True
                )
            else:
                # Desenvolvimento local - conexão local
                self.client = weaviate.connect_to_local(
                    host=weaviate_config["host"],
                    port=weaviate_config["port"],
                    auth_credentials=weaviate.auth.AuthApiKey(weaviate_config["api_key"]),
                    skip_init_checks=True
                )
            
            # Cria o schema se não existir
            self._create_schema()
        except Exception as e:
            raise ValueError(f"Failed to connect to Weaviate: {e}")
    
    def _create_schema(self):
        """
        Cria o schema para a classe MemoryItem se não existir
        """
        try:
            # Verifica se a coleção já existe
            collections = self.client.collections.list_all()
            collection_names = []
            for col in collections:
                if hasattr(col, 'name'):
                    collection_names.append(col.name)
                elif isinstance(col, str):
                    collection_names.append(col)
                else:
                    # Se não conseguirmos obter o nome, vamos tentar criar a coleção
                    collection_names = []
                    break
            
            if "MemoryItem" not in collection_names:
                # Cria a coleção MemoryItem
                self.client.collections.create(
                    name="MemoryItem",
                    description="Itens de memória vetorial",
                    properties=[
                        weaviate.classes.config.Property(
                            name="text",
                            data_type=weaviate.classes.config.DataType.TEXT
                        )
                    ]
                )
                print("✅ Coleção MemoryItem criada com sucesso!")
            else:
                print("✅ Coleção MemoryItem já existe!")
                
        except Exception as e:
            print(f"Erro ao criar schema: {e}")
            # Se houver erro, tenta criar a coleção de qualquer forma
            try:
                self.client.collections.create(
                    name="MemoryItem",
                    description="Itens de memória vetorial",
                    properties=[
                        weaviate.classes.config.Property(
                            name="text",
                            data_type=weaviate.classes.config.DataType.TEXT
                        )
                    ]
                )
                print("✅ Coleção MemoryItem criada com sucesso após erro!")
            except Exception as e2:
                print(f"Erro ao criar coleção após falha: {e2}")
    
    def add_memory(self, text: str):
        """
        Adiciona um novo item de memória
        
        Args:
            text: Texto a ser armazenado
        """
        try:
            data = {"text": text}
            self.client.collections.get("MemoryItem").data.insert(data)
            print(f"✅ Memória adicionada: {text[:50]}...")
        except Exception as e:
            print(f"Erro ao adicionar memória: {e}")
    
    def search_memory(self, query_text: str, limit: int = 3):
        """
        Pesquisa memórias similares usando busca por palavras-chave
        
        Args:
            query_text: Texto para pesquisa
            limit: Número máximo de resultados
            
        Returns:
            Lista de textos mais relevantes
        """
        try:
            # Extrair palavras-chave da query
            keywords = query_text.lower().split()
            # Filtrar palavras muito comuns
            common_words = {'a', 'o', 'e', 'é', 'de', 'da', 'do', 'em', 'um', 'uma', 'com', 'para', 'por', 'que', 'qual', 'quem', 'como', 'quando', 'onde', 'porque', 'minha', 'meu', 'sua', 'seu', 'é', 'são', 'está', 'estão'}
            keywords = [word for word in keywords if word not in common_words and len(word) > 2]
            
            print(f"🔍 Palavras-chave extraídas: {keywords}")
            
            # Buscar por cada palavra-chave
            all_results = []
            for keyword in keywords:
                response = (
                    self.client.collections.get("MemoryItem")
                    .query
                    .fetch_objects(
                        limit=limit * 2,  # Buscar mais resultados para ter mais opções
                        filters=weaviate.classes.query.Filter.by_property("text").contains_any([keyword])
                    )
                )
                
                for obj in response.objects:
                    text = obj.properties["text"]
                    if text not in all_results:
                        all_results.append(text)
            
            # Ordenar por relevância (memórias mais recentes primeiro)
            # Como não temos timestamp, vamos retornar os primeiros resultados únicos
            return all_results[:limit]
            
        except Exception as e:
            print(f"Erro na pesquisa: {e}")
            return []
    
    def close(self):
        """
        Fecha a conexão com o Weaviate
        """
        if hasattr(self, 'client'):
            self.client.close() 