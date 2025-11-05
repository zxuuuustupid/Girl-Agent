
from .datasource import DataSource
from .vector_store import VectorStore

class Retriever:
    def __init__(self, doc_path, db_path="faiss_index"):
        self.doc_path = doc_path
        self.db_path = db_path
        self.vector_store = VectorStore(db_path)

    def get_retriever(self):
        retriever = self.vector_store.as_retriever()
        if retriever is None:
            print("Building vector store...")
            data_source = DataSource(self.doc_path)
            documents = data_source.load_documents()
            split_docs = data_source.split_documents()
            self.vector_store.build(split_docs)
            retriever = self.vector_store.as_retriever()
        return retriever
