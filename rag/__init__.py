"""
Tazkiyah RAG Package

Quranic knowledge retrieval pipeline using:
- LangChain + langchain-ollama + langchain-chroma
- Ollama embeddings (nomic-embed-text-v2-moe)
- Ollama LLM (gemma3:4b)
- ChromaDB vector store
- Gradio 6.0 web UI
"""
from rag.rag_pipeline import TazkiyahRAG, create_documents_from_chunks

__all__ = [
    "TazkiyahRAG",
    "create_documents_from_chunks",
]
