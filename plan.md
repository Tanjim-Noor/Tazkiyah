## Plan: Quran Data Collection Script for RAG (Final)

A Python CLI tool collecting Quran verses, translations, and optional tafsirs from the Quran Foundation API. Uses JSONL format with 50-verse batch writes, parallel tafsir fetching with circuit breaker protection, and chapter-level resume granularity.

### Steps

1. **Create virtual environment and setup files** - Create [SETUP.md](SETUP.md) with mandatory venv instructions, [requirements.txt](requirements.txt) with packages only (no versions): `requests`, `tqdm`, `click`. Query Context7 for latest docs/best practices.

2. **Implement API client with circuit breaker** - Create [quran_api.py](quran_api.py) with: `requests.Session`, 0.3s minimum delay, 429 detection, circuit breaker (5 consecutive 429s → pause 60s, reduce concurrency 50%, log "Rate limited. Pausing 60s. Reducing concurrency X→Y"), thread-safe request tracking.

3. **Build parallel tafsir fetcher** - Create [tafsir_fetcher.py](tafsir_fetcher.py) with `ThreadPoolExecutor`, default 3 threads (configurable 1-10), graceful degradation on errors, respects circuit breaker state from API client.

4. **Build collector with batch JSONL writes** - Create [collector.py](collector.py) to: buffer verses in memory, flush every 50 verses (configurable `--batch-size`), flush on completion/interruption via signal handler, chapter-level resume (parse JSONL for last `verse_key`, re-fetch incomplete chapters).

5. **Implement CLI entry point** - Create [collect_quran.py](collect_quran.py) with `click`: `--output-format {jsonl,json}`, `--concurrency N`, `--batch-size N`, `--tafsirs` (optional), `--resume` (chapter-level), nested `tqdm` progress, signal handler for graceful shutdown.

6. **Create utilities and documentation** - Build [convert_to_json.py](convert_to_json.py), [validate_data.py](validate_data.py), [config.example.json](config.example.json), and [README.md](README.md) with dev/production examples.

### File Structure
```
Tazkiyah/
├── SETUP.md                  # Venv setup (mandatory)
├── README.md                 # Usage guide
├── requirements.txt          # requests, tqdm, click (no versions)
├── config.example.json
├── collect_quran.py          # CLI entry point
├── quran_api.py              # API client + circuit breaker
├── collector.py              # Data collection + batch writes
├── tafsir_fetcher.py         # Parallel tafsir fetching
├── validate_data.py          # Validation utility
└── convert_to_json.py        # JSONL → JSON converter
```

### Architecture Diagram
```
┌─────────────────────────────────────────────────────────────┐
│                    collect_quran.py (CLI)                   │
│  --all --translations 131,85 --tafsirs 169 --concurrency 5  │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                     collector.py                            │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────────┐ │
│  │ Fetch       │  │ Memory      │  │ JSONL Writer         │ │
│  │ Chapters    │→ │ Buffer      │→ │ (flush every 50)     │ │
│  └─────────────┘  │ [verses...] │  └──────────────────────┘ │
│                   └─────────────┘                           │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                     quran_api.py                            │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ QuranAPIClient                                        │  │
│  │ • Session pooling    • 0.3s delay    • Retry logic    │  │
│  │ • Circuit breaker: 5x429 → pause 60s, concurrency/2   │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│              tafsir_fetcher.py (ThreadPoolExecutor)         │
│  Thread 1: /tafsirs/169/by_ayah/1:1                         │
│  Thread 2: /tafsirs/169/by_ayah/1:2                         │
│  Thread 3: /tafsirs/169/by_ayah/1:3                         │
└─────────────────────────────────────────────────────────────┘
```

### Circuit Breaker Flow
```
Normal Operation
      │
      ▼
┌─────────────┐     429      ┌─────────────┐
│ Request API │────────────→ │ Increment   │
└─────────────┘              │ fail_count  │
      │                      └──────┬──────┘
      │ 200                         │
      ▼                             ▼
┌─────────────┐              fail_count >= 5?
│ Reset       │                     │
│ fail_count  │              ┌──────┴──────┐
└─────────────┘              No           Yes
                             │             │
                             ▼             ▼
                        Continue    ┌─────────────────┐
                                    │ Log: "Rate      │
                                    │ limited..."     │
                                    │ Sleep 60s       │
                                    │ concurrency /= 2│
                                    └────────┬────────┘
                                             │
                                             ▼
                                        Auto-resume
```

### Resume Logic Flow
```
--resume flag provided
        │
        ▼
┌───────────────────┐
│ Parse existing    │
│ JSONL file        │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│ Find all unique   │
│ chapter numbers   │
│ from verse_keys   │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│ Identify last     │
│ COMPLETE chapter  │
│ (all verses exist)│
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│ Resume from next  │
│ chapter (re-fetch │
│ partial chapters) │
└───────────────────┘
```
