
import os
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter

class DataSource:
    def __init__(self, path):
        self.path = path
        self.documents = []

    def load_documents(self):
        for file in os.listdir(self.path):
            if file.endswith(".txt"):
                loader = TextLoader(os.path.join(self.path, file), encoding='utf-8')
                self.documents.extend(loader.load())
        return self.documents

    def split_documents(self, chunk_size=1000, chunk_overlap=0):
        text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        return text_splitter.split_documents(self.documents)
