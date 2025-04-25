import os
from chromadb import PersistentClient
from chromadb.config import Settings

DB_DIR = os.path.abspath("chroma")  # Caminho do banco

# Configurar cliente do ChromaDB
def get_client():
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)
    
    settings = Settings(
        persist_directory=DB_DIR,
        allow_reset=True,
        anonymized_telemetry=False
    )
    return PersistentClient(settings=settings)