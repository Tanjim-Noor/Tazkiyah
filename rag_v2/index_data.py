#!/usr/bin/env python3
"""
Tazkiyah RAG v2 - Index

Loads quran_full_rag_v2.json directly and indexes into ChromaDB.

Usage:
    python -m rag_v2.index_data
    python -m rag_v2.index_data --clear
    python -m rag_v2.index_data --data-file path/to/quran.json
"""
import sys
import logging

import click
from rich.console import Console
from rich.progress import (
    Progress,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
    TimeElapsedColumn,
)

from rag_v2 import config
from rag_v2.data_loader import load_and_create_documents
from rag_v2.rag_pipeline import TazkiyahRAGv2

console = Console()
logger = logging.getLogger(__name__)


@click.command()
@click.option(
    "--data-file",
    type=click.Path(exists=True),
    default=None,
    help=f"Path to Quran JSON. Default: {config.DATA_FILE}",
)
@click.option("--clear", is_flag=True, help="Clear existing collection before indexing")
@click.option("--batch-size", default=100, help="Documents per batch (default: 100)")
@click.option("--max-content-length", default=3000, help="Max chars per document (default: 3000)")
@click.option("--no-commentary", is_flag=True, help="Exclude commentary from indexed text")
def main(data_file, clear: bool, batch_size: int, max_content_length: int, no_commentary: bool):
    """Index quran_full_rag_v2.json into ChromaDB for RAG v2."""

    console.print("\n[bold cyan]Tazkiyah RAG v2 — Indexer[/bold cyan]\n")
    console.print(f"  [dim]Embedding model:[/dim] {config.EMBEDDING_MODEL}")
    console.print(f"  [dim]LLM model:[/dim]       {config.LLM_MODEL}")
    console.print(f"  [dim]Vector store:[/dim]     {config.CHROMA_PERSIST_DIR}")
    console.print(f"  [dim]Collection:[/dim]       {config.COLLECTION_NAME}")

    langsmith_on = (
        config.LANGSMITH_TRACING.lower() == "true" and config.LANGSMITH_API_KEY
    )
    console.print(
        f"  [dim]LangSmith:[/dim]        {'[green]ON[/green]' if langsmith_on else '[yellow]OFF[/yellow]'}"
    )
    console.print()

    # Initialize RAG pipeline
    rag = TazkiyahRAGv2()

    # Clear if requested
    if clear:
        console.print("[yellow]Clearing existing collection...[/yellow]")
        rag.clear_collection()
        console.print("[green]Collection cleared.[/green]\n")

    # Load data
    from pathlib import Path

    data_path = Path(data_file) if data_file else config.DATA_FILE
    console.print(f"[cyan]Loading data from:[/cyan] {data_path}")

    documents = load_and_create_documents(
        filepath=data_path,
        include_commentary=not no_commentary,
        max_content_length=max_content_length,
    )
    console.print(f"[green]Created {len(documents)} documents[/green]")
    console.print(
        f"  [dim]Content: translation_clean"
        f"{' + commentary_clean' if not no_commentary else ''}[/dim]"
    )
    console.print(f"  [dim]Max length: {max_content_length} chars[/dim]\n")

    if not documents:
        console.print("[red]No documents created! Check data file.[/red]")
        sys.exit(1)

    # Index in batches
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
            batch = documents[i : i + batch_size]
            ids = rag.add_documents(batch)
            total_indexed += len(ids)
            progress.update(task, advance=len(batch))

    # Report stats
    console.print()
    stats = rag.get_collection_stats()
    console.print("[bold green]Indexing complete![/bold green]")
    console.print(f"  [dim]Collection:[/dim]  {stats['name']}")
    console.print(f"  [dim]Documents:[/dim]   {stats['count']}")
    console.print(f"  [dim]Embedding:[/dim]   {stats['embedding_model']}")
    console.print(f"  [dim]Persisted:[/dim]   {stats['persist_directory']}")
    console.print()


if __name__ == "__main__":
    main()
