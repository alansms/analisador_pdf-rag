from langchain_core.documents import Document as BaseDocument

class Document(BaseDocument):
    """Classe documento personalizada que estende o Document do LangChain"""
    def __init__(self, page_content: str, metadata: dict = None):
        super().__init__(page_content=page_content, metadata=metadata or {})