
import os
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

class VectorStore:
    def __init__(self, db_path="faiss_index"):
        self.db_path = db_path
        self.embeddings = OpenAIEmbeddings()
        self.db = None

    def build(self, documents):
        self.db = FAISS.from_documents(documents, self.embeddings)
        self.db.save_local(self.db_path)

    def load(self):
        if os.path.exists(self.db_path):
            self.db = FAISS.load_local(self.db_path, self.embeddings, allow_dangerous_deserialization=True)
        return self.db

    def as_retriever(self):
        if not self.db:
            self.load()
        if self.db:
            return self.db.as_retriever()
        return None
