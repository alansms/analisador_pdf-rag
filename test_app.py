"""
Script para testar a execução completa da aplicação
"""
import os
import sys
import subprocess
import time

def print_header(message):
    print("\n" + "=" * 80)
    print(f" {message} ".center(80, "="))
    print("=" * 80)

def print_step(message):
    print(f"\n>> {message}")

def run_command(command, cwd=None):
    print(f"Executando: {command}")
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            check=True, 
            text=True, 
            capture_output=True,
            cwd=cwd
        )
        print(f"Saída: {result.stdout}")
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Erro: {e}")
        print(f"Saída de erro: {e.stderr}")
        return False, e.stderr

def check_imports():
    print_step("Verificando importações essenciais")
    
    modules = [
        "streamlit",
        "sqlalchemy",
        "chromadb",
        "hnswlib",
        "langchain_openai",
        "langchain_community",
        "openai",
        "tiktoken",
        "pypdf"
    ]
    
    all_ok = True
    for module in modules:
        try:
            __import__(module)
            print(f"✅ Módulo {module} importado com sucesso")
        except ImportError as e:
            print(f"❌ Erro ao importar {module}: {e}")
            all_ok = False
    
    return all_ok

def check_files():
    print_step("Verificando arquivos essenciais")
    
    files = [
        "app.py",
        "streamlit_app.py",
        "ingest.py",
        "gpt_utils.py",
        "db.py",
        "requirements.txt",
        "setup.sh"
    ]
    
    all_ok = True
    for file in files:
        if os.path.exists(file):
            print(f"✅ Arquivo {file} encontrado")
        else:
            print(f"❌ Arquivo {file} não encontrado")
            all_ok = False
    
    return all_ok

def check_directories():
    print_step("Verificando diretórios necessários")
    
    directories = ["tmp", "db"]
    
    for directory in directories:
        if not os.path.exists(directory):
            print(f"Criando diretório {directory}")
            os.makedirs(directory, exist_ok=True)
        print(f"✅ Diretório {directory} verificado")
    
    return True

def main():
    print_header("TESTE DE EXECUÇÃO COMPLETA")
    print("Este script verifica se a aplicação está pronta para execução")
    
    # Verificar arquivos
    if not check_files():
        print("❌ Alguns arquivos essenciais estão faltando. Verifique os erros acima.")
        return False
    
    # Verificar diretórios
    check_directories()
    
    # Verificar importações
    if not check_imports():
        print("\n❌ Algumas dependências estão faltando.")
        print("Recomendação: Execute o script setup.sh para instalar todas as dependências:")
        print("  ./setup.sh")
        return False
    
    print_header("TESTE CONCLUÍDO COM SUCESSO")
    print("\nA aplicação está pronta para execução!")
    print("\nPara executar a aplicação, use o comando:")
    print("  streamlit run app.py")
    print("\nLembre-se de que você precisará de uma chave API válida da OpenAI.")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
