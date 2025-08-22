#!/usr/bin/env python3
"""
Script para testar o sistema de logging do backend
"""
import asyncio
import aiohttp
import subprocess
import time
import signal
import sys
import os

async def test_api_call():
    """Faz uma chamada à API para testar o logging"""
    try:
        async with aiohttp.ClientSession() as session:
            data = {"message": "O que é ética? Preciso de uma resposta completa."}
            
            async with session.post(
                "http://localhost:8000/api/message",
                json=data,
                headers={"Content-Type": "application/json"}
            ) as response:
                
                print(f"Status: {response.status}")
                result = await response.json()
                print(f"Resposta: {result}")
                return result
                
    except Exception as e:
        print(f"Erro na chamada à API: {e}")
        return None

def start_server():
    """Inicia o servidor backend"""
    print("🚀 Iniciando servidor backend...")
    
    cmd = [
        sys.executable, "-m", "uvicorn",
        "backend_app.api.chat_with_memory:app",
        "--host", "0.0.0.0",
        "--port", "8000"
    ]
    
    process = subprocess.Popen(
        cmd,
        cwd="/Users/catiamachado/Documents/Ethic Companion V2",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        universal_newlines=True
    )
    
    return process

async def main():
    """Função principal"""
    server_process = None
    
    try:
        # Iniciar servidor
        server_process = start_server()
        
        # Aguardar inicialização
        print("⏳ Aguardando servidor inicializar...")
        await asyncio.sleep(5)
        
        # Verificar se servidor está vivo
        if server_process.poll() is not None:
            stdout, stderr = server_process.communicate()
            print(f"❌ Servidor falhou ao iniciar:")
            print(f"STDOUT: {stdout}")
            print(f"STDERR: {stderr}")
            return
        
        print("✅ Servidor iniciado, fazendo teste...")
        
        # Fazer teste da API
        result = await test_api_call()
        
        if result:
            print("✅ Teste da API concluído!")
        else:
            print("❌ Teste da API falhou!")
        
        # Aguardar um pouco para ver os logs
        print("⏳ Aguardando para ver logs do servidor...")
        await asyncio.sleep(3)
        
    except Exception as e:
        print(f"❌ Erro durante teste: {e}")
        
    finally:
        # Parar servidor
        if server_process and server_process.poll() is None:
            print("🛑 Parando servidor...")
            server_process.terminate()
            try:
                server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server_process.kill()
                server_process.wait()

if __name__ == "__main__":
    # Mudar para o diretório correto
    os.chdir("/Users/catiamachado/Documents/Ethic Companion V2")
    
    # Executar teste
    asyncio.run(main())
