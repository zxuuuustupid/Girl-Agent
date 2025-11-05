from ..rag.retriever import Retriever
from .tool_interface import ToolInterface

class RetrievalTool(ToolInterface):
    def __init__(self, doc_path="documents", db_path="faiss_index"):
        self.retriever = Retriever(doc_path, db_path).get_retriever()

    def name(self) -> str:
        return "retrieval"

    def description(self) -> str:
        return "Retrieves information from the knowledge base. Use this tool when you need to answer questions about topics you don't know."

    def run(self, query: str) -> str:
        docs = self.retriever.invoke(query)
        return "\n".join([doc.page_content for doc in docs])
