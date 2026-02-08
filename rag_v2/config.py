"""
Tazkiyah RAG v2 - Configuration

Loads settings from root-level .env file.
All settings configurable via environment variables.

Key difference from v1: Uses translation_clean + commentary_clean as primary
RAG content. No footnotes/annotated fields.
"""
import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from project root (parent of rag_v2/)
_PROJECT_ROOT = Path(__file__).parent.parent
load_dotenv(_PROJECT_ROOT / ".env")

# =============================================================================
# LangSmith Tracing
# =============================================================================
# These env vars are read automatically by LangChain/LangSmith SDK
# We just ensure they're set from .env
LANGSMITH_TRACING = os.getenv("LANGSMITH_TRACING", "false")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY", "")
LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT", "tazkiyah-rag-v2")
LANGSMITH_ENDPOINT = os.getenv("LANGSMITH_ENDPOINT", "https://api.smith.langchain.com")

# Propagate to env so LangChain SDK picks them up automatically
os.environ["LANGSMITH_TRACING"] = LANGSMITH_TRACING
if LANGSMITH_API_KEY:
    os.environ["LANGSMITH_API_KEY"] = LANGSMITH_API_KEY
os.environ["LANGSMITH_PROJECT"] = LANGSMITH_PROJECT
os.environ["LANGSMITH_ENDPOINT"] = LANGSMITH_ENDPOINT

# =============================================================================
# Model Configuration (switchable via .env)
# =============================================================================
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text-v2-moe")
LLM_MODEL = os.getenv("LLM_MODEL", "gemma3:4b")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Embedding prefixes (for nomic-embed-text-v2-moe)
EMBED_QUERY_PREFIX = os.getenv("EMBED_QUERY_PREFIX", "search_query: ")
EMBED_DOCUMENT_PREFIX = os.getenv("EMBED_DOCUMENT_PREFIX", "search_document: ")

# =============================================================================
# Vector Store
# =============================================================================
CHROMA_PERSIST_DIR = Path(os.getenv(
    "CHROMA_PERSIST_DIR",
    str(Path(__file__).parent / "chroma_db_v2")
))
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "quran_tazkiyah_v2")

# =============================================================================
# Retrieval
# =============================================================================
TOP_K = int(os.getenv("TOP_K", "5"))
SEARCH_TYPE = os.getenv("SEARCH_TYPE", "similarity")  # "similarity" or "mmr"
MMR_LAMBDA = float(os.getenv("MMR_LAMBDA", "0.5"))
MIN_RELEVANCE_SCORE = float(os.getenv("MIN_RELEVANCE_SCORE", "0.0"))

# =============================================================================
# LLM Generation
# =============================================================================
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.3"))
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "1024"))
LLM_TOP_P = float(os.getenv("LLM_TOP_P", "0.9"))
LLM_REPEAT_PENALTY = float(os.getenv("LLM_REPEAT_PENALTY", "1.1"))

# =============================================================================
# Prompt Templates
# =============================================================================
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", """You are Tazkiyah, an Islamic knowledge assistant specializing in Quranic understanding.
You help users understand the Quran through verses, translations, and scholarly tafsir (commentary) by Maududi.

When answering questions:
1. Base your answers ONLY on the provided context from the Quran and tafsir
2. Reference specific verse numbers (e.g., 2:255) when citing
3. Explain the meaning using the tafsir/commentary provided
4. Be respectful and scholarly in your tone
5. If the context doesn't contain relevant information, say so honestly
6. Do not fabricate or invent any Quranic content""")

RAG_PROMPT_TEMPLATE = os.getenv("RAG_PROMPT_TEMPLATE", """Use the following context from the Quran (translation and commentary by Maududi) to answer the question.

Context:
{context}

Question: {question}

Provide a thorough answer based on the context. Cite verse references where applicable. If the context doesn't contain relevant information, acknowledge this.""")

# =============================================================================
# Data Source
# =============================================================================
DATA_FILE = Path(os.getenv(
    "RAG_DATA_FILE",
    str(_PROJECT_ROOT / "quran_full_rag_v2.json")
))

# =============================================================================
# Logging
# =============================================================================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# =============================================================================
# UI
# =============================================================================
UI_SERVER_HOST = os.getenv("UI_SERVER_HOST", "127.0.0.1")
UI_SERVER_PORT = int(os.getenv("UI_SERVER_PORT", "7861"))
UI_SHARE = os.getenv("UI_SHARE", "false").lower() == "true"
SHOW_SOURCES = os.getenv("SHOW_SOURCES", "true").lower() == "true"
MAX_SOURCES_DISPLAY = int(os.getenv("MAX_SOURCES_DISPLAY", "5"))

# =============================================================================
# Performance
# =============================================================================
EMBEDDING_BATCH_SIZE = int(os.getenv("EMBEDDING_BATCH_SIZE", "32"))
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "120"))
