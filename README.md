<div align="center">


# PROJECT DEMO + CODEBASE WALKTHROUGH

## Open the demo first

[![Watch the walkthrough](https://img.shields.io/badge/Watch%20the%20walkthrough-Google%20Drive-1a73e8?style=for-the-badge&logo=google-drive&logoColor=white)](https://drive.google.com/file/d/1jHUGgBWAn-LgU5Yo1c6Jp-R8ZkYu5WN2/view?usp=sharing)

**Basic codebase walkthrough + project demo**

</div>

# Tazkiyah

AI-powered Quranic guidance platform that bridges daily life questions with contextually relevant Quranic verses and commentary.

## Product Vision

Tazkiyah helps Muslims describe real-life struggles in natural language and receive Quranic guidance with context, compassion, and clarity.

The long-term product includes conversational guidance, reflection workflows, community wisdom, and growth tracking. The repository currently contains the backend API foundation and the supporting collection/RAG tooling required to power those experiences.

## Features

- Conversational Quran guidance backend with category-aware responses.
- Semantic retrieval against a Quran vector store (RAG v2 data pipeline).
- Streaming and non-streaming chat APIs for frontend integration.
- Runtime health/config endpoints for diagnostics and app bootstrap.
- Quran collection toolkit with translations, tafsir, and validation workflows.
- Chunk preparation and indexing tooling for retrieval quality.

## Current Scope (Implemented)

- Backend API (FastAPI + LangGraph):
  - GET /health
  - GET /api/v1/config
  - POST /api/v1/chat (SSE)
  - POST /api/v1/chat/sync (JSON)
- Data and retrieval tooling:
  - Quran collection and validation utilities under tools/python/collection
  - RAG v2 pipeline under tools/python/rag_v2
  - Model-specific Chroma vector stores under data/vectorstores/rag_v2/<provider>/<model>/<collection>
  - Vectorstore discovery CLI: `python -m tools.python.rag_v2.list_vectorstores`
- Frontend status:
  - React + Vite scaffold exists in frontend/
  - Product UI features are in active build phase

## Planned Product Capabilities (Roadmap)

- Verse card system with Arabic/transliteration/translation controls.
- Reflection journal with mood tracking and bookmarks.
- Community wisdom wall (anonymous reflections).
- Progress and growth dashboard.
- Personalized verse-of-the-day and preference adaptation.

## Run the Project (Frontend + Backend) - Start Here

Use this sequence first. Collection/tooling commands come later in this README.

### 1. Prerequisites

- Python 3.11+
- Node.js 20+ and npm
- Ollama

### 2. Install backend dependencies

```powershell
# Windows (PowerShell)
cd "d:\Work\Quran Project\Tazkiyah"
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

```bash
# Linux / macOS
cd /path/to/Tazkiyah
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Install frontend dependencies

```bash
cd frontend
npm install
```

### 4. Configure frontend API URL

Create `frontend/.env.local`:

```dotenv
VITE_API_BASE_URL=http://127.0.0.1:8000
```

### 5. Install and run Ollama

Install Ollama (pick your OS):

```powershell
# Windows
winget install Ollama.Ollama
```

```bash
# macOS
brew install ollama
```

```bash
# Linux
curl -fsSL https://ollama.com/install.sh | sh
```

Start Ollama if it is not already running:

```bash
ollama serve
```

Pull required models:

```bash
ollama pull gemma3:4b
ollama pull qwen3-embedding:8b
```

Verify models:

```bash
ollama list
```

### 6. Build the vector store once

The backend expects a model-matched Chroma store. Build it once before running chat:

```powershell
python -m tools.python.rag_v2.build_vectorstore
```

Optional (build a store for another embedding model):

```powershell
python -m tools.python.rag_v2.build_vectorstore --embedding-model "jina/jina-embeddings-v2-base-en"
```

### 7. Run backend API

```powershell
& "d:/Work/Quran Project/Tazkiyah/venv/Scripts/python.exe" -m uvicorn backend.main:app --reload
```

Backend endpoints:

- `GET /health`
- `GET /api/v1/config`
- `POST /api/v1/chat` (SSE streaming)
- `POST /api/v1/chat/sync` (JSON)

### 8. Run frontend app

In a second terminal:

```bash
cd frontend
npm run dev
```

Then open the local Vite URL shown in terminal (usually `http://127.0.0.1:5173`).

### 9. Quick verification

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/api/v1/config
```

If you need to override model/provider settings, create a root `.env` file and set values like `LLM_MODEL`, `EMBEDDING_MODEL`, and `OLLAMA_BASE_URL`.

## Repository Layout

The repository is organized as a separation-first monorepo.

- `frontend/` hosts the React + Vite + TypeScript app.
- `backend/` contains the FastAPI + LangGraph chatbot backend.
- `tools/python/collection/` holds the Quran collection tooling.
- `tools/python/rag_v1/` holds the legacy RAG pipeline and compatibility tools.
- `tools/python/rag_v2/` holds the active RAG pipeline.
- `data/` holds raw, processed, sample, and vectorstore artifacts.
- `docs/` contains the migration and boundary notes.

## Data Collection and Tooling (After App Setup)

### Basic Commands

```bash
# Collect all surahs
python -m tools.python.collection.collect_quran --all -t 20,85 -o quran.jsonl

# Collect single surah
python -m tools.python.collection.collect_quran --surah 2 -t 20 -o baqarah.jsonl

# Collect range of surahs
python -m tools.python.collection.collect_quran --surah-range 1 10 -t 20,85 -o first_ten.jsonl

# Resume interrupted collection
python -m tools.python.collection.collect_quran --all -t 20 --resume -o quran.jsonl

# Validate existing data
python -m tools.python.collection.collect_quran --validate-only -o quran.jsonl

# Build the vector store for the active embedding model
python -m tools.python.rag_v2.build_vectorstore

# List all already-built vectorstores
python -m tools.python.rag_v2.list_vectorstores
```

### CLI Options

| Option | Short | Description |
|--------|-------|-------------|
| `--all` | | Collect all 114 surahs |
| `--surah N` | `-s N` | Collect specific surah (1-114) |
| `--surah-range START END` | `-r` | Collect range of surahs |
| `--translations IDS` | `-t` | Comma-separated translation IDs |
| `--tafsirs IDS` | `-T` | Comma-separated tafsir IDs (optional) |
| `--output FILE` | `-o` | Output file path |
| `--output-format {jsonl,json}` | `-f` | Output format (default: jsonl) |
| `--concurrency N` | `-c` | Parallel threads for tafsir (1-10) |
| `--batch-size N` | `-b` | Buffer size before writing (default: 50) |
| `--resume` | | Resume from existing file |
| `--no-metadata` | | Exclude verse metadata |
| `--config FILE` | | Load from config file |
| `--list-resources` | | Show available translations/tafsirs |
| `--validate-only` | | Validate existing file |
| `--verbose` | `-v` | Verbose output |
| `--debug` | | Debug output |

## Output Format

### JSONL (Default)

Each line is a JSON object:

```json
{"verse_id": "1:1", "surah_number": 1, "verse_number": 1, ...}
{"verse_id": "1:2", "surah_number": 1, "verse_number": 2, ...}
```

### JSON

Single array of verses:

```json
[
  {"verse_id": "1:1", ...},
  {"verse_id": "1:2", ...}
]
```

### Verse Schema

```json
{
  "verse_id": "2:255",
  "surah_number": 2,
  "verse_number": 255,
  "surah_name": "Al-Baqarah",
  "surah_name_arabic": "البقرة",
  "arabic_text": "ٱللَّهُ لَآ إِلَـٰهَ إِلَّا هُوَ ٱلْحَىُّ ٱلْقَيُّومُ...",
  "translations": {
    "Saheeh International": "Allah - there is no deity except Him,[1] the Ever-Living...",
    "M.A.S. Abdel Haleem": "God: there is no god but Him..."
  },
  "footnotes": {
    "1": "i.e., no one worthy of worship except Him."
  },
  "tafsirs": {
    "Tafsir Ibn Kathir": "This is Ayat Al-Kursi..."
  },
  "metadata": {
    "juz": 3,
    "page": 42,
    "hizb": 5,
    "rub_el_hizb": 17,
    "ruku": 35,
    "manzil": 1,
    "sajdah": null,
    "revelation_place": "madinah",
    "revelation_order": 87
  }
}
```

**Note:** Footnote markers in translations (e.g., `[1]`, `[2]`) reference the corresponding entries in the `footnotes` object. When using multiple translations, footnotes are prefixed with the translation name for disambiguation (e.g., `"Saheeh International:1"`).

## Popular Resource IDs

### Translations

| ID | Name | Language |
|----|------|----------|
| 20 | Saheeh International | English |
| 85 | M.A.S. Abdel Haleem | English |
| 95 | Dr. Mustafa Khattab (The Clear Quran) | English |
| 84 | Mufti Taqi Usmani | English |
| 20 | Pickthall | English |
| 22 | Yusuf Ali | English |

### Tafsirs

| ID | Name | Language |
|----|------|----------|
| 169 | Tafsir Ibn Kathir | English |
| 91 | Maariful Quran | English |
| 93 | Tafsir al-Jalalayn | Arabic |
| 168 | Tafsir al-Tabari | Arabic |

Run `python -m tools.python.collection.collect_quran --list-resources` for the complete list.

## Configuration File

Create `config.json` from `config.example.json`:

```json
{
  "surahs": {
    "mode": "all"
  },
  "translations": {
    "ids": [20, 85]
  },
  "tafsirs": {
    "ids": [169]
  },
  "output": {
    "file": "quran_data.jsonl",
    "format": "jsonl"
  },
  "performance": {
    "concurrency": 3,
    "batch_size": 50
  }
}
```

Use with: `python -m tools.python.collection.collect_quran --config config.json`

## Utilities

### Convert JSONL to JSON

```bash
python -m tools.python.collection.convert_to_json quran_data.jsonl
# Creates quran_data.json

python -m tools.python.collection.convert_to_json quran_data.jsonl output.json --compact
```

### Validate Data

```bash
python -m tools.python.collection.validate_data quran_data.jsonl
python -m tools.python.collection.validate_data quran_data.jsonl -v  # verbose
python -m tools.python.collection.validate_data quran_data.jsonl -o report.txt
```

### Prepare RAG Chunks

Transform raw collected data into clean, embedding-ready chunks:

```bash
# Preview chunks before processing
python -m tools.python.collection.prepare_chunks quran_data.jsonl --preview 3

# Show input statistics
python -m tools.python.collection.prepare_chunks quran_data.jsonl --stats-only

# Full processing with structured format
python -m tools.python.collection.prepare_chunks quran_data.jsonl -o chunks.jsonl

# Minimal format with tafsir truncation (good for embeddings)
python -m tools.python.collection.prepare_chunks quran_data.jsonl -o chunks.jsonl --chunk-format minimal --max-tafsir 2000

# Skip Arabic text and tafsir (translations only)
python -m tools.python.collection.prepare_chunks quran_data.jsonl -o chunks.jsonl --no-arabic --no-tafsir
```

#### Chunk Processor Options

| Option | Description |
|--------|-------------|
| `--chunk-format {structured,prose,minimal}` | Output format style (default: structured) |
| `--output-format {jsonl,json,txt}` | File format (default: jsonl) |
| `--inline-footnotes / --no-inline-footnotes` | Inline footnotes in text (default: inline) |
| `--max-tafsir N` | Truncate tafsir to N characters |
| `--no-arabic` | Exclude Arabic text from chunks |
| `--no-tafsir` | Exclude tafsir from chunks |
| `--no-clean-html` | Keep HTML tags (not recommended) |
| `--preview N` | Preview first N chunks without writing |
| `--stats-only` | Show input statistics only |

#### Chunk Formats

- **structured** - Sectioned with headers (`=== Verse 1:1 ===`), best for readability
- **prose** - Flowing paragraph style, natural reading
- **minimal** - Compact format optimized for vector embeddings

#### Chunk Output Schema

```json
{
  "id": "2:255",
  "text": "=== Verse 2:255 - Al-Baqarah ===\n\nArabic:\nٱللَّهُ لَآ إِلَـٰهَ...",
  "metadata": {
    "verse_id": "2:255",
    "surah_number": 2,
    "verse_number": 255,
    "surah_name": "Al-Baqarah",
    "juz": 3,
    "hizb": 5,
    "page": 42,
    "revelation_place": "madinah"
  },
  "arabic_text": "ٱللَّهُ لَآ إِلَـٰهَ إِلَّا هُوَ...",
  "translations": {
    "Saheeh International": "Allah - there is no deity except Him..."
  },
  "tafsirs": {
    "Ibn Kathir (Abridged)": "This is Ayat Al-Kursi..."
  },
  "footnotes": {
    "1": "i.e., no one worthy of worship except Him."
  }
}
```

## Rate Limiting & Circuit Breaker

The script includes built-in protection against rate limiting:

- **Minimum delay**: 0.3 seconds between requests
- **Circuit breaker**: After 5 consecutive 429 errors:
  - Pauses for 60 seconds
  - Reduces concurrency by 50%
  - Auto-resumes

## Troubleshooting

### "Rate limited" messages

The API is limiting requests. The script handles this automatically by:
1. Backing off exponentially
2. Reducing concurrency
3. Pausing when needed

### Incomplete collection

Use `--resume` to continue:
```bash
python -m tools.python.collection.collect_quran --all -t 20 --resume -o quran.jsonl
```

### Validation failures

Run validation to check data:
```bash
python -m tools.python.collection.validate_data quran_data.jsonl -v
```

## RAG Pipeline

After preparing chunks, use the RAG pipeline to query Quranic knowledge with AI:

### Quick Start

```bash
# Index chunks into ChromaDB
python -m tools.python.rag_v2.index_data

# Launch web chat UI
python -m tools.python.rag_v2.chat_ui

# Or use terminal chat
python -m tools.python.rag_v2.chat

# Or single query
python -m tools.python.rag_v2.query_rag "What is the meaning of Bismillah?"
```

### RAG Architecture

```
Quran JSON (rag_v2 source) -> Embeddings (jina/jina-embeddings-v2-base-en) -> ChromaDB -> Retrieval -> LLM (gemma3:4b) -> Answer
```

### Configuration

Edit `tools/python/rag_v2/config.py` to customize:
- **TOP_K**: Number of documents to retrieve (default: 5)
- **LLM_MODEL**: Ollama model (default: gemma3:4b)
- **LLM_TEMPERATURE**: 0=factual, 1=creative (default: 0.3)
- **RAG_PROMPT_TEMPLATE**: Custom prompt template

See [tools/python/rag_v2/README.md](tools/python/rag_v2/README.md) for full documentation.

## Project Structure

```
Tazkiyah/
├── backend/                      # FastAPI + LangGraph API
├── frontend/                     # React + Vite app (in progress)
├── tools/python/collection/      # Quran collection + validation utilities
├── tools/python/rag_v2/          # Active RAG v2 pipeline
├── tools/python/rag_v1/          # Legacy pipeline and compatibility tools
├── data/                         # Raw, processed, samples, vectorstores
├── docs/                         # Architecture and migration notes
├── requirements.txt
├── config.example.json
└── SETUP.md
```

## License

This project is for educational and research purposes. Quran data is sourced from the [Quran Foundation](https://quran.foundation).

## Contributing

Contributions are welcome! Please ensure:
- Code follows PEP 8 style guide
- Type hints are used throughout
- Docstrings are provided for all functions
- Tests pass before submitting
