#!/bin/bash
# Script de instalação e execução para o Assistente IA - Processamento de Linguagem Natural
# Este script instala todas as dependências necessárias e executa a aplicação

echo "=== Assistente IA - Processamento de Linguagem Natural ==="
echo "Este script instalará todas as dependências e iniciará a aplicação automaticamente."

# Verificar se o Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "Python 3 não encontrado. Por favor, instale o Python 3 antes de continuar."
    exit 1
fi

echo "Python 3 encontrado: $(python3 --version)"

# Instalar dependências essenciais diretamente
echo "Instalando dependências essenciais..."

# Tentar instalar com pip3 primeiro (macOS/Linux)
if command -v pip3 &> /dev/null; then
    pip3 install streamlit sqlalchemy chromadb hnswlib langchain-community langchain-openai langchain-chroma openai tiktoken pypdf
elif command -v pip &> /dev/null; then
    pip install streamlit sqlalchemy chromadb hnswlib langchain-community langchain-openai langchain-chroma openai tiktoken pypdf
else
    echo "Pip não encontrado. Tentando instalar com python3 -m pip..."
    python3 -m pip install streamlit sqlalchemy chromadb hnswlib langchain-community langchain-openai langchain-chroma openai tiktoken pypdf
fi

# Criar diretórios necessários
echo "Criando diretórios necessários..."
mkdir -p tmp
mkdir -p db

# Verificar se a instalação foi bem-sucedida
echo "Verificando instalação..."
if python3 -c "import streamlit, sqlalchemy, chromadb, hnswlib, langchain_community, langchain_openai, openai, tiktoken, pypdf" &> /dev/null; then
    echo "Verificação concluída. Todos os pacotes essenciais foram instalados com sucesso."
else
    echo "Aviso: Alguns pacotes essenciais podem não ter sido instalados corretamente."
    echo "Tentando instalar novamente com --user flag..."
    python3 -m pip install --user streamlit sqlalchemy chromadb hnswlib langchain-community langchain-openai langchain-chroma openai tiktoken pypdf
fi

echo "=== Instalação concluída ==="
echo ""
echo "Iniciando a aplicação..."
streamlit run app.py
