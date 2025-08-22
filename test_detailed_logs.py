#!/usr/bin/env python3
"""
Script para capturar logs detalhados do servidor backend
"""
import asyncio
import aiohttp
import subprocess
import time
import threading
import queue
import sys
import os

def read_server_output(process, output_queue):
    """Lê output do servidor em thread separada"""
    try:
        for line in iter(process.stdout.readline, ''):
            if line:
                output_queue.put(line.strip())
    except Exception as e:
        output_queue.put(f"Erro ao ler output: {e}")

async def test_api_and_capture_logs():
    """Testa API e captura logs do servidor"""
    print("🚀 Iniciando servidor e capturando logs...")
    
    # Iniciar servidor
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
    
    # Queue para capturar output
    output_queue = queue.Queue()
    
    # Thread para ler output do servidor
    output_thread = threading.Thread(
        target=read_server_output,
        args=(process, output_queue),
        daemon=True
    )
    output_thread.start()
    
    # Aguardar inicialização
    print("⏳ Aguardando servidor inicializar...")
    await asyncio.sleep(5)
    
    # Capturar logs iniciais
    print("\n📋 LOGS INICIAIS DO SERVIDOR:")
    print("=" * 50)
    while not output_queue.empty():
        try:
            log_line = output_queue.get_nowait()
            print(log_line)
        except queue.Empty:
            break
    print("=" * 50)
    
    # Fazer chamada à API
    print("\n🧪 Fazendo chamada à API...")
    
    try:
        async with aiohttp.ClientSession() as session:
            data = {"message": "O que é ética? Explica-me de forma detalhada."}
            
            async with session.post(
                "http://localhost:8000/api/message",
                json=data,
                headers={"Content-Type": "application/json"}
            ) as response:
                
                print(f"📊 Status da resposta: {response.status}")
                result = await response.json()
                print(f"📝 Resposta da API: {result.get('response', 'Sem resposta')[:100]}...")
                
    except Exception as e:
        print(f"❌ Erro na chamada à API: {e}")
    
    # Aguardar e capturar logs após a chamada
    print("\n⏳ Aguardando logs do processamento...")
    await asyncio.sleep(3)
    
    print("\n📋 LOGS APÓS CHAMADA À API:")
    print("=" * 50)
    while not output_queue.empty():
        try:
            log_line = output_queue.get_nowait()
            print(log_line)
        except queue.Empty:
            break
    print("=" * 50)
    
    # Parar servidor
    print("\n🛑 Parando servidor...")
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()

if __name__ == "__main__":
    # Mudar para o diretório correto
    os.chdir("/Users/catiamachado/Documents/Ethic Companion V2")
    
    # Executar teste
    asyncio.run(test_api_and_capture_logs())
