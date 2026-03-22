# Tazkiyah RAG

Quranic knowledge retrieval pipeline optimized for RTX 3080 10GB.

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌───────────────┐
│  Chunks JSONL   │────▶│    Embeddings    │────▶│   ChromaDB    │
│  (fatiha...)    │     │ nomic-v2-moe     │     │  Vector Store │
└─────────────────┘     └──────────────────┘     └───────────────┘
                                                         │
                                                         ▼
                        ┌──────────────────┐     ┌───────────────┐
                        │   gemma3:4b LLM  │◀────│   Retrieval   │
                        │   (Ollama)       │     │   (top-k=5)   │
                        └──────────────────┘     └───────────────┘
```

## Tech Stack

- **Embeddings**: `nomic-embed-text-v2-moe` (Ollama) - requires prefixes
- **LLM**: `gemma3:4b` (Ollama) - fits in 10GB VRAM
- **Vector Store**: ChromaDB with persistence
- **Framework**: LangChain (langchain-ollama, langchain-chroma, langchain-core)
- **UI**: Gradio 6.0 with debug logging

## Files

| File | Purpose |
|------|---------|
| `config.py` | Configuration constants (fully customizable) |
| `rag_pipeline.py` | Core TazkiyahRAG class |
| `index_chunks.py` | CLI to index JSONL chunks |
| `query_rag.py` | CLI to query |
| `chat.py` | Terminal chat REPL |
| `chat_ui.py` | Gradio 6.0 web UI with debug panel |

## Quick Start

### 1. Prerequisites

```bash
# Install dependencies
pip install -r requirements.txt

# Pull Ollama models
ollama pull nomic-embed-text-v2-moe
ollama pull gemma3:4b
```

### 2. Index Chunks

```bash
python -m rag.index_chunks fatiha.chunks.jsonl
```

Options:
- `--clear`: Delete existing documents first
- `--batch-size N`: Documents per batch (default: 100)

### 3. Query

**Terminal CLI:**
```bash
python -m rag.query_rag "What is the meaning of Bismillah?"
```

**Terminal Chat:**
```bash
python -m rag.chat
```

**Web UI:**
```bash
python -m rag.chat_ui
```
Open http://127.0.0.1:7860

## Configuration

Edit `rag/config.py` to customize the entire pipeline. All settings support environment variable overrides.

### 🔍 Retrieval Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `TOP_K` | 5 | Number of documents to retrieve |
| `SEARCH_TYPE` | "similarity" | Use "mmr" for diverse results |
| `MIN_RELEVANCE_SCORE` | 0.0 | Filter low-score documents |

### 💬 LLM Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `LLM_MODEL` | "gemma3:4b" | Ollama model name |
| `LLM_TEMPERATURE` | 0.3 | 0=factual, 1=creative |
| `LLM_MAX_TOKENS` | 1024 | Max response length |
| `LLM_TOP_P` | 0.9 | Nucleus sampling |
| `LLM_REPEAT_PENALTY` | 1.1 | Discourage repetition |

### 📝 Prompts

| Setting | Description |
|---------|-------------|
| `SYSTEM_PROMPT` | Assistant personality |
| `RAG_PROMPT_TEMPLATE` | Template with {context} and {question} |

### 🌐 UI Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `UI_SERVER_HOST` | "127.0.0.1" | Gradio host |
| `UI_SERVER_PORT` | 7860 | Gradio port |
| `SHOW_SOURCES` | true | Show sources in chat |
| `MAX_SOURCES_DISPLAY` | 5 | Number of sources to show |

### Environment Variable Override

```powershell
$env:TOP_K = "3"
$env:LLM_TEMPERATURE = "0.1"
$env:LLM_MODEL = "qwen3:8b"
python -m rag.chat_ui
```

### Quick Presets

Uncomment in `config.py`:

```python
# FAST PRESET (quick responses)
TOP_K = 3
LLM_MAX_TOKENS = 512

# THOROUGH PRESET (detailed answers)
TOP_K = 10
LLM_MAX_TOKENS = 2048
```

## Debug Panel

The web UI includes a debug panel showing every step of the RAG pipeline:

1. **QUERY** - User's question
2. **RETRIEVAL** - Searching for similar documents
3. **RETRIEVED_DOCS** - Each document with similarity score
4. **CONTEXT** - Combined context from retrieved documents
5. **FULL_PROMPT** - Complete prompt sent to LLM
6. **LLM_CALL** - Model being invoked
7. **LLM_RESPONSE** - Full response from LLM

## Gradio 6.0 Notes

The chat UI uses Gradio 6.0's new message format:

```python
# OLD (removed in 6.0)
[("user msg", "bot msg"), ...]

# NEW (required in 6.0)
[
    {"role": "user", "content": "user msg"},
    {"role": "assistant", "content": "bot msg"},
]
```

## Troubleshooting

**"No documents indexed"**
```bash
python -m rag.index_chunks fatiha.chunks.jsonl
```

**Model not found**
```bash
ollama list  # Check available models
ollama pull gemma3:4b
```

**CUDA out of memory**
- Use smaller LLM: `gemma3:1b` instead of `4b`
- Reduce batch size when indexing
- Lower TOP_K in config

**Import errors**
```bash
pip install langchain-ollama langchain-chroma langchain-core gradio
```
