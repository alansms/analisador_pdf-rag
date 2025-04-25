import streamlit as st
from typing import List
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
import tempfile
import os
import shutil

if 'api_key_valid' not in st.session_state:
    st.session_state.api_key_valid = False

if 'openai_api_key' not in st.session_state:
    st.session_state.openai_api_key = ""

# Get OpenAI API key from user
openai_api_key = st.text_input("OpenAI API Key", type="password", key="openai_api_key")

if st.session_state.openai_api_key and not st.session_state.api_key_valid:
    try:
        # quick test call
        OpenAIEmbeddings(openai_api_key=st.session_state.openai_api_key).embed_query("test")
        st.success("API key válida! ✅")
        st.session_state.api_key_valid = True
    except Exception as e:
        st.error("Chave inválida ou sem acesso ao modelo. ❌")
        st.session_state.api_key_valid = False

class ChromaEmbeddingFunction:
    """
    Pequeno adaptador que torna um objeto `OpenAIEmbeddings`
    compatível com a interface esperada pelo ChromaDB.

    * `__call__(texts)` → lista de embeddings (para ingestão/bulk add)
    * `embed_query(text)` → embedding único (para buscas)
    """

    def __init__(self, embedding_function):
        self.embedding_function = embedding_function  # normalmente OpenAIEmbeddings

    # ---------- Interface usada pelo Chroma durante a ingestão ----------
    # Chroma passa SEMPRE uma lista de strings!
    def __call__(self, texts: List[str]) -> List[List[float]]:  # noqa: D401
        if isinstance(texts, str):
            texts = [texts]  # type: ignore[list-item]
        return self.embedding_function.embed_documents(list(texts))

    # ---------- Conveniência para buscas -------------------------------
    def embed_query(self, text: str) -> List[float]:  # noqa: D401
        return self.embedding_function.embed_query(text)

    # Alias for ingestion
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self.__call__(texts)

st.title("Assistente de analise de documentos PDF")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file:
    if st.session_state.openai_api_key and st.session_state.api_key_valid:
        # Clear any existing vector database so each upload starts fresh
        shutil.rmtree("chroma_db", ignore_errors=True)
        os.makedirs("chroma_db", exist_ok=True)
        with st.spinner("Ingerindo PDF..."):
            # write to temp file and load by path
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.getbuffer())
                tmp_path = tmp_file.name
            loader = PyPDFLoader(tmp_path)
            docs = loader.load()

            openai_embeddings = OpenAIEmbeddings(openai_api_key=st.session_state.openai_api_key)
            chroma_func = ChromaEmbeddingFunction(openai_embeddings)

            vectordb = Chroma.from_documents(
                docs,
                embedding=chroma_func,
                persist_directory="chroma_db",
                collection_name="pdf_collection"
            )

            st.success("PDF ingerido com sucesso! 📄")

        qa_chain = RetrievalQA.from_chain_type(
            llm=ChatOpenAI(openai_api_key=st.session_state.openai_api_key, model_name="gpt-3.5-turbo"),
            retriever=vectordb.as_retriever()
        )

        query = st.text_input("Digite sua pergunta sobre o PDF:")
        if st.button("Perguntar"):
            if query:
                response = qa_chain.run(query)
                st.write("Resposta:")
                st.write(response)
            else:
                st.warning("Por favor, insira uma pergunta.")
    else:
        st.warning("Please enter an OpenAI API key.")
