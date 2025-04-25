# Assistente Virtual RAG para Processamento de Linguagem Natural

Um assistente virtual baseado em IA utilizando a arquitetura RAG (Retrieval Augmented Generation) para responder perguntas sobre os avanços mais recentes em processamento de linguagem natural.

## Funcionalidades

- Interface moderna e dinâmica com Streamlit
- Validação de chave API da OpenAI
- Ingestão de dados de múltiplas fontes:
  - Documentos PDF
  - Vídeos do YouTube (transcrições)
- Processamento de texto com chunking inteligente
- Armazenamento vetorial com ChromaDB
- Respostas baseadas em contexto usando GPT
- Histórico de conversas

## Requisitos

- Python 3.10+
- Chave API da OpenAI

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/assistente-rag-pln.git
cd assistente-rag-pln
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure sua chave API da OpenAI:
   - Crie um arquivo `.env` na raiz do projeto
   - Adicione sua chave API: `OPENAI_API_KEY=sua-chave-aqui`
   - Ou insira a chave diretamente na interface web

## Uso

Execute o aplicativo Streamlit:
```bash
streamlit run app.py
```

Acesse o aplicativo em seu navegador em `http://localhost:8501`

### Ingestão de Dados

1. Valide sua chave API da OpenAI
2. Escolha o tipo de conteúdo (PDF ou vídeo do YouTube)
3. Faça upload de PDFs ou insira URLs do YouTube
4. Clique em "Iniciar Ingestão"

### Consulta

1. Digite sua pergunta no campo de texto
2. Clique em "Enviar Pergunta"
3. Veja a resposta gerada com base nos documentos ingeridos

## Estrutura do Projeto

- `app.py`: Interface principal do Streamlit
- `ingest.py`: Processamento e ingestão de dados
- `gpt_utils.py`: Funções para interação com a API da OpenAI
- `db.py`: Configuração do banco de dados para histórico de conversas
- `requirements.txt`: Dependências do projeto

## Deploy no Streamlit.app

Este projeto está configurado para ser facilmente implantado no Streamlit.app:

1. Faça fork deste repositório para sua conta GitHub
2. Acesse [streamlit.io/cloud](https://streamlit.io/cloud)
3. Conecte sua conta GitHub
4. Selecione o repositório e implante

## Licença

MIT

## Créditos

Desenvolvido como parte de um projeto de assistente virtual baseado em IA para processamento de linguagem natural.
