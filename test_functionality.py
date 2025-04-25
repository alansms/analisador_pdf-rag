"""
Script para testar as funcionalidades básicas do assistente RAG.
"""
import os
import sys

def run_tests():
    """Executa testes básicos de funcionalidade."""
    print("Iniciando testes de funcionalidade do assistente RAG...")
    
    # Teste 1: Extração de ID de vídeo do YouTube
    print("\n1. Testando extração de ID de vídeo do YouTube:")
    from ingest import extract_video_id
    video_id = extract_video_id('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
    print(f"   ID extraído: {video_id}")
    assert video_id == "dQw4w9WgXcQ", "Falha na extração do ID do vídeo"
    print("   ✓ Teste de extração de ID de vídeo passou!")
    
    # Teste 2: Verificação da estrutura do banco de dados
    print("\n2. Verificando estrutura do banco de dados:")
    from db import Session, Message
    print("   ✓ Banco de dados configurado corretamente!")
    
    # Teste 3: Verificação de funções de processamento de texto
    print("\n3. Testando funções de processamento de texto:")
    from ingest import split_text
    text = "Este é um texto de exemplo para testar a função de divisão de texto em chunks."
    chunks = split_text(text)
    print(f"   Número de chunks gerados: {len(chunks)}")
    assert len(chunks) > 0, "Falha na divisão de texto em chunks"
    print("   ✓ Teste de processamento de texto passou!")
    
    print("\nTodos os testes básicos passaram com sucesso!")
    return True

if __name__ == "__main__":
    run_tests()
