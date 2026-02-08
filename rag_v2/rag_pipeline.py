#!/usr/bin/env python3
"""
Tazkiyah RAG v2 - Pipeline

LangChain + Ollama + ChromaDB + LangSmith

Key differences from v1:
  - Loads directly from quran_full_rag_v2.json (no JSONL chunk preprocessing)
  - Uses translation_clean + commentary_clean as searchable content
  - LangSmith tracing enabled via env vars
  - Model/embedding switchable from .env
  - Uses ChatOllama (chat model) instead of OllamaLLM
"""
import logging
from pathlib import Path
from typing import Optional
from uuid import uuid4

from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from rag_v2 import config

# Setup logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format=config.LOG_FORMAT,
)
logger = logging.getLogger(__name__)


class TazkiyahRAGv2:
    """
    RAG v2 Pipeline for Quranic knowledge retrieval.

    - translation_clean + commentary_clean are the indexed content
    - LangSmith tracing is automatic (configured via env vars in config.py)
    - Models switchable via .env
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
        self._llm: Optional[ChatOllama] = None
        self._vectorstore: Optional[Chroma] = None

        logger.info(
            f"TazkiyahRAGv2 initialized: embedding={embedding_model}, "
            f"llm={llm_model}, collection={collection_name}"
        )

        # Log LangSmith status
        if config.LANGSMITH_TRACING.lower() == "true" and config.LANGSMITH_API_KEY:
            logger.info(
                f"LangSmith tracing ENABLED -> project: {config.LANGSMITH_PROJECT}"
            )
        else:
            logger.info("LangSmith tracing DISABLED (set LANGSMITH_TRACING=true and LANGSMITH_API_KEY)")

    # ─── Embedding prefix helpers ─────────────────────────────────────────

    def _needs_prefix(self) -> bool:
        """Check if embedding model requires prefixes (nomic-embed-text-v2-moe)."""
        return "v2-moe" in self.embedding_model

    def _add_query_prefix(self, query: str) -> str:
        if self._needs_prefix() and not query.startswith(config.EMBED_QUERY_PREFIX):
            return f"{config.EMBED_QUERY_PREFIX}{query}"
        return query

    def _add_document_prefix(self, text: str) -> str:
        if self._needs_prefix() and not text.startswith(config.EMBED_DOCUMENT_PREFIX):
            return f"{config.EMBED_DOCUMENT_PREFIX}{text}"
        return text

    # ─── Lazy-loaded components ───────────────────────────────────────────

    @property
    def embeddings(self) -> OllamaEmbeddings:
        """Lazy-load Ollama embeddings."""
        if self._embeddings is None:
            logger.info(f"Loading embeddings: {self.embedding_model}")
            self._embeddings = OllamaEmbeddings(
                model=self.embedding_model,
                base_url=config.OLLAMA_BASE_URL,
            )
        return self._embeddings

    @property
    def llm(self) -> ChatOllama:
        """Lazy-load ChatOllama (chat model for better prompt handling)."""
        if self._llm is None:
            logger.info(f"Loading ChatOllama: {self.llm_model}")
            self._llm = ChatOllama(
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
        """Lazy-load ChromaDB vector store."""
        if self._vectorstore is None:
            persist_dir = str(self.persist_directory)
            logger.info(f"Initializing ChromaDB: {persist_dir}")
            self._vectorstore = Chroma(
                collection_name=self.collection_name,
                embedding_function=self.embeddings,
                persist_directory=persist_dir,
            )
        return self._vectorstore

    # ─── Document management ──────────────────────────────────────────────

    def add_documents(self, documents: list[Document]) -> list[str]:
        """Add documents to vector store with UUID ids."""
        total = len(documents)
        logger.info(f"Adding {total} documents to vector store")

        # Add document prefix for nomic-embed-text-v2-moe
        if self._needs_prefix():
            for doc in documents:
                doc.page_content = self._add_document_prefix(doc.page_content)

        uuids = [str(uuid4()) for _ in range(total)]
        ids = self.vectorstore.add_documents(documents=documents, ids=uuids)
        logger.info(f"Successfully added {len(ids)} documents")
        return ids

    def clear_collection(self):
        """Delete all documents from the collection."""
        logger.warning("Clearing vector store collection")
        collection = self.vectorstore._collection
        all_ids = collection.get()["ids"]
        if all_ids:
            collection.delete(ids=all_ids)
        logger.info(f"Deleted {len(all_ids)} documents")

    def get_collection_stats(self) -> dict:
        """Get vector store statistics."""
        collection = self.vectorstore._collection
        return {
            "name": self.collection_name,
            "count": collection.count(),
            "persist_directory": str(self.persist_directory),
            "embedding_model": self.embedding_model,
            "llm_model": self.llm_model,
        }

    # ─── Search ───────────────────────────────────────────────────────────

    def similarity_search(self, query: str, k: int = config.TOP_K) -> list[Document]:
        """Perform similarity search."""
        prefixed_query = self._add_query_prefix(query)
        logger.info(f"Similarity search: '{query[:60]}...' (k={k})")
        results = self.vectorstore.similarity_search(prefixed_query, k=k)
        logger.info(f"Found {len(results)} results")
        return results

    def similarity_search_with_score(
        self, query: str, k: int = config.TOP_K
    ) -> list[tuple[Document, float]]:
        """Similarity search with relevance scores."""
        prefixed_query = self._add_query_prefix(query)
        return self.vectorstore.similarity_search_with_score(prefixed_query, k=k)

    # ─── RAG Query ────────────────────────────────────────────────────────

    def query(
        self,
        question: str,
        return_sources: bool = True,
        debug_callback=None,
    ) -> dict:
        """
        Query the RAG v2 pipeline.

        All calls are traced by LangSmith automatically when configured.

        Args:
            question: User's question about the Quran
            return_sources: Whether to include source documents in result
            debug_callback: Optional fn(step, data) for debug logging

        Returns:
            {"result": str, "source_documents": list[Doc], "scores": list[float]}
        """
        def log_step(step: str, data: str):
            logger.info(f"[{step}] {data[:200]}")
            if debug_callback:
                debug_callback(step, data)

        log_step("QUERY", f"User question: {question}")

        # Step 1: Retrieve relevant documents with scores
        log_step("RETRIEVAL", f"Searching top {config.TOP_K} documents...")
        results_with_scores = self.similarity_search_with_score(
            question, k=config.TOP_K
        )
        source_docs = [doc for doc, score in results_with_scores]

        # Log retrieval details
        retrieval_details = []
        for i, (doc, score) in enumerate(results_with_scores, 1):
            meta = doc.metadata
            verse_key = meta.get("verse_key", "?")
            surah = meta.get("surah_name", "")
            snippet = doc.page_content[:120].replace("\n", " ")
            retrieval_details.append(
                f"  [{i}] Score: {score:.4f} | {verse_key} ({surah}) | {snippet}..."
            )
        log_step(
            "RETRIEVED_DOCS",
            f"Found {len(source_docs)} docs:\n" + "\n".join(retrieval_details),
        )

        # Step 2: Build context
        context = "\n\n---\n\n".join(doc.page_content for doc in source_docs)
        log_step("CONTEXT", f"Context ({len(context)} chars)")

        # Step 3: Create prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", config.SYSTEM_PROMPT),
            ("human", config.RAG_PROMPT_TEMPLATE),
        ])

        # Step 4: Build and invoke chain (LangSmith traces this automatically)
        chain = prompt | self.llm | StrOutputParser()

        log_step("LLM_CALL", f"Invoking {self.llm_model}...")
        result = chain.invoke({"context": context, "question": question})
        log_step("LLM_RESPONSE", f"Response ({len(result)} chars)")

        response: dict = {"result": result}
        if return_sources:
            response["source_documents"] = source_docs
            response["scores"] = [score for _, score in results_with_scores]

        return response

    def get_retriever(self, k: int = config.TOP_K):
        """Get a LangChain retriever for advanced chain composition."""
        search_kwargs = {"k": k}
        if config.SEARCH_TYPE == "mmr":
            return self.vectorstore.as_retriever(
                search_type="mmr",
                search_kwargs={**search_kwargs, "lambda_mult": config.MMR_LAMBDA},
            )
        return self.vectorstore.as_retriever(search_kwargs=search_kwargs)
