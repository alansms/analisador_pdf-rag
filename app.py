import streamlit as st
from typing import List
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
import tempfile
import os

if 'api_key_valid' not in st.session_state:
    st.session_state.api_key_valid = False

if 'openai_api_key' not in st.session_state:
    st.session_state.openai_api_key = ""

openai_api_key = st.text_input("OpenAI API Key", type="password", key="openai_api_key")

if st.session_state.openai_api_key and not st.session_state.api_key_valid:
    try:
        OpenAIEmbeddings(openai_api_key=st.session_state.openai_api_key).embed_query("test")
        st.success("API key válida! ✅")
        st.session_state.api_key_valid = True
    except Exception:
        st.error("Chave inválida ou sem acesso ao modelo. ❌")
        st.session_state.api_key_valid = False

class ChromaEmbeddingFunction:
    def __init__(self, embedding_function):
        self.embedding_function = embedding_function

    def __call__(self, texts: List[str]) -> List[List[float]]:
        if isinstance(texts, str):
            texts = [texts]
        return self.embedding_function.embed_documents(list(texts))

    def embed_query(self, text: str) -> List[float]:
        return self.embedding_function.embed_query(text)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self.__call__(texts)

st.title("Assistente de análise de documentos PDF")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file:
    if st.session_state.openai_api_key and st.session_state.api_key_valid:
        with st.spinner("Ingerindo PDF..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.getbuffer())
                tmp_path = tmp_file.name

            loader = PyPDFLoader(tmp_path)
            docs = loader.load()

            openai_embeddings = OpenAIEmbeddings(openai_api_key=st.session_state.openai_api_key)
            chroma_func = ChromaEmbeddingFunction(openai_embeddings)

            vectordb = Chroma.from_documents(
                docs,
                embedding=chroma_func
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
        st.warning("Por favor, insira uma chave válida da OpenAI.")
