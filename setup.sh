#!/bin/bash
# Script de instalação automatizada para o Assistente IA - Processamento de Linguagem Natural
# Este script instala todas as dependências necessárias para executar o aplicativo

echo "=== Iniciando instalação do Assistente IA - Processamento de Linguagem Natural ==="
echo "Este script instalará todas as dependências necessárias para executar o aplicativo."

# Verificar se o Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "Python 3 não encontrado. Por favor, instale o Python 3 antes de continuar."
    exit 1
fi

echo "Python 3 encontrado: $(python3 --version)"

# Criar ambiente virtual (opcional, mas recomendado)
echo "Deseja criar um ambiente virtual para o projeto? (recomendado) [s/n]"
read -r create_venv

if [[ "$create_venv" == "s" || "$create_venv" == "S" || "$create_venv" == "" ]]; then
    echo "Criando ambiente virtual..."
    
    # Verificar se o módulo venv está disponível
    if ! python3 -c "import venv" &> /dev/null; then
        echo "Módulo venv não encontrado. Tentando instalar..."
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            echo "Sistema macOS detectado."
            if command -v brew &> /dev/null; then
                echo "Homebrew encontrado, instalando python3-venv..."
                brew install python3-venv
            else
                echo "Homebrew não encontrado. Por favor, instale o módulo venv manualmente."
                echo "Continuando sem ambiente virtual..."
            fi
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            # Linux
            echo "Sistema Linux detectado."
            if command -v apt-get &> /dev/null; then
                echo "Instalando python3-venv via apt..."
                sudo apt-get update
                sudo apt-get install -y python3-venv
            elif command -v yum &> /dev/null; then
                echo "Instalando python3-venv via yum..."
                sudo yum install -y python3-venv
            else
                echo "Gerenciador de pacotes não reconhecido. Por favor, instale o módulo venv manualmente."
                echo "Continuando sem ambiente virtual..."
            fi
        else
            echo "Sistema operacional não reconhecido. Por favor, instale o módulo venv manualmente."
            echo "Continuando sem ambiente virtual..."
        fi
    fi
    
    # Tentar criar o ambiente virtual novamente
    if python3 -c "import venv" &> /dev/null; then
        python3 -m venv .venv
        
        # Ativar o ambiente virtual
        if [[ -f ".venv/bin/activate" ]]; then
            echo "Ambiente virtual criado com sucesso."
            echo "Ativando ambiente virtual..."
            source .venv/bin/activate
            echo "Ambiente virtual ativado."
        else
            echo "Falha ao criar ambiente virtual. Continuando sem ambiente virtual..."
        fi
    fi
fi

# Atualizar pip
echo "Atualizando pip..."
python3 -m pip install --upgrade pip

# Instalar dependências
echo "Instalando dependências..."

# Verificar se o requirements.txt existe
if [[ -f "requirements.txt" ]]; then
    echo "Arquivo requirements.txt encontrado. Instalando dependências..."
    
    # Instalar dependências do requirements.txt
    python3 -m pip install -r requirements.txt
    
    if [ $? -ne 0 ]; then
        echo "Aviso: Alguns pacotes podem não ter sido instalados corretamente."
        echo "Tentando instalar pacotes essenciais individualmente..."
        
        # Instalar pacotes essenciais individualmente
        python3 -m pip install streamlit
        python3 -m pip install sqlalchemy
        python3 -m pip install chromadb
        python3 -m pip install hnswlib
        python3 -m pip install langchain-community
        python3 -m pip install langchain-openai
        python3 -m pip install langchain-chroma
        python3 -m pip install openai
        python3 -m pip install tiktoken
        python3 -m pip install pypdf
        
        echo "Instalação de pacotes essenciais concluída."
    else
        echo "Todas as dependências foram instaladas com sucesso."
    fi
else
    echo "Arquivo requirements.txt não encontrado. Instalando dependências essenciais..."
    
    # Instalar pacotes essenciais individualmente
    python3 -m pip install streamlit
    python3 -m pip install sqlalchemy
    python3 -m pip install chromadb
    python3 -m pip install hnswlib
    python3 -m pip install langchain-community
    python3 -m pip install langchain-openai
    python3 -m pip install langchain-chroma
    python3 -m pip install openai
    python3 -m pip install tiktoken
    python3 -m pip install pypdf
    
    echo "Instalação de pacotes essenciais concluída."
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
    echo "Por favor, verifique as mensagens de erro acima e tente instalar os pacotes manualmente se necessário."
fi

echo "=== Instalação concluída ==="
echo ""
echo "Para executar o aplicativo, use o seguinte comando:"
if [[ -n "${VIRTUAL_ENV}" ]]; then
    echo "source $(dirname "${VIRTUAL_ENV}")/bin/activate && streamlit run app.py"
else
    echo "streamlit run app.py"
fi
echo ""
echo "Lembre-se de que você precisará de uma chave API válida da OpenAI para usar o aplicativo."
echo "Você pode obter uma chave API em: https://platform.openai.com/api-keys"
