# app.py
# ─────────────────────────────────────────────────────────────────────────────
# Corrige SQLite (<3.35), hnswlib.file_handle_count e passa Settings ao Chroma
# ─────────────────────────────────────────────────────────────────────────────

# ▸ SQLite ≥ 3.35 via pysqlite3
import sys, types
import pysqlite3
sys.modules["sqlite3"] = pysqlite3

# ▸ hnswlib patch (evita TypeError em file_handle_count)
try:
    import hnswlib
except ModuleNotFoundError:
    hnswlib = types.ModuleType("hnswlib")       # stub
    class _DummyIndex: pass
    hnswlib.Index = _DummyIndex                 # type: ignore
hnswlib.Index.file_handle_count = 0             # sempre inteiro

# ─ Streamlit / LangChain stack ───────────────────────────────────────────────
import os, shutil, tempfile
from typing import List, Sequence

import streamlit as st

from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

from chromadb.config import Settings            # ← NEW


# ╭─ Estado de sessão ───────────────────────────────────────────────────────╮
if "api_key_valid" not in st.session_state:
    st.session_state.api_key_valid = False
if "openai_api_key" not in st.session_state:
    st.session_state.openai_api_key = ""
# ╰──────────────────────────────────────────────────────────────────────────╯


st.title("Assistente de Análise de PDFs 📑")

key = st.text_input("🔑 OpenAI API Key", type="password", key="openai_api_key")

if key and not st.session_state.api_key_valid:
    try:
        OpenAIEmbeddings(openai_api_key=key).embed_query("ping")
        st.session_state.api_key_valid = True
        st.success("API key válida ✅")
    except Exception:
        st.session_state.api_key_valid = False
        st.error("Chave inválida ou sem acesso aos modelos ❌")


# Pequeno adaptador p/ Chroma -------------------------------------------------
class ChromaEmbeddingFunction:
    def __init__(self, embedder: OpenAIEmbeddings):
        self._emb = embedder

    def __call__(self, texts: Sequence[str]):
        return self._emb.embed_documents(list(texts))

    def embed_query(self, text: str):
        return self._emb.embed_query(text)

    embed_documents = __call__


uploaded = st.file_uploader("📄 Envie um PDF", type=["pdf"])

if uploaded:
    if not st.session_state.api_key_valid:
        st.warning("Insira a chave API antes de prosseguir.")
        st.stop()

    # DB fresco a cada upload
    shutil.rmtree("chroma_db", ignore_errors=True)
    os.makedirs("chroma_db", exist_ok=True)

    with st.spinner("Ingerindo PDF …"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded.getbuffer())
            pdf_path = tmp.name

        docs = PyPDFLoader(pdf_path).load()

        embedder = OpenAIEmbeddings(openai_api_key=key)
        client_settings = Settings(                 # ← FIX principal
            chroma_db_impl="duckdb+parquet",
            persist_directory="chroma_db",
        )

        chroma_vec = Chroma.from_documents(
            docs,
            embedding=ChromaEmbeddingFunction(embedder),
            client_settings=client_settings,
            collection_name="pdf_collection",
        )

    st.success("PDF ingerido com sucesso 🚀")

    # QA ---------------------------------------------------------------------
    qa = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(openai_api_key=key, model_name="gpt-3.5-turbo"),
        retriever=chroma_vec.as_retriever(),
    )

    q = st.text_input("❓ Sua pergunta sobre o documento:")
    if st.button("Perguntar") and q:
        with st.spinner("Consultando …"):
            ans = qa.run(q)
        st.markdown("**Resposta:**")
        st.write(ans)
