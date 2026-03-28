#!/usr/bin/env python3
"""
Tazkiyah RAG v2 - Vector store builder.

Builds a Chroma vector store into a model-specific directory so each embedding
model gets its own reusable store.
"""
from __future__ import annotations

import logging
from pathlib import Path

import click
from rich.console import Console
from rich.progress import BarColumn, Progress, TaskProgressColumn, TextColumn, TimeElapsedColumn

from tools.python.rag_v2 import config
from tools.python.rag_v2.data_loader import load_and_create_documents
from tools.python.rag_v2.rag_pipeline import TazkiyahRAGv2
from tools.python.rag_v2.vectorstore_paths import get_vectorstore_persist_directory


console = Console()
logger = logging.getLogger(__name__)


def _resolve_persist_directory(
    embedding_provider: str,
    embedding_model: str,
    collection_name: str,
    persist_directory: str | None,
    vectorstore_root: str | None,
) -> Path:
    if persist_directory:
        return Path(persist_directory).expanduser().resolve()

    root_dir = Path(vectorstore_root).expanduser().resolve() if vectorstore_root else None
    return get_vectorstore_persist_directory(
        embedding_provider=embedding_provider,
        embedding_model=embedding_model,
        collection_name=collection_name,
        root_dir=root_dir,
    )


@click.command()
@click.option("--data-file", type=click.Path(exists=True), default=None, help=f"Path to Quran JSON. Default: {config.DATA_FILE}")
@click.option("--embedding-model", default=config.EMBEDDING_MODEL, show_default=True, help="Embedding model to index with")
@click.option("--embedding-provider", default=config.EMBEDDING_PROVIDER, show_default=True, help="Embedding provider used to derive the store path")
@click.option("--collection-name", default=config.COLLECTION_NAME, show_default=True, help="Chroma collection name")
@click.option("--vectorstore-root", default=str(config.VECTORSTORE_ROOT_DIR), show_default=True, help="Root directory for model-specific vector stores")
@click.option("--persist-directory", default=None, help="Override the resolved vector store directory")
@click.option("--clear", is_flag=True, help="Clear existing collection before indexing")
@click.option("--rebuild", is_flag=True, help="Force a rebuild even if the vector store already exists")
@click.option("--batch-size", default=100, show_default=True, help="Documents per batch")
@click.option("--no-commentary", is_flag=True, help="Exclude commentary from indexed text")
def main(
    data_file: str | None,
    embedding_model: str,
    embedding_provider: str,
    collection_name: str,
    vectorstore_root: str,
    persist_directory: str | None,
    clear: bool,
    rebuild: bool,
    batch_size: int,
    no_commentary: bool,
) -> int:
    """Build a Chroma vector store for the active embedding model."""

    resolved_persist_dir = _resolve_persist_directory(
        embedding_provider=embedding_provider,
        embedding_model=embedding_model,
        collection_name=collection_name,
        persist_directory=persist_directory,
        vectorstore_root=vectorstore_root,
    )

    console.print("\n[bold cyan]Tazkiyah RAG v2 — Vector Store Builder[/bold cyan]\n")
    console.print(f"  [dim]Embedding provider:[/dim] {embedding_provider}")
    console.print(f"  [dim]Embedding model:[/dim]    {embedding_model}")
    console.print(f"  [dim]Vector store root:[/dim]   {vectorstore_root}")
    console.print(f"  [dim]Persist directory:[/dim]   {resolved_persist_dir}")
    console.print(f"  [dim]Collection:[/dim]         {collection_name}")

    langsmith_on = config.LANGSMITH_TRACING.lower() == "true" and config.LANGSMITH_API_KEY
    console.print(f"  [dim]LangSmith:[/dim]          {'[green]ON[/green]' if langsmith_on else '[yellow]OFF[/yellow]'}")
    console.print()

    rag = TazkiyahRAGv2(
        embedding_model=embedding_model,
        collection_name=collection_name,
        persist_directory=resolved_persist_dir,
    )

    stats = rag.get_collection_stats()
    if stats["count"] > 0 and not rebuild and not clear:
        console.print("[green]Vector store already exists; skipping rebuild.[/green]")
        console.print(f"  [dim]Documents:[/dim] {stats['count']}")
        console.print(f"  [dim]Path:[/dim]       {stats['persist_directory']}")
        console.print()
        return 0

    if clear or rebuild:
        console.print("[yellow]Clearing existing collection...[/yellow]")
        rag.clear_collection()
        console.print("[green]Collection cleared.[/green]\n")

    data_path = Path(data_file) if data_file else config.DATA_FILE
    console.print(f"[cyan]Loading data from:[/cyan] {data_path}")

    documents = load_and_create_documents(
        filepath=data_path,
        include_commentary=not no_commentary,
    )
    console.print(f"[green]Created {len(documents)} documents[/green]")
    console.print(f"  [dim]Content: translation_clean{' + commentary_clean' if not no_commentary else ''}[/dim]")
    console.print()

    if not documents:
        console.print("[red]No documents created. Check the data file.[/red]")
        return 1

    console.print("[cyan]Indexing documents...[/cyan]")
    with Progress(
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Indexing", total=len(documents))

        for i in range(0, len(documents), batch_size):
            batch = documents[i : i + batch_size]
            rag.add_documents(batch)
            progress.update(task, advance=len(batch))

    stats = rag.get_collection_stats()
    console.print()
    console.print("[bold green]Indexing complete![/bold green]")
    console.print(f"  [dim]Collection:[/dim]  {stats['name']}")
    console.print(f"  [dim]Documents:[/dim]   {stats['count']}")
    console.print(f"  [dim]Embedding:[/dim]   {stats['embedding_model']}")
    console.print(f"  [dim]Persisted:[/dim]   {stats['persist_directory']}")
    console.print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())