from setuptools import setup, find_packages

setup(
    name="assistente-rag-pln",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "streamlit",
        "sqlalchemy",
        "chromadb>=0.4.6",
        "hnswlib>=0.7.2",
        "langchain-community>=0.0.1",
        "langchain-openai",
        "langchain-chroma==0.2.3",
        "openai",
        "tiktoken",
        "pypdf",
        "python-dotenv",
        "watchdog",
        "pydantic-settings"
    ],
    author="Assistente RAG",
    author_email="exemplo@email.com",
    description="Assistente virtual baseado em IA utilizando a arquitetura RAG para processamento de linguagem natural",
    keywords="rag, ia, nlp, processamento de linguagem natural, chatbot",
    url="https://github.com/seu-usuario/assistente-rag-pln",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)