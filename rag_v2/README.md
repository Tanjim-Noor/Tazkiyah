# Tazkiyah RAG v2

**LangChain + Ollama + ChromaDB + LangSmith**

Second-generation RAG pipeline for Quranic knowledge retrieval, built on `quran_full_rag_v2.json`.

## Key Differences from v1

| Feature | v1 (rag/) | v2 (rag_v2/) |
|---------|-----------|--------------|
| Data source | Pre-processed JSONL chunks | Direct from `quran_full_rag_v2.json` |
| Indexed content | Custom chunk text | `translation_clean` + `commentary_clean` |
| Excluded fields | — | footnotes, annotated versions, has_* flags |
| LLM interface | `OllamaLLM` | `ChatOllama` (chat model) |
| Tracing | None | LangSmith integration |
| Config | Hardcoded + env | `.env` file with `python-dotenv` |

## Setup

### 1. Create & activate virtual environment

```bash
# From project root
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

Edit the root `.env` file — the RAG v2 section has all settings:

```dotenv
# Key settings to configure:
LLM_MODEL=gemma3:4b                      # Switch to any Ollama model
EMBEDDING_MODEL=nomic-embed-text-v2-moe   # Switch embedding model
LANGSMITH_API_KEY=your-key-here            # Get from smith.langchain.com
LANGSMITH_TRACING=true                     # Enable/disable tracing
```

### 4. Ensure Ollama is running with required models

```bash
ollama pull gemma3:4b
ollama pull nomic-embed-text-v2-moe
```

## Usage

### Index the Quran data

```bash
python -m rag_v2.index_data                # Index with defaults
python -m rag_v2.index_data --clear         # Clear and re-index
python -m rag_v2.index_data --no-commentary # Index only translations
```

### Query from CLI

```bash
python -m rag_v2.query_rag "What is the meaning of Bismillah?"
python -m rag_v2.query_rag --top-k 10 "What does the Quran say about patience?"
```

### Interactive terminal chat

```bash
python -m rag_v2.chat
```

### Web UI (Gradio)

```bash
python -m rag_v2.chat_ui
# Opens at http://127.0.0.1:7861
```

## Architecture

```
quran_full_rag_v2.json
        │
        ▼
   data_loader.py          ← Loads JSON, creates LangChain Documents
        │                     page_content = translation_clean + commentary_clean
        │                     metadata = surah/verse identifiers
        ▼
   rag_pipeline.py         ← TazkiyahRAGv2 class
        │                     OllamaEmbeddings → ChromaDB → ChatOllama
        │                     LangSmith traces all calls automatically
        ▼
   index_data.py           ← CLI to index documents
   query_rag.py            ← CLI single query
   chat.py                 ← Terminal REPL chat
   chat_ui.py              ← Gradio web interface
```

## LangSmith Integration

When `LANGSMITH_TRACING=true` and `LANGSMITH_API_KEY` is set:
- All LLM calls are traced automatically
- Retrieval steps are logged
- View traces at https://smith.langchain.com

## Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_MODEL` | `gemma3:4b` | Ollama chat model |
| `EMBEDDING_MODEL` | `nomic-embed-text-v2-moe` | Ollama embedding model |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama server URL |
| `LANGSMITH_TRACING` | `true` | Enable LangSmith tracing |
| `LANGSMITH_API_KEY` | — | LangSmith API key |
| `LANGSMITH_PROJECT` | `tazkiyah-rag-v2` | LangSmith project name |
| `COLLECTION_NAME` | `quran_tazkiyah_v2` | ChromaDB collection |
| `TOP_K` | `5` | Documents to retrieve |
| `LLM_TEMPERATURE` | `0.3` | LLM temperature |
| `LLM_MAX_TOKENS` | `1024` | Max response tokens |
| `LOG_LEVEL` | `INFO` | Logging level |
