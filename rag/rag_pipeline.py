#!/usr/bin/env python3
"""
Tazkiyah RAG Pipeline

Modern LangChain implementation based on latest documentation:
- langchain-ollama: Embeddings and LLM
- langchain-chroma: Vector store with persistence
- langchain-core: Prompts, documents, runnables
"""
import logging
from pathlib import Path
from typing import Optional
from uuid import uuid4

from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser

from rag import config

# Setup logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format=config.LOG_FORMAT
)
logger = logging.getLogger(__name__)


class TazkiyahRAG:
    """
    RAG Pipeline for Quranic knowledge retrieval.
    
    Based on LangChain latest patterns from Context7 documentation.
    """
    
    def __init__(
        self,
        embedding_model: str = config.EMBEDDING_MODEL,
        llm_model: str = config.LLM_MODEL,
        collection_name: str = config.COLLECTION_NAME,
        persist_directory: Optional[Path] = None,
    ):
        self.embedding_model = embedding_model
        self.llm_model = llm_model
        self.collection_name = collection_name
        self.persist_directory = persist_directory or config.CHROMA_PERSIST_DIR
        
        self._embeddings: Optional[OllamaEmbeddings] = None
        self._llm: Optional[OllamaLLM] = None
        self._vectorstore: Optional[Chroma] = None
        
        logger.info(f"TazkiyahRAG initialized: embedding={embedding_model}, llm={llm_model}")
    
    def _needs_prefix(self) -> bool:
        """Check if embedding model requires prefixes."""
        return "v2-moe" in self.embedding_model
    
    def _add_query_prefix(self, query: str) -> str:
        """Add query prefix for nomic-embed-text-v2-moe."""
        if self._needs_prefix() and not query.startswith(config.EMBED_QUERY_PREFIX):
            return f"{config.EMBED_QUERY_PREFIX}{query}"
        return query
    
    def _add_document_prefix(self, text: str) -> str:
        """Add document prefix for nomic-embed-text-v2-moe."""
        if self._needs_prefix() and not text.startswith(config.EMBED_DOCUMENT_PREFIX):
            return f"{config.EMBED_DOCUMENT_PREFIX}{text}"
        return text
    
    @property
    def embeddings(self) -> OllamaEmbeddings:
        """Lazy-load Ollama embeddings (from langchain-ollama)."""
        if self._embeddings is None:
            logger.info(f"Loading embeddings: {self.embedding_model}")
            self._embeddings = OllamaEmbeddings(
                model=self.embedding_model,
                base_url=config.OLLAMA_BASE_URL,
            )
        return self._embeddings
    
    @property
    def llm(self) -> OllamaLLM:
        """Lazy-load Ollama LLM (from langchain-ollama)."""
        if self._llm is None:
            logger.info(f"Loading LLM: {self.llm_model}")
            self._llm = OllamaLLM(
                model=self.llm_model,
                base_url=config.OLLAMA_BASE_URL,
                temperature=config.LLM_TEMPERATURE,
                num_predict=config.LLM_MAX_TOKENS,
                top_p=config.LLM_TOP_P,
                repeat_penalty=config.LLM_REPEAT_PENALTY,
            )
        return self._llm
    
    @property
    def vectorstore(self) -> Chroma:
        """Lazy-load ChromaDB vector store (from langchain-chroma)."""
        if self._vectorstore is None:
            persist_dir = str(self.persist_directory)
            logger.info(f"Initializing vector store: {persist_dir}")
            
            # From Context7: langchain-chroma initialization
            self._vectorstore = Chroma(
                collection_name=self.collection_name,
                embedding_function=self.embeddings,
                persist_directory=persist_dir,
            )
        return self._vectorstore
    
    def add_documents(self, documents: list[Document]) -> list[str]:
        """
        Add documents to vector store.
        
        From Context7: Use uuid4 for document IDs, add_documents with ids parameter.
        """
        total = len(documents)
        logger.info(f"Adding {total} documents to vector store")
        
        # Add document prefix if needed for nomic-embed-text-v2-moe
        if self._needs_prefix():
            for doc in documents:
                doc.page_content = self._add_document_prefix(doc.page_content)
        
        # From Context7: Generate UUIDs for documents
        uuids = [str(uuid4()) for _ in range(total)]
        
        # From Context7: add_documents with ids
        ids = self.vectorstore.add_documents(documents=documents, ids=uuids)
        logger.info(f"Added {len(ids)} documents")
        
        return ids
    
    def similarity_search(self, query: str, k: int = config.TOP_K) -> list[Document]:
        """
        Perform similarity search.
        
        From Context7: similarity_search with query string and k parameter.
        """
        prefixed_query = self._add_query_prefix(query)
        logger.info(f"Similarity search: '{query[:50]}...' (k={k})")
        
        results = self.vectorstore.similarity_search(prefixed_query, k=k)
        logger.info(f"Found {len(results)} results")
        
        return results
    
    def similarity_search_with_score(self, query: str, k: int = config.TOP_K) -> list[tuple[Document, float]]:
        """
        Similarity search with scores.
        
        From Context7: similarity_search_with_score returns (doc, score) tuples.
        """
        prefixed_query = self._add_query_prefix(query)
        logger.info(f"Similarity search with score: '{query[:50]}...'")
        
        return self.vectorstore.similarity_search_with_score(prefixed_query, k=k)
    
    def query(self, question: str, return_sources: bool = True, debug_callback=None) -> dict:
        """
        Query the RAG pipeline.
        
        Args:
            question: The user's question
            return_sources: Whether to return source documents
            debug_callback: Optional function to receive debug info at each step
        
        From Context7: Use ChatPromptTemplate, chain with | operator, StrOutputParser.
        """
        def log_step(step: str, data: str):
            logger.info(f"[{step}] {data[:200]}...")
            if debug_callback:
                debug_callback(step, data)
        
        log_step("QUERY", f"User question: {question}")
        
        # Step 1: Retrieve relevant documents with scores
        log_step("RETRIEVAL", f"Searching for top {config.TOP_K} similar documents...")
        results_with_scores = self.similarity_search_with_score(question, k=config.TOP_K)
        
        source_docs = [doc for doc, score in results_with_scores]
        
        # Log each retrieved document
        retrieval_details = []
        for i, (doc, score) in enumerate(results_with_scores, 1):
            meta = doc.metadata
            verse_key = meta.get("verse_key", "?")
            surah = meta.get("surah_name", "")
            snippet = doc.page_content[:150].replace("\n", " ")
            detail = f"  [{i}] Score: {score:.4f} | Verse {verse_key} ({surah})\n      {snippet}..."
            retrieval_details.append(detail)
        
        log_step("RETRIEVED_DOCS", f"Found {len(source_docs)} documents:\n" + "\n".join(retrieval_details))
        
        # Step 2: Format context
        context = "\n\n".join(doc.page_content for doc in source_docs)
        log_step("CONTEXT", f"Built context ({len(context)} chars):\n{context[:500]}...")
        
        # Step 3: Create prompt (from Context7 LangChain patterns)
        prompt = ChatPromptTemplate.from_template(config.RAG_PROMPT_TEMPLATE)
        
        # Step 4: Format the full prompt for logging
        full_prompt = config.RAG_PROMPT_TEMPLATE.format(context=context, question=question)
        log_step("FULL_PROMPT", f"Prompt to LLM ({len(full_prompt)} chars):\n{full_prompt}")
        
        # Step 5: Build chain with | operator (from Context7)
        chain = prompt | self.llm | StrOutputParser()
        
        # Step 6: Invoke chain
        log_step("LLM_CALL", f"Invoking {self.llm_model}...")
        result = chain.invoke({"context": context, "question": question})
        log_step("LLM_RESPONSE", f"Response ({len(result)} chars):\n{result}")
        
        response: dict = {"result": result}
        if return_sources:
            response["source_documents"] = source_docs  # type: ignore
            response["scores"] = [score for _, score in results_with_scores]
        
        return response
    
    def get_collection_stats(self) -> dict:
        """Get vector store statistics."""
        collection = self.vectorstore._collection
        return {
            "name": self.collection_name,
            "count": collection.count(),
            "persist_directory": str(self.persist_directory),
        }
    
    def clear_collection(self):
        """Delete all documents from the collection."""
        logger.warning("Clearing vector store collection")
        collection = self.vectorstore._collection
        all_ids = collection.get()["ids"]
        if all_ids:
            collection.delete(ids=all_ids)
        logger.info(f"Deleted {len(all_ids)} documents")


def create_documents_from_chunks(chunks: list[dict]) -> list[Document]:
    """
    Convert chunk dictionaries to LangChain Documents.
    
    From Context7: Document(page_content=..., metadata=...)
    """
    documents = []
    
    for chunk in chunks:
        content = chunk.get("text", "")
        metadata = chunk.get("metadata", {}).copy()
        
        # Add extra fields to metadata
        if "id" in chunk:
            metadata["verse_id"] = chunk["id"]
        if "arabic_text" in chunk:
            metadata["arabic_text"] = chunk["arabic_text"]
        if "surah_name" in chunk:
            metadata["surah_name"] = chunk["surah_name"]
        
        documents.append(Document(
            page_content=content,
            metadata=metadata,
        ))
    
    return documents
