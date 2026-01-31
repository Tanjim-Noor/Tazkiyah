"""
Tazkiyah RAG Pipeline Configuration

🎛️ CUSTOMIZE YOUR RAG PIPELINE HERE

Optimized for RTX 3080 10GB VRAM
All settings can be overridden via environment variables.
"""
from pathlib import Path
import os

# =============================================================================
# 🧠 MODEL CONFIGURATION
# =============================================================================

# Embedding Model (via Ollama)
# Options:
#   - "nomic-embed-text-v2-moe" (305M active, 958MB, 768 dims) - BEST for multilingual/Arabic
#   - "nomic-embed-text"        (137M params, 274MB, 768 dims) - Fast, English-focused
#   - "mxbai-embed-large"       (334M params, 670MB, 1024 dims) - Balanced
#   - "bge-m3"                  (567M params, 1.2GB, 1024 dims) - High accuracy
#   - "all-minilm"              (23M params, 46MB, 384 dims) - Tiny, fast
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text-v2-moe")

# Embedding prefixes (required for nomic-embed-text-v2-moe)
# Set to empty strings "" if using other models
EMBED_QUERY_PREFIX = os.getenv("EMBED_QUERY_PREFIX", "search_query: ")
EMBED_DOCUMENT_PREFIX = os.getenv("EMBED_DOCUMENT_PREFIX", "search_document: ")

# LLM Model (via Ollama)
# Options for RTX 3080 10GB:
#   - "qwen3:8b"        (4.9GB) - Best reasoning, recommended
#   - "llama3.1:8b"     (4.9GB) - Reliable, general purpose
#   - "mistral:7b"      (4.1GB) - Fast, good for chat
#   - "gemma3:4b"       (3.3GB) - Lightweight, fast
#   - "phi3:mini"       (2.3GB) - Very fast, good for simple Q&A
LLM_MODEL = os.getenv("LLM_MODEL", "gemma3:4b")

# Ollama server URL
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# =============================================================================
# 📦 VECTOR STORE CONFIGURATION
# =============================================================================

# Where to persist the ChromaDB database
CHROMA_PERSIST_DIR = Path(os.getenv(
    "CHROMA_PERSIST_DIR", 
    str(Path(__file__).parent / "chroma_db")
))

# Collection name in ChromaDB
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "quran_verses")

# =============================================================================
# 🔍 RETRIEVAL CONFIGURATION (MOST IMPORTANT FOR TUNING)
# =============================================================================

# Number of documents to retrieve
# Lower = faster, more focused | Higher = more context, slower
# Recommended: 3-10 depending on chunk size
TOP_K = int(os.getenv("TOP_K", "5"))

# Search type
# - "similarity": Standard cosine similarity (faster)
# - "mmr": Maximal Marginal Relevance (more diverse results, avoids redundancy)
SEARCH_TYPE = os.getenv("SEARCH_TYPE", "similarity")

# MMR settings (only used if SEARCH_TYPE = "mmr")
# lambda_mult: 0 = max diversity, 1 = max relevance
MMR_LAMBDA = float(os.getenv("MMR_LAMBDA", "0.5"))

# Minimum similarity score threshold (0.0 to 1.0)
# Documents below this score will be filtered out
# Set to 0.0 to disable filtering
MIN_RELEVANCE_SCORE = float(os.getenv("MIN_RELEVANCE_SCORE", "0.0"))

# =============================================================================
# 💬 LLM GENERATION CONFIGURATION
# =============================================================================

# Temperature: 0.0 = deterministic, 1.0+ = creative
# For factual Q&A: 0.1-0.3 | For creative: 0.7-1.0
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.3"))

# Maximum tokens in response
# Higher = longer answers but slower
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "1024"))

# Top-p (nucleus sampling): 0.1-1.0
# Lower = more focused, higher = more variety
LLM_TOP_P = float(os.getenv("LLM_TOP_P", "0.9"))

# Repeat penalty: 1.0 = no penalty, >1.0 = discourage repetition
LLM_REPEAT_PENALTY = float(os.getenv("LLM_REPEAT_PENALTY", "1.1"))

# =============================================================================
# 📝 PROMPT TEMPLATES
# =============================================================================

# System prompt for the assistant
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", """You are Tazkiyah, an Islamic knowledge assistant specializing in Quranic understanding. 
You help users understand the Quran through verses, translations, and scholarly tafsir (commentary).

When answering questions:
1. Base your answers on the provided context from the Quran and tafsir
2. Quote relevant verses in Arabic when available
3. Explain the meaning using the tafsir provided
4. Be respectful and scholarly in your tone
5. If the context doesn't contain relevant information, say so honestly""")

# RAG prompt template - {context} and {question} are replaced at runtime
RAG_PROMPT_TEMPLATE = os.getenv("RAG_PROMPT_TEMPLATE", """Use the following context from the Quran and Islamic scholarship to answer the question.

Context:
{context}

Question: {question}

Answer based on the context provided. If the context doesn't contain relevant information, acknowledge this.""")

# =============================================================================
# 📊 LOGGING CONFIGURATION
# =============================================================================

# Log level: DEBUG, INFO, WARNING, ERROR
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# =============================================================================
# ⚡ PERFORMANCE CONFIGURATION
# =============================================================================

# Batch size for embedding documents during indexing
# Higher = faster indexing but more memory
EMBEDDING_BATCH_SIZE = int(os.getenv("EMBEDDING_BATCH_SIZE", "32"))

# Maximum concurrent requests to Ollama
MAX_CONCURRENT_REQUESTS = int(os.getenv("MAX_CONCURRENT_REQUESTS", "1"))

# Request timeout in seconds
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "120"))

# =============================================================================
# 🌐 UI CONFIGURATION
# =============================================================================

# Gradio server settings
UI_SERVER_HOST = os.getenv("UI_SERVER_HOST", "127.0.0.1")
UI_SERVER_PORT = int(os.getenv("UI_SERVER_PORT", "7860"))
UI_SHARE = os.getenv("UI_SHARE", "false").lower() == "true"

# Show sources in chat response
SHOW_SOURCES = os.getenv("SHOW_SOURCES", "true").lower() == "true"
MAX_SOURCES_DISPLAY = int(os.getenv("MAX_SOURCES_DISPLAY", "5"))

# =============================================================================
# 🔧 QUICK PRESETS (uncomment to use)
# =============================================================================

# --- FAST PRESET (quick responses, less context) ---
# TOP_K = 3
# LLM_TEMPERATURE = 0.2
# LLM_MAX_TOKENS = 512

# --- THOROUGH PRESET (detailed answers, more context) ---
# TOP_K = 10
# LLM_TEMPERATURE = 0.4
# LLM_MAX_TOKENS = 2048

# --- CREATIVE PRESET (for discussion/exploration) ---
# TOP_K = 5
# LLM_TEMPERATURE = 0.7
# LLM_MAX_TOKENS = 1024
