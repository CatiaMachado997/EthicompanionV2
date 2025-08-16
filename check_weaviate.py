#!/usr/bin/env python3
"""
🔍 Check Weaviate - Script de Verificação da Base de Dados Vetorial

Este script conecta-se ao Weaviate local e verifica o estado da coleção MemoryItem.
Mostra o número total de objetos armazenados na base de dados vetorial.
"""

import os
import sys
from dotenv import load_dotenv
import weaviate
from weaviate.exceptions import WeaviateConnectionError, WeaviateStartUpError

def load_environment():
    """Carrega as variáveis de ambiente do ficheiro .env"""
    print("🔧 Carregando variáveis de ambiente...")
    
    # Carrega o ficheiro .env
    load_dotenv()
    
    # Obtém as configurações do Weaviate
    weaviate_url = os.getenv('WEAVIATE_URL', 'http://localhost:8080')
    weaviate_api_key = os.getenv('WEAVIATE_API_KEY')
    
    print(f"   📍 URL: {weaviate_url}")
    print(f"   🔑 API Key: {'✅ Configurada' if weaviate_api_key else '⚠️  Não configurada'}")
    
    return weaviate_url, weaviate_api_key

def connect_to_weaviate(url, api_key):
    """Conecta-se ao Weaviate"""
    print(f"\n🔗 Conectando ao Weaviate em {url}...")
    
    try:
        # Determina o host e porta da URL
        if url.startswith('http://'):
            host = url.replace('http://', '').split(':')[0]
            port = int(url.replace('http://', '').split(':')[1]) if ':' in url.replace('http://', '') else 8080
        else:
            host = 'localhost'
            port = 8080
        
        # Conecta com ou sem API key
        if api_key and api_key.strip():
            print(f"   🔐 Conectando com autenticação...")
            client = weaviate.connect_to_local(
                host=host,
                port=port,
                auth_credentials=weaviate.auth.AuthApiKey(api_key),
                skip_init_checks=True
            )
        else:
            print(f"   🔓 Conectando sem autenticação...")
            client = weaviate.connect_to_local(
                host=host,
                port=port,
                skip_init_checks=True
            )
        
        # Testa a conexão
        meta = client.get_meta()
        print(f"   ✅ Conexão estabelecida!")
        print(f"   📊 Versão do Weaviate: {meta.get('version', 'Desconhecida')}")
        
        return client
        
    except WeaviateConnectionError as e:
        print(f"   ❌ Erro de conexão: {e}")
        return None
    except WeaviateStartUpError as e:
        print(f"   ❌ Erro de inicialização: {e}")
        return None
    except Exception as e:
        print(f"   ❌ Erro inesperado: {e}")
        return None

def check_memory_collection(client):
    """Verifica a coleção MemoryItem"""
    print(f"\n🗃️  Verificando coleção 'MemoryItem'...")
    
    try:
        # Lista todas as coleções disponíveis
        collections = client.collections.list_all()
        collection_names = []
        
        print(f"   📋 Coleções disponíveis:")
        for collection in collections:
            if hasattr(collection, 'name'):
                name = collection.name
            elif isinstance(collection, str):
                name = collection
            else:
                name = str(collection)
            
            collection_names.append(name)
            print(f"      - {name}")
        
        # Verifica se MemoryItem existe
        if "MemoryItem" not in collection_names:
            print(f"   ⚠️  Coleção 'MemoryItem' não encontrada!")
            print(f"   💡 A coleção será criada automaticamente quando o primeiro item for adicionado.")
            return 0
        
        # Conta os objetos na coleção MemoryItem
        memory_collection = client.collections.get("MemoryItem")
        
        # Faz uma query para contar todos os objetos
        response = memory_collection.query.fetch_objects(limit=10000)  # Limite alto para contar todos
        
        total_count = len(response.objects) if response.objects else 0
        
        print(f"   ✅ Coleção 'MemoryItem' encontrada!")
        print(f"   📊 Total de objetos: {total_count}")
        
        # Mostra alguns exemplos se existirem
        if total_count > 0 and response.objects:
            print(f"\n   🔍 Primeiros itens da memória:")
            for i, obj in enumerate(response.objects[:5], 1):
                text = obj.properties.get('text', 'Texto não disponível')
                # Limita o texto e remove quebras de linha para melhor apresentação
                display_text = text.replace('\n', ' ').replace('\r', ' ')[:80]
                print(f"      {i}. {display_text}{'...' if len(display_text) == 80 else ''}")
            
            if total_count > 5:
                print(f"      ... e mais {total_count - 5} itens")
        
        return total_count
        
    except Exception as e:
        print(f"   ❌ Erro ao verificar coleção: {e}")
        return None

def main():
    """Função principal"""
    print("🧠 Check Weaviate - Verificação da Base de Dados Vetorial")
    print("=" * 60)
    
    try:
        # 1. Carrega variáveis de ambiente
        weaviate_url, weaviate_api_key = load_environment()
        
        # 2. Conecta ao Weaviate
        client = connect_to_weaviate(weaviate_url, weaviate_api_key)
        
        if not client:
            print("\n❌ Falha na conexão com o Weaviate!")
            print("💡 Certifica-te de que o Weaviate está a correr:")
            print("   docker run -d -p 8080:8080 -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true semitechnologies/weaviate:latest")
            sys.exit(1)
        
        # 3. Verifica a coleção MemoryItem
        total_items = check_memory_collection(client)
        
        # 4. Fecha a conexão
        client.close()
        
        # 5. Resultado final
        print("\n" + "=" * 60)
        if total_items is not None:
            print(f"🎯 RESULTADO FINAL: {total_items} itens encontrados na coleção MemoryItem")
            
            if total_items == 0:
                print("💡 A base de dados de memória está vazia.")
                print("   Para adicionar memórias, use o chat do Ethic Companion.")
            else:
                print(f"✅ A base de dados de memória contém {total_items} item{'s' if total_items != 1 else ''}.")
        else:
            print("❌ Não foi possível verificar a coleção MemoryItem.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Verificação interrompida pelo utilizador.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
