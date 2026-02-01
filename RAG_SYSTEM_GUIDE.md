# Tazkiyah RAG System - Complete Technical Guide

## Table of Contents
1. [Overview](#overview)
2. [End-to-End Flow](#end-to-end-flow)
3. [Chunk Structure & Storage](#chunk-structure--storage)
4. [Embedding Model & Storage](#embedding-model--storage)
5. [Semantic Similarity & Retrieval](#semantic-similarity--retrieval)
6. [Query Execution & Field Access](#query-execution--field-access)
7. [Code Examples](#code-examples)
8. [Architectural Diagram](#architectural-diagram)

---

## Overview

The Tazkiyah RAG (Retrieval-Augmented Generation) system is a production-ready pipeline that:

1. **Prepares** Quranic data into clean, embedding-ready chunks
2. **Indexes** chunks into ChromaDB vector database using embeddings
3. **Retrieves** semantically similar chunks when users query
4. **Generates** contextual answers using LLM powered by retrieved documents
5. **Serves** results through CLI, terminal chat, and web UI

**Technology Stack:**
- **Embeddings**: `nomic-embed-text-v2-moe` (768-dim, 305M active parameters)
- **Vector DB**: ChromaDB (persisted locally at `rag/chroma_db/`)
- **LLM**: Ollama models (default: `gemma3:4b`)
- **Framework**: LangChain with latest patterns
- **UI**: Gradio 6.0 web interface, Rich CLI

---

## End-to-End Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    COMPLETE PIPELINE FLOW                       │
└─────────────────────────────────────────────────────────────────┘

PHASE 1: DATA COLLECTION & PREPARATION
─────────────────────────────────────────────────────────────────

    collect_quran.py          quran_api.py
         ↓                          ↓
    Collect verses from Quran Foundation API
    (114 surahs, 6236 verses)
         ↓
    Output: quran_data.jsonl
    {
      "verse_id": "2:255",
      "surah_number": 2,
      "verse_number": 255,
      "arabic_text": "ٱللَّهُ لَآ إِلَـٰهَ...",
      "translations": {...},
      "tafsirs": {...},
      "footnotes": {...},
      "metadata": {...}
    }

         ↓
    prepare_chunks.py
         ↓
    Clean HTML, format text, inline footnotes
         ↓
    Output: fatiha.chunks.jsonl
    
PHASE 2: INDEXING INTO VECTOR DATABASE
─────────────────────────────────────────────────────────────────

    fatiha.chunks.jsonl
         ↓
    index_chunks.py
         ↓
    Load JSONL file → Parse chunks
         ↓
    create_documents_from_chunks()
         ↓
    Convert to LangChain Document objects
    {
      page_content: "=== Verse 1:1 - Al-Fatihah ===\n...",
      metadata: {
        verse_id: "1:1",
        surah_name: "Al-Fatihah",
        juz: 1,
        page: 1,
        arabic_text: "بِسْمِ ٱللَّهِ...",
        ...
      }
    }
         ↓
    Add document prefix (if needed)
    "search_document: " + page_content
         ↓
    TazkiyahRAG.add_documents()
         ↓
    OllamaEmbeddings generates vectors (768-dim)
         ↓
    ChromaDB stores: (id, embedding, metadata, content)
         ↓
    Persisted at: rag/chroma_db/

PHASE 3: QUERY EXECUTION
─────────────────────────────────────────────────────────────────

    User Question
    "What is Bismillah?"
         ↓
    rag.query(question)
         ↓
    ┌─ Step 1: ADD QUERY PREFIX
    │  "search_query: What is Bismillah?"
    │
    ├─ Step 2: RETRIEVE SIMILAR DOCUMENTS
    │  similarity_search_with_score(prefixed_query, k=5)
    │         ↓
    │  ChromaDB cosine similarity search
    │         ↓
    │  Returns: [(Document, score), ...]
    │  [
    │    (Document(1:1), 0.8932),
    │    (Document(1:2), 0.7654),
    │    (Document(109:1), 0.6543),
    │    (Document(1:3), 0.5432),
    │    (Document(24:35), 0.4321)
    │  ]
    │
    ├─ Step 3: BUILD CONTEXT
    │  context = "\n\n".join([doc.page_content for doc in retrieved_docs])
    │
    ├─ Step 4: CREATE PROMPT
    │  prompt = ChatPromptTemplate.from_template(RAG_PROMPT_TEMPLATE)
    │
    ├─ Step 5: BUILD LLM CHAIN
    │  chain = prompt | llm | StrOutputParser()
    │
    └─ Step 6: GENERATE ANSWER
       result = chain.invoke({
         "context": context,
         "question": question
       })
         ↓
    Output: AI-generated answer with sources

PHASE 4: UI SERVING
─────────────────────────────────────────────────────────────────

    Terminal Chat (chat.py)
    ↓
    Web UI (chat_ui.py)
    ↓
    Single Query (query_rag.py)
    ↓
    All powered by: TazkiyahRAG.query()
```

---

## Chunk Structure & Storage

### Chunk Format (JSONL)

Each line in the chunks file is a complete JSON object representing one verse:

```json
{
  "id": "1:1",
  "text": "=== Verse 1:1 - Al-Fatihah (الفاتحة) ===\n\nArabic:\nبِسْمِ ٱللَّهِ ٱلرَّحْمَـٰنِ ٱلرَّحِيمِ\n\nTranslation:\n  [Saheeh International] In the name of Allāh...\n  [M.A.S. Abdel Haleem] In the name of God...\n\nTafsir (Ibn Kathir (Abridged)):\nIntroduction to Fatihah Which was revealed...",
  
  "metadata": {
    "verse_id": "1:1",
    "surah_number": 1,
    "verse_number": 1,
    "surah_name": "Al-Fatihah",
    "surah_name_arabic": "الفاتحة",
    "juz": 1,
    "hizb": 1,
    "page": 1,
    "revelation_place": "makkah"
  },
  
  "arabic_text": "بِسْمِ ٱللَّهِ ٱلرَّحْمَـٰنِ ٱلرَّحِيمِ",
  
  "translations": {
    "Saheeh International": "In the name of Allāh, (Allāh is a proper name...) the Entirely Merciful...",
    "M.A.S. Abdel Haleem": "In the name of God, the Lord of Mercy..."
  },
  
  "tafsirs": {
    "Ibn Kathir (Abridged)": "Introduction to Fatihah Which was revealed in Makkah..."
  },
  
  "footnotes": {
    "Saheeh International:1": "Allāh is a proper name belonging only to the one...",
    "Saheeh International:2": "Ar-Raḥmān and ar-Raḥeem are two names of Allāh..."
  }
}
```

### Key Fields Explained

| Field | Type | Purpose | Example |
|-------|------|---------|---------|
| `id` | string | Unique identifier (verse_id) | `"1:1"` |
| `text` | string | **MAIN CONTENT** used for embeddings & display | Formatted full verse |
| `metadata` | object | ChromaDB metadata (searchable) | `{verse_id, surah_name, juz, ...}` |
| `arabic_text` | string | Original Arabic text | Arabic verse |
| `translations` | object | Multiple translations by name | Keys: translator names |
| `tafsirs` | object | Commentary by source | Keys: tafsir names |
| `footnotes` | object | Explanation of translation notes | Keys: `"TranslatorName:footnote_id"` |

### Chunk Formats (Customizable)

You can generate chunks in different formats:

```bash
# Structured (default) - Best for readability
python prepare_chunks.py data.jsonl --chunk-format structured

# Prose - Natural flowing paragraph
python prepare_chunks.py data.jsonl --chunk-format prose

# Minimal - Compact, optimized for embeddings
python prepare_chunks.py data.jsonl --chunk-format minimal --max-tafsir 2000
```

**Structured Format:**
```
=== Verse 1:1 - Al-Fatihah ===

Arabic:
بِسْمِ ٱللَّهِ...

Translation:
  [Saheeh International] In the name of Allah...
  [M.A.S. Abdel Haleem] In the name of God...

Tafsir (Ibn Kathir):
Introduction to Fatihah...
```

**Prose Format:**
```
In Verse 1:1 of Al-Fatihah (الفاتحة), the Arabic text reads: بِسْمِ ٱللَّهِ...

According to the Saheeh International translation: "In the name of Allāh, the Entirely Merciful, the Especially Merciful."

The M.A.S. Abdel Haleem translation states: "In the name of God, the Lord of Mercy, the Giver of Mercy!"

Ibn Kathir provides this tafsir commentary: "Introduction to Fatihah Which was revealed in Makkah..."
```

---

## Embedding Model & Storage

### Embedding Process

#### 1. **Model Configuration**

```python
# From config.py
EMBEDDING_MODEL = "nomic-embed-text-v2-moe"  # 768-dimensional embeddings

# Prefixes for nomic-embed-text-v2-moe
EMBED_QUERY_PREFIX = "search_query: "        # Added to user queries
EMBED_DOCUMENT_PREFIX = "search_document: "  # Added to chunk text
```

**Why Prefixes?**
- `nomic-embed-text-v2-moe` is trained to recognize these prefixes
- Improves semantic alignment between query and document embeddings
- Other models (bge-m3, mxbai-embed-large) don't require prefixes

#### 2. **Vector Storage Structure in ChromaDB**

ChromaDB stores data in a structured format:

```
rag/chroma_db/
├── chroma.sqlite3          # Main database file
└── 0d602136-eb1e.../       # Collection directory
    ├── index/              # Vector index (HNSW algorithm)
    └── data/               # Metadata storage
```

**Per-Document Storage:**

```python
{
  "id": "550e8400-e29b-41d4-a716-446655440000",  # UUID generated at indexing
  "embedding": [0.1234, -0.5678, ..., 0.9999],   # 768 float32 values
  "metadata": {
    "verse_id": "1:1",
    "surah_name": "Al-Fatihah",
    "juz": 1,
    "page": 1,
    "revelation_place": "makkah",
    "arabic_text": "بِسْمِ ٱللَّهِ...",
    "surah_number": 1,
    "verse_number": 1
  },
  "document": "search_document: === Verse 1:1 - Al-Fatihah ===\n\nArabic:\nبِسْمِ ٱللَّهِ...",
  "upsert_at": 1704067200  # Timestamp
}
```

#### 3. **Indexing Code**

```python
# From rag_pipeline.py
def add_documents(self, documents: list[Document]) -> list[str]:
    """Add documents to vector store."""
    total = len(documents)
    
    # Add document prefix if needed
    if self._needs_prefix():
        for doc in documents:
            doc.page_content = self._add_document_prefix(doc.page_content)
    
    # Generate UUIDs
    uuids = [str(uuid4()) for _ in range(total)]
    
    # Add to ChromaDB with embeddings
    ids = self.vectorstore.add_documents(
        documents=documents, 
        ids=uuids
    )
    
    logger.info(f"Added {len(ids)} documents")
    return ids
```

**What happens internally:**

1. LangChain creates `Document` objects with `page_content` and `metadata`
2. Each document prefix is added: `"search_document: " + original_text`
3. OllamaEmbeddings generates 768-dimensional vectors
4. ChromaDB stores: `(uuid, embedding, metadata, prefixed_content)`

#### 4. **Embedding Dimensions**

- **Model**: `nomic-embed-text-v2-moe`
- **Dimensions**: 768
- **Parameters**: 305M active (Mixture of Experts)
- **VRAM Usage**: ~1-2GB for embeddings
- **Speed**: ~500 docs/minute (RTX 3080)

---

## Semantic Similarity & Retrieval

### 1. Query Processing

```python
# From rag_pipeline.py - query() method
def query(self, question: str, return_sources: bool = True) -> dict:
    """
    Query the RAG pipeline.
    """
    # Step 1: Add query prefix
    prefixed_query = self._add_query_prefix(question)
    # Result: "search_query: What is Bismillah?"
    
    # Step 2: Retrieve similar documents
    results_with_scores = self.similarity_search_with_score(
        prefixed_query, 
        k=config.TOP_K  # Default: 5
    )
    
    # results_with_scores = [
    #   (Document(verse 1:1), 0.8932),
    #   (Document(verse 1:2), 0.7654),
    #   (Document(verse 109:1), 0.6543),
    #   ...
    # ]
```

### 2. Similarity Search Details

```python
# ChromaDB similarity_search_with_score internally:
def similarity_search_with_score(self, query: str, k: int) -> list[tuple]:
    """
    1. Encode query to 768-dim vector
    2. Compare against all stored embeddings using COSINE SIMILARITY
    3. Return top-k by similarity score
    """
    # Cosine similarity formula:
    # similarity = (query_embedding · doc_embedding) / 
    #              (||query_embedding|| * ||doc_embedding||)
    # Result: score between 0 and 1 (higher = more similar)
```

### 3. Semantic Similarity Scoring

**Score Interpretation:**

| Score Range | Interpretation | Typical Use |
|------------|---|---|
| 0.9 - 1.0 | Nearly identical | Direct answers |
| 0.8 - 0.9 | Very similar | Highly relevant |
| 0.7 - 0.8 | Similar | Related concepts |
| 0.6 - 0.7 | Somewhat similar | Tangential content |
| < 0.6 | Weakly similar | Possible noise |

**Configuration Options:**

```python
# From config.py

# Top K documents to retrieve
TOP_K = 5  # Default: retrieve 5 most similar

# Search type
SEARCH_TYPE = "similarity"  # or "mmr" (Maximal Marginal Relevance)

# Relevance filtering
MIN_RELEVANCE_SCORE = 0.0  # Filter documents below this threshold

# MMR settings (for diversity)
MMR_LAMBDA = 0.5  # 0 = maximize diversity, 1 = maximize relevance
```

### 4. Retrieval Example

**User Query:**
```
"What is the meaning of Bismillah?"
```

**Processing:**
```
1. Add prefix: "search_query: What is the meaning of Bismillah?"

2. Generate embedding: [0.245, -0.156, ..., 0.789]  # 768 dimensions

3. Calculate cosine similarity with ALL stored documents

4. Retrieved documents (sorted by similarity):
   - Verse 1:1 (Bismillah) - score: 0.8932
   - Verse 1:2 (Al-Hamd) - score: 0.7654
   - Verse 109:1 - score: 0.6543
   - Verse 1:3 - score: 0.5432
   - Verse 24:35 (Ayat al-Nur) - score: 0.4321

5. Context concatenated from top documents:
   "\n\n".join([doc.page_content for doc in retrieved_docs])
```

---

## Query Execution & Field Access

### 1. Complete Query Flow Diagram

```
Question: "What is Bismillah?"
     ↓
[RETRIEVAL PHASE]
     ↓
ChromaDB returns:
[
  Document {
    page_content: "=== Verse 1:1 ===\nArabic: بِسْمِ ٱللَّهِ...",
    metadata: {
      verse_id: "1:1",
      surah_name: "Al-Fatihah",
      juz: 1,
      page: 1,
      arabic_text: "بِسْمِ ٱللَّهِ...",
      ...
    }
  },
  ...more documents
]
     ↓
[LLM PROMPT BUILDING]
     ↓
RAG_PROMPT_TEMPLATE:
"Context:
{context}

Question: {question}

Answer based on context..."
     ↓
[LLM GENERATION]
     ↓
Ollama generates answer using retrieved context
     ↓
Output with sources
```

### 2. Field Access on Query Hit

**What fields are accessible when you retrieve a document:**

#### Fields Always Available:

```python
document = retrieved_documents[0]

# ✅ Accessible fields:
document.page_content          # Full formatted text (used in embedding)
document.metadata              # Complete metadata object

# From metadata:
document.metadata["verse_id"]          # "1:1"
document.metadata["surah_name"]        # "Al-Fatihah"
document.metadata["juz"]               # 1
document.metadata["page"]              # 1
document.metadata["revelation_place"]  # "makkah"
document.metadata["arabic_text"]       # Full Arabic text
document.metadata["surah_number"]      # 1
document.metadata["verse_number"]      # 1
```

#### Fields NOT Directly Accessible:

```python
# ❌ NOT accessible from retrieved Document:
document.translations         # NOT in metadata
document.tafsirs             # NOT in metadata
document.footnotes           # NOT in metadata

# Why? These are embedded WITHIN page_content, not stored separately
```

### 3. How to Extract Full Verse Data

**If you need the original translations, tafsirs, and footnotes:**

```python
# OPTION 1: Parse from page_content (crude)
import re

page_content = document.page_content
# Extract sections manually with regex

# OPTION 2: Load original chunk file and search by verse_id (better)
verse_id = document.metadata["verse_id"]
chunk = find_chunk_by_id("fatiha.chunks.jsonl", verse_id)
# chunk["translations"]  ✅ accessible
# chunk["tafsirs"]       ✅ accessible
# chunk["footnotes"]     ✅ accessible

# OPTION 3: Modify document conversion to include ALL fields
def create_documents_from_chunks(chunks: list[dict]) -> list[Document]:
    documents = []
    for chunk in chunks:
        content = chunk.get("text", "")
        metadata = chunk.get("metadata", {}).copy()
        
        # STORE additional fields in metadata
        metadata["translations"] = json.dumps(chunk.get("translations", {}))
        metadata["tafsirs"] = json.dumps(chunk.get("tafsirs", {}))
        metadata["footnotes"] = json.dumps(chunk.get("footnotes", {}))
        
        documents.append(Document(
            page_content=content,
            metadata=metadata,
        ))
    return documents
```

### 4. Retrieved Document Structure

**Complete structure of a retrieved document:**

```python
retrieved_doc = result["source_documents"][0]

print(retrieved_doc.page_content)
# Output:
# === Verse 1:1 - Al-Fatihah (الفاتحة) ===
# 
# Arabic:
# بِسْمِ ٱللَّهِ ٱلرَّحْمَـٰنِ ٱلرَّحِيمِ
# 
# Translation:
#   [Saheeh International] In the name of Allah...
#   [M.A.S. Abdel Haleem] In the name of God...
# 
# Tafsir (Ibn Kathir (Abridged)):
# Introduction to Fatihah Which was revealed in Makkah...

print(retrieved_doc.metadata)
# Output:
# {
#   'verse_id': '1:1',
#   'surah_number': 1,
#   'verse_number': 1,
#   'surah_name': 'Al-Fatihah',
#   'surah_name_arabic': 'الفاتحة',
#   'juz': 1,
#   'hizb': 1,
#   'page': 1,
#   'revelation_place': 'makkah',
#   'arabic_text': 'بِسْمِ ٱللَّهِ ٱلرَّحْمَـٰنِ ٱلرَّحِيمِ'
# }

# Access scores
scores = result["scores"]  # [0.8932, 0.7654, ...]
```

### 5. Chat UI Debug Output

The web UI shows **real-time debug logs** of each retrieval step:

```
[14:32:15.240] [QUERY] User question: What is Bismillah?
[14:32:15.241] [RETRIEVAL] Searching for top 5 similar documents...
[14:32:15.352] [RETRIEVED_DOCS] Found 5 documents:
  [1] Score: 0.8932 | Verse 1:1 (Al-Fatihah)
      بِسْمِ ٱللَّهِ ٱلرَّحْمَـٰنِ ٱلرَّحِيمِ...
  [2] Score: 0.7654 | Verse 1:2 (Al-Fatihah)
      ٱلْحَمْدُ لِلَّهِ رَبِّ ٱلْعَـٰلَمِينَ...
  [3] Score: 0.6543 | Verse 109:1
      ...
[14:32:15.360] [CONTEXT] Built context (2847 chars)
[14:32:15.361] [LLM_CALL] Invoking gemma3:4b...
[14:32:18.542] [LLM_RESPONSE] Response (450 chars):
  Bismillah (بِسْمِ ٱللَّهِ) means "In the name of Allah"...
```

---

## Code Examples

### Example 1: Index Chunks

```python
#!/usr/bin/env python3
"""Index chunks into ChromaDB"""

from rag.rag_pipeline import TazkiyahRAG, create_documents_from_chunks
import json

# Load chunks from JSONL
chunks = []
with open("fatiha.chunks.jsonl") as f:
    for line in f:
        chunks.append(json.loads(line))

# Convert to LangChain Documents
documents = create_documents_from_chunks(chunks)

# Initialize RAG pipeline
rag = TazkiyahRAG()

# Clear existing collection
rag.clear_collection()

# Add documents in batches
batch_size = 50
for i in range(0, len(documents), batch_size):
    batch = documents[i:i+batch_size]
    ids = rag.add_documents(batch)
    print(f"Indexed {len(ids)} documents")

# Get stats
stats = rag.get_collection_stats()
print(f"Total indexed: {stats['count']}")
```

### Example 2: Query with Source Retrieval

```python
#!/usr/bin/env python3
"""Query RAG and display results with sources"""

from rag.rag_pipeline import TazkiyahRAG

rag = TazkiyahRAG()

question = "What is the significance of Bismillah?"

# Query with sources
result = rag.query(question, return_sources=True)

# Display answer
print("ANSWER:")
print(result["result"])
print("\n" + "="*50)

# Display sources
print("\nSOURCES:")
for i, doc in enumerate(result["source_documents"], 1):
    score = result["scores"][i-1]
    verse_id = doc.metadata.get("verse_id", "?")
    surah = doc.metadata.get("surah_name", "")
    
    print(f"\n[{i}] Verse {verse_id} ({surah}) - Score: {score:.4f}")
    print(f"    {doc.page_content[:200]}...")
```

### Example 3: Similarity Search with Detailed Scores

```python
#!/usr/bin/env python3
"""Show detailed similarity scores for debugging"""

from rag.rag_pipeline import TazkiyahRAG

rag = TazkiyahRAG()

question = "Mercy of Allah"

# Search with scores
results = rag.similarity_search_with_score(question, k=10)

print(f"Top 10 results for: '{question}'\n")
print("Score  | Verse ID | Surah Name        | Preview")
print("-------|----------|-------------------|------------------------------------------")

for doc, score in results:
    verse_id = doc.metadata.get("verse_id", "?")
    surah = doc.metadata.get("surah_name", "")[:15]
    preview = doc.page_content[:40].replace("\n", " ")
    
    print(f"{score:.4f} | {verse_id:>8} | {surah:<17} | {preview}")
```

### Example 4: Chat Interface

```python
#!/usr/bin/env python3
"""Terminal chat with debug logging"""

from rag.rag_pipeline import TazkiyahRAG
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel

console = Console()
rag = TazkiyahRAG()

console.print("[bold cyan]Tazkiyah Chat[/bold cyan]")
console.print("[dim]Type 'quit' to exit\n[/dim]")

while True:
    question = Prompt.ask("[blue]You[/blue]")
    
    if question.lower() in ("quit", "exit"):
        break
    
    # Define debug callback
    debug_lines = []
    def debug_callback(step, data):
        debug_lines.append(f"[{step}] {data[:100]}...")
    
    # Query with debug
    result = rag.query(question, return_sources=False, debug_callback=debug_callback)
    
    # Show answer
    console.print(Panel(result["result"], title="Tazkiyah", border_style="green"))
    
    # Show debug (optional)
    if False:  # Set to True to show debug logs
        console.print("\n[dim]Debug logs:[/dim]")
        for line in debug_lines:
            console.print(f"[dim]{line}[/dim]")
```

### Example 5: Custom Metadata Filtering

```python
#!/usr/bin/env python3
"""Retrieve documents from specific surahs only"""

from rag.rag_pipeline import TazkiyahRAG

rag = TazkiyahRAG()

# Get all documents (simulate filtering)
all_docs = rag.similarity_search(
    query="mercy",
    k=100  # Get many results to filter
)

# Filter by surah
target_surah = "Al-Fatiha"
filtered = [
    doc for doc in all_docs 
    if doc.metadata.get("surah_name") == target_surah
]

print(f"Found {len(filtered)} verses in {target_surah}")
for doc in filtered[:3]:
    print(f"  - Verse {doc.metadata['verse_id']}")
```

---

## Architectural Diagram

### Complete System Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                    TAZKIYAH RAG SYSTEM                         │
└────────────────────────────────────────────────────────────────┘

                        ┌─────────────────┐
                        │  USER QUERIES   │
                        └────────┬────────┘
                                 │
                ┌────────────────┼────────────────┐
                │                │                │
        ┌───────▼────────┐ ┌────▼────────┐ ┌────▼────────┐
        │ Terminal Chat  │ │  Web UI     │ │ Query CLI   │
        │ (chat.py)      │ │ (chat_ui.py)│ │(query_rag.py)
        └────────┬───────┘ └────┬────────┘ └────┬────────┘
                 │             │               │
                 └─────────────┬───────────────┘
                               │
                    ┌──────────▼───────────┐
                    │  TazkiyahRAG.query() │
                    └──────────┬───────────┘
                               │
                ┌──────────────┼──────────────┐
                │              │              │
        ┌───────▼────────┐ ┌──▼──────────┐ ┌▼───────────┐
        │ ADD PREFIXES   │ │ EMBEDDINGS  │ │ CHROMADB   │
        │ "search_query" │ │ (Ollama)    │ │ RETRIEVAL  │
        │                │ │             │ │            │
        │ Prefixed Query │ │ 768-dims    │ │ Top-K      │
        │ +embedding     │ │ vectors     │ │ documents  │
        └────────┬───────┘ └──┬──────────┘ └┬───────────┘
                 │            │             │
                 └────────────┬─────────────┘
                              │
                ┌─────────────▼──────────────┐
                │  BUILD LLM PROMPT         │
                │  - Format context         │
                │  - Insert question        │
                │  - Apply RAG template     │
                └─────────────┬──────────────┘
                              │
                ┌─────────────▼──────────────┐
                │  LLM GENERATION           │
                │  (Ollama Model)           │
                │  - gemma3:4b (default)    │
                │  - Temperature: 0.3       │
                │  - Max tokens: 1024       │
                └─────────────┬──────────────┘
                              │
                ┌─────────────▼──────────────┐
                │  POST-PROCESSING          │
                │  - Parse response         │
                │  - Add source references  │
                │  - Format output          │
                └─────────────┬──────────────┘
                              │
                    ┌─────────▼─────────┐
                    │  USER OUTPUT      │
                    │  - AI Answer      │
                    │  - Source verses  │
                    │  - Similarity     │
                    │    scores         │
                    └───────────────────┘

┌────────────────────────────────────────────────────────────────┐
│                    DATA FLOW DURING INDEXING                   │
└────────────────────────────────────────────────────────────────┘

fatiha.chunks.jsonl (JSONL file)
         │
         ├─ Load chunk → { id, text, metadata, translations, ... }
         │
         ├─ Create LangChain Document
         │  ├─ page_content: formatted "text" field
         │  └─ metadata: { verse_id, surah_name, juz, page, ... }
         │
         ├─ Add prefix
         │  └─ page_content = "search_document: " + page_content
         │
         ├─ Generate embedding (nomic-embed-text-v2-moe)
         │  └─ 768-dimensional vector
         │
         └─ Store in ChromaDB
            ├─ id: UUID
            ├─ embedding: [768 floats]
            ├─ metadata: { verse_id, surah_name, ... }
            └─ document: prefixed page_content

┌────────────────────────────────────────────────────────────────┐
│                  CONFIGURATION TUNING                          │
└────────────────────────────────────────────────────────────────┘

# rag/config.py

# Retrieval Parameters
TOP_K = 5                           # Documents per query
SEARCH_TYPE = "similarity"          # or "mmr"
MIN_RELEVANCE_SCORE = 0.0          # Filter threshold

# Embedding Model
EMBEDDING_MODEL = "nomic-embed-text-v2-moe"  # 768-dim
EMBED_QUERY_PREFIX = "search_query: "
EMBED_DOCUMENT_PREFIX = "search_document: "

# LLM Generation
LLM_MODEL = "gemma3:4b"             # Default model
LLM_TEMPERATURE = 0.3               # 0=factual, 1=creative
LLM_MAX_TOKENS = 1024               # Response length
LLM_TOP_P = 0.9                     # Nucleus sampling
LLM_REPEAT_PENALTY = 1.1            # Avoid repetition

# Vector Store
CHROMA_PERSIST_DIR = "rag/chroma_db"
COLLECTION_NAME = "quran_verses"
```

---

## Summary Table

| Aspect | Details |
|--------|---------|
| **Chunks Source** | JSONL files with id, text, metadata, translations, tafsirs, footnotes |
| **Embedding Model** | nomic-embed-text-v2-moe (768-dim) |
| **Vector Database** | ChromaDB (persisted) |
| **Similarity Metric** | Cosine similarity (0 to 1) |
| **Semantic Fields** | Full formatted text with Arabic, translations, tafsir |
| **Retrieved Fields** | page_content (complete text) + metadata (verse info) |
| **Query Prefixes** | "search_query: " for questions, "search_document: " for chunks |
| **LLM Models** | Ollama (gemma3:4b, llama3.1:8b, qwen3:8b, etc.) |
| **UI Options** | Terminal chat, Web UI (Gradio 6.0), CLI query |
| **Chain Pattern** | LangChain: prompt \| llm \| StrOutputParser() |
| **Top-K Default** | 5 documents per query |
| **Score Interpretation** | Higher = more similar (range: 0-1) |

---

## Next Steps

1. **Tune `TOP_K`**: Adjust from 5 to 3-10 based on context needs
2. **Change LLM**: Modify `LLM_MODEL` for different reasoning/speed tradeoffs
3. **Adjust Temperature**: Set `LLM_TEMPERATURE` based on query type
4. **Add Custom Fields**: Modify `create_documents_from_chunks()` to store additional metadata
5. **Filter Results**: Implement `MIN_RELEVANCE_SCORE` filtering for confidence thresholds

For questions or extensions, refer to [rag/README.md](rag/README.md).
