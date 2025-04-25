# app.py  ―  Streamlit PDF-RAG assistant
# ---------------------------------------------------------------------------
# 1) Forçar SQLite ≥ 3.35 (pysqlite3-binary) para o ChromaDB funcionar
import sys, pysqlite3  # type: ignore
sys.modules["sqlite3"] = pysqlite3

# 2) Compatibilidade NumPy < 2.0 × ChromaDB
import numpy as np
if not hasattr(np, "float_"):  # presente até NumPy < 2.0
    np.float_ = np.float64     # cria alias esperado pelo Chroma

# 3) Alguns wheels do hnswlib não expõem file_handle_count; “stub” seguro
try:
    import hnswlib  # type: ignore
    if not hasattr(hnswlib.Index, "file_handle_count"):
        class _SafeIndex(hnswlib.Index):         # noqa: D101
            @staticmethod
            def file_handle_count() -> int:      # noqa: D401
                return 0
        hnswlib.Index = _SafeIndex
except ModuleNotFoundError:                      # hnswlib ausente
    import types                                # cria stub mínimo
    hnswlib = types.SimpleNamespace(Index=type("I", (), {"file_handle_count": staticmethod(lambda: 0)}))

# ---------------------------------------------------------------------------
import streamlit as st
import tempfile, os, shutil
from typing import List

from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

# -------------------- estado da sessão / chave OpenAI ----------------------
if "api_key_valid" not in st.session_state:
    st.session_state.api_key_valid = False
if "openai_api_key" not in st.session_state:
    st.session_state.openai_api_key = ""

api_key_input = st.text_input("OpenAI API Key", type="password", key="openai_api_key")

if st.session_state.openai_api_key and not st.session_state.api_key_valid:
    try:
        OpenAIEmbeddings(openai_api_key=st.session_state.openai_api_key).embed_query("ping")
        st.success("API key válida ✅")
        st.session_state.api_key_valid = True
    except Exception:
        st.error("Chave inválida ou sem acesso ao modelo ❌")
        st.session_state.api_key_valid = False

# -------------------------- adaptador p/ Chroma ----------------------------
class ChromaEmbeddingFunction:
    def __init__(self, embedding_fn: OpenAIEmbeddings):
        self.embedding_fn = embedding_fn

    def __call__(self, texts: List[str]):            # ingestão
        if isinstance(texts, str):
            texts = [texts]
        return self.embedding_fn.embed_documents(texts)

    def embed_query(self, text: str):                # busca
        return self.embedding_fn.embed_query(text)

    # compat extra
    def embed_documents(self, texts):
        return self.__call__(texts)

# -------------------------- interface Streamlit ----------------------------
st.title("Assistente de Análise de PDF 📄🤖")

uploaded = st.file_uploader("Faça upload de um PDF", type=["pdf"])

if uploaded:
    if st.session_state.api_key_valid:
        shutil.rmtree("chroma_db", ignore_errors=True)
        os.makedirs("chroma_db", exist_ok=True)

        with st.spinner("Ingerindo PDF…"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded.getbuffer())
                tmp_path = tmp.name

            docs = PyPDFLoader(tmp_path).load()

            embeddings = OpenAIEmbeddings(openai_api_key=st.session_state.openai_api_key)
            vectordb = Chroma.from_documents(
                docs,
                embedding=ChromaEmbeddingFunction(embeddings),
                persist_directory="chroma_db",
                collection_name="pdf_collection",
            )
            st.success("PDF ingerido com sucesso!")

        qa = RetrievalQA.from_chain_type(
            llm=ChatOpenAI(openai_api_key=st.session_state.openai_api_key, model_name="gpt-3.5-turbo"),
            retriever=vectordb.as_retriever(),
        )

        question = st.text_input("Digite sua pergunta sobre o documento:")
        if st.button("Perguntar") and question:
            answer = qa.run(question)
            st.markdown("**Resposta:**")
            st.write(answer)
    else:
        st.warning("Insira uma chave da OpenAI antes de prosseguir.")
