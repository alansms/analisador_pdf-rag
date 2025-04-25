
import sys, os, shutil, tempfile, types

# ---- 1 · SQLite >= 3.35 exigido pelo Chroma ---------------------------------
import pysqlite3                                        # noqa: E402
sys.modules["sqlite3"] = pysqlite3                      # monkey-patch
# -----------------------------------------------------------------------------


# ---- 2 · hnswlib stub/patch --------------------------------------------------
try:
    import hnswlib                                      # noqa: E402

    # algumas builds tinham apenas método; Chroma espera inteiro
    if not hasattr(hnswlib.Index, "file_handle_count"):
        hnswlib.Index.file_handle_count = 0
except ModuleNotFoundError:
    hnswlib = types.SimpleNamespace(
        Index=type("Index", (), {"file_handle_count": 0})
    )
# -----------------------------------------------------------------------------


# ---- 3 · restante do app -----------------------------------------------------
import streamlit as st                                 # noqa: E402
from typing import List, Sequence                      # noqa: E402
from langchain.document_loaders import PyPDFLoader     # noqa: E402
from langchain.embeddings import OpenAIEmbeddings      # noqa: E402
from langchain.vectorstores import Chroma              # noqa: E402
from langchain.chains import RetrievalQA               # noqa: E402
from langchain.chat_models import ChatOpenAI           # noqa: E402


# ---------- Estado ----------------------------------------------------------------
if "api_key_valid" not in st.session_state:
    st.session_state.api_key_valid = False
if "openai_api_key" not in st.session_state:
    st.session_state.openai_api_key = ""


# ---------- Header -----------------------------------------------------------------
st.title("Assistente de Análise de PDFs 📑")


# ---------- API key ---------------------------------------------------------------
key = st.text_input("🔑 OpenAI API Key", type="password", key="openai_api_key")

if key and not st.session_state.api_key_valid:
    try:
        OpenAIEmbeddings(openai_api_key=key).embed_query("ping")
        st.session_state.api_key_valid = True
        st.success("API key válida! ✅")
    except Exception:
        st.session_state.api_key_valid = False
        st.error("Chave inválida ou sem acesso aos modelos. ❌")


# ---------- Adapter ­para Chroma ---------------------------------------------------
class ChromaEmbeddingFunction:
    """Adapta `OpenAIEmbeddings` à interface esperada pelo Chroma."""

    def __init__(self, embedder: OpenAIEmbeddings):
        self._emb = embedder

    # usado em ingestão
    def __call__(self, texts: Sequence[str]):
        return self._emb.embed_documents(list(texts))

    # usado em busca
    def embed_query(self, text: str):
        return self._emb.embed_query(text)

    embed_documents = __call__


# ---------- Upload / ingestão ------------------------------------------------------
uploaded = st.file_uploader("📄 Envie um PDF", type=["pdf"])

if uploaded:
    if not st.session_state.api_key_valid:
        st.warning("Insira uma chave API para continuar.")
        st.stop()

    shutil.rmtree("chroma_db", ignore_errors=True)
    os.makedirs("chroma_db", exist_ok=True)

    with st.spinner("Ingerindo PDF …"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded.getbuffer())
            path = tmp.name

        docs = PyPDFLoader(path).load()

        embedder = OpenAIEmbeddings(openai_api_key=key)
        vectordb = Chroma.from_documents(
            docs,
            embedding=ChromaEmbeddingFunction(embedder),
            persist_directory="chroma_db",
            collection_name="pdf_collection",
        )

    st.success("PDF ingerido com sucesso! 🚀")

    # ---------- QA ­-------------------------------------------------------------
    qa_chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(openai_api_key=key, model_name="gpt-3.5-turbo"),
        retriever=vectordb.as_retriever(),
    )

    question = st.text_input("❓ Sua pergunta sobre o documento:")
    if st.button("Perguntar") and question:
        with st.spinner("Consultando …"):
            answer = qa_chain.run(question)
        st.markdown("**Resposta:**")
        st.write(answer)
