#!/usr/bin/env python3
"""
Index Chunks - CLI to index JSONL chunks into ChromaDB

Usage:
    python -m rag.index_chunks fatiha.chunks.jsonl
    python -m rag.index_chunks --clear fatiha.chunks.jsonl
"""
import json
import sys
import logging
from pathlib import Path

import click
from rich.console import Console
from rich.progress import Progress, TextColumn, BarColumn, TaskProgressColumn, TimeElapsedColumn

from rag.rag_pipeline import TazkiyahRAG, create_documents_from_chunks
from rag import config

console = Console()
logger = logging.getLogger(__name__)


def load_chunks(filepath: Path) -> list[dict]:
    """Load chunks from JSONL file."""
    chunks = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                chunks.append(json.loads(line))
    return chunks


@click.command()
@click.argument("chunks_file", type=click.Path(exists=True, path_type=Path))
@click.option("--clear", is_flag=True, help="Clear existing collection before indexing")
@click.option("--batch-size", default=100, help="Number of documents per batch")
def main(chunks_file: Path, clear: bool, batch_size: int):
    """
    Index JSONL chunks into ChromaDB vector store.
    
    CHUNKS_FILE: Path to .chunks.jsonl file
    """
    console.print("\n[bold cyan]Tazkiyah RAG Indexer[/bold cyan]\n")
    
    # Initialize RAG
    console.print(f"[dim]Embedding model: {config.EMBEDDING_MODEL}[/dim]")
    console.print(f"[dim]Vector store: {config.CHROMA_PERSIST_DIR}[/dim]\n")
    
    rag = TazkiyahRAG()
    
    # Clear if requested
    if clear:
        console.print("[yellow]Clearing existing collection...[/yellow]")
        rag.clear_collection()
        console.print("[green]Collection cleared[/green]\n")
    
    # Load chunks
    console.print(f"[cyan]Loading chunks from:[/cyan] {chunks_file}")
    chunks = load_chunks(chunks_file)
    console.print(f"[green]Loaded {len(chunks)} chunks[/green]\n")
    
    if not chunks:
        console.print("[red]No chunks found![/red]")
        sys.exit(1)
    
    # Convert to Documents
    console.print("[cyan]Converting to LangChain Documents...[/cyan]")
    documents = create_documents_from_chunks(chunks)
    console.print(f"[green]Created {len(documents)} documents[/green]\n")
    
    # Index in batches with progress
    console.print("[cyan]Indexing documents...[/cyan]")
    
    with Progress(
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Indexing", total=len(documents))
        
        total_indexed = 0
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]
            ids = rag.add_documents(batch)
            total_indexed += len(ids)
            progress.update(task, advance=len(batch))
    
    # Report stats
    console.print()
    stats = rag.get_collection_stats()
    console.print("[bold green]Indexing complete![/bold green]")
    console.print(f"  [dim]Collection:[/dim] {stats['name']}")
    console.print(f"  [dim]Documents:[/dim] {stats['count']}")
    console.print(f"  [dim]Persisted to:[/dim] {stats['persist_directory']}")
    console.print()


if __name__ == "__main__":
    main()
