# app.py
# ──────────────────────────────────────────────────────────────────────────────
# 1. Força SQLite ≥ 3.35 (pysqlite3)                → Chroma em Streamlit Cloud
# 2. Garante hnswlib.Index.file_handle_count == int → evita TypeError
# 3. App Streamlit para perguntas sobre PDF usando LangChain + Chroma
# ──────────────────────────────────────────────────────────────────────────────

# --- 1 · SQLite ----------------------------------------------------------------
import sys
import pysqlite3                              # SQLite 3.42 incluído
sys.modules["sqlite3"] = pysqlite3            # Monkey-patch global

# --- 2 · hnswlib ----------------------------------------------------------------
import types
try:
    import hnswlib
except ModuleNotFoundError:                   # fallback mínimo se lib ausente
    hnswlib = types.ModuleType("hnswlib")
    class _DummyIndex: pass                   # noqa: E306,E302
    hnswlib.Index = _DummyIndex

# A partir daqui, seja qual for a build, garantimos inteiro
hnswlib.Index.file_handle_count = 0            # ← fix definitivo

# --- 3 · dependências principais ------------------------------------------------
import os, shutil, tempfile
from typing import List, Sequence

import streamlit as st
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI


# ---------- Estado da sessão ----------------------------------------------------
if "api_key_valid" not in st.session_state:
    st.session_state.api_key_valid = False
if "openai_api_key" not in st.session_state:
    st.session_state.openai_api_key = ""


# ---------- Cabeçalho -----------------------------------------------------------
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


# ---------- Adaptador p/ Chroma --------------------------------------------------
class ChromaEmbeddingFunction:
    """Adapta `OpenAIEmbeddings` à interface esperada pelo Chroma."""

    def __init__(self, embedder: OpenAIEmbeddings):
        self._emb = embedder

    def __call__(self, texts: Sequence[str]):
        return self._emb.embed_documents(list(texts))

    def embed_query(self, text: str):
        return self._emb.embed_query(text)

    embed_documents = __call__


# ---------- Upload / ingestão ----------------------------------------------------
uploaded = st.file_uploader("📄 Envie um PDF", type=["pdf"])

if uploaded:
    if not st.session_state.api_key_valid:
        st.warning("Insira uma chave API para continuar.")
        st.stop()

    # DB fresco a cada upload
    shutil.rmtree("chroma_db", ignore_errors=True)
    os.makedirs("chroma_db", exist_ok=True)

    with st.spinner("Ingerindo PDF …"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded.getbuffer())
            path = tmp.name

        docs = PyPDFLoader(path).load()

        embedder   = OpenAIEmbeddings(openai_api_key=key)
        chroma_vec = Chroma.from_documents(
            docs,
            embedding=ChromaEmbeddingFunction(embedder),
            persist_directory="chroma_db",
            collection_name="pdf_collection",
        )

    st.success("PDF ingerido com sucesso 🚀")

    # ---------- QA ----------------------------------------------------------------
    qa_chain = RetrievalQA.from_chain_type(
        llm       = ChatOpenAI(openai_api_key=key, model_name="gpt-3.5-turbo"),
        retriever = chroma_vec.as_retriever(),
    )

    q = st.text_input("❓ Sua pergunta sobre o documento:")
    if st.button("Perguntar") and q:
        with st.spinner("Consultando …"):
            ans = qa_chain.run(q)
        st.markdown("**Resposta:**")
        st.write(ans)
