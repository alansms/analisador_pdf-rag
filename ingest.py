# --- Compatibilidade hnswlib / Chroma ---------------------------------------
import hnswlib
if hasattr(hnswlib, "Index") and not hasattr(hnswlib.Index, "file_handle_count"):
    hnswlib.Index.file_handle_count = 0  # fallback seguro para evitar AttributeError
# ---------------------------------------------------------------------------
from chromadb import PersistentClient
from chromadb.config import Settings
import os
import shutil
import chromadb.errors as chroma_errors

DB_DIR = os.path.abspath("chroma")  # Refira o diretório correto.

def get_clean_client() -> PersistentClient:
    """Cria um client ChromaDB sempre em um diretório limpo."""
    if os.path.isdir(DB_DIR):
        shutil.rmtree(DB_DIR, ignore_errors=True)
    os.makedirs(DB_DIR, exist_ok=True)
    return PersistentClient(settings=Settings(
        persist_directory=DB_DIR,
        anonymized_telemetry=False
    ))

# Instancia o client sempre limpo
client = get_clean_client()

def get_collection_safely(name: str):
    """Obtém ou cria coleção; em caso de qualquer falha, reinicializa tudo."""
    try:
        return client.get_or_create_collection(name=name)
    except chroma_errors.ChromaError:
        global client
        client = get_clean_client()
        return client.get_or_create_collection(name=name)

collection = get_collection_safely("document_collection")