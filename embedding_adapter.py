from typing import List

class ChromaEmbeddingFunction:
    def __init__(self, embedding_function):
        self.embedding_function = embedding_function

    def __call__(self, input: str) -> List[float]:
        # Usa a função embed_query do OpenAIEmbeddings para gerar embeddings
        return self.embedding_function.embed_query(input)