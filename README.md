# Tazkiyah

Separation-first monorepo for Quran data collection and RAG tooling.

## Features

- 📖 **Complete Quran Collection** - All 114 surahs, 6236 verses
- 🌍 **Multiple Translations** - Support for 100+ translations
- 📚 **Tafsir Integration** - Optional commentary from major tafsir sources
- 📝 **Footnote Extraction** - Automatic footnote fetching and linking
- ⚡ **Parallel Processing** - Configurable concurrent tafsir fetching
- 💾 **JSONL Output** - Streaming format with resume capability
- 🔄 **Resume Support** - Continue interrupted collections
- 🛡️ **Rate Limiting** - Built-in circuit breaker and backoff
- ✅ **Validation** - Verify data completeness and integrity
- 🧹 **RAG Chunk Preparation** - Clean HTML, format text for embeddings

## Quick Start

### 1. Setup Virtual Environment

```powershell
# Windows (PowerShell)
cd "d:\Work\Quran Project\Tazkiyah"
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Repository Layout

The repository is organized as a separation-first monorepo.

- `frontend/` is reserved for the future React + Vite + TypeScript app.
- `backend/` is reserved for the future FastAPI app.
- `tools/python/collection/` holds the Quran collection tooling.
- `tools/python/rag_v1/` holds the legacy RAG pipeline and compatibility tools.
- `tools/python/rag_v2/` holds the active RAG pipeline.
- `data/` holds raw, processed, sample, and vectorstore artifacts.
- `docs/` contains the migration and boundary notes.

No frontend or backend framework scaffold is created yet.

```bash
# Linux / macOS
cd /path/to/Tazkiyah
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. List Available Resources

```bash
python -m tools.python.collection.collect_quran --list-resources
```

### 3. Collect Data

```bash
# Quick test: First 3 surahs
python -m tools.python.collection.collect_quran --surah-range 1 3 --translations 20,85 --output test.jsonl

# Full collection with tafsir
python -m tools.python.collection.collect_quran --all --translations 20,85 --tafsirs 169 --output quran_complete.jsonl
```

## Usage

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

Run `python collect_quran.py --list-resources` for the complete list.

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
python prepare_chunks.py quran_data.jsonl --preview 3

# Show input statistics
python prepare_chunks.py quran_data.jsonl --stats-only

# Full processing with structured format
python prepare_chunks.py quran_data.jsonl -o chunks.jsonl

# Minimal format with tafsir truncation (good for embeddings)
python prepare_chunks.py quran_data.jsonl -o chunks.jsonl --chunk-format minimal --max-tafsir 2000

# Skip Arabic text and tafsir (translations only)
python prepare_chunks.py quran_data.jsonl -o chunks.jsonl --no-arabic --no-tafsir
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
python collect_quran.py --all -t 20 --resume -o quran.jsonl
```

### Validation failures

Run validation to check data:
```bash
python validate_data.py quran_data.jsonl -v
```

## RAG Pipeline

After preparing chunks, use the RAG pipeline to query Quranic knowledge with AI:

### Quick Start

```bash
# Index chunks into ChromaDB
python -m rag.index_chunks fatiha.chunks.jsonl

# Launch web chat UI
python -m rag.chat_ui

# Or use terminal chat
python -m rag.chat

# Or single query
python -m rag.query_rag "What is the meaning of Bismillah?"
```

### RAG Architecture

```
Chunks JSONL → Embeddings (nomic-v2-moe) → ChromaDB → Retrieval → LLM (gemma3:4b) → Answer
```

### Configuration

Edit `rag/config.py` to customize:
- **TOP_K**: Number of documents to retrieve (default: 5)
- **LLM_MODEL**: Ollama model (default: gemma3:4b)
- **LLM_TEMPERATURE**: 0=factual, 1=creative (default: 0.3)
- **RAG_PROMPT_TEMPLATE**: Custom prompt template

See [rag/README.md](rag/README.md) for full documentation.

## Project Structure

```
Tazkiyah/
├── README.md             # This file
├── SETUP.md              # Setup instructions
├── requirements.txt      # Dependencies
├── config.example.json   # Configuration template
│
├── collect_quran.py      # Main collection CLI
├── quran_api.py          # API client
├── collector.py          # Data collection logic
├── tafsir_fetcher.py     # Parallel tafsir fetching
│
├── prepare_chunks.py     # RAG chunk preparation CLI
├── chunk_processor.py    # Chunk processing logic
│
├── validate_data.py      # Validation utility
├── convert_to_json.py    # JSONL → JSON converter
│
└── rag/                  # RAG Pipeline
    ├── config.py         # Configuration (models, retrieval, prompts)
    ├── rag_pipeline.py   # Core TazkiyahRAG class
    ├── index_chunks.py   # Index chunks CLI
    ├── query_rag.py      # Query CLI
    ├── chat.py           # Terminal chat
    ├── chat_ui.py        # Gradio web UI
    └── README.md         # RAG documentation
```

## License

This project is for educational and research purposes. Quran data is sourced from the [Quran Foundation](https://quran.foundation).

## Contributing

Contributions are welcome! Please ensure:
- Code follows PEP 8 style guide
- Type hints are used throughout
- Docstrings are provided for all functions
- Tests pass before submitting
