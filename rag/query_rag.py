#!/usr/bin/env python3
"""
Query RAG - CLI to query the Tazkiyah RAG pipeline

Usage:
    python -m rag.query_rag "What is the meaning of Bismillah?"
    python -m rag.query_rag --no-sources "Explain Al-Fatiha"
"""
import sys
import logging

import click
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from rag.rag_pipeline import TazkiyahRAG
from rag import config

console = Console()
logger = logging.getLogger(__name__)


@click.command()
@click.argument("question", type=str)
@click.option("--sources/--no-sources", default=True, help="Show source documents")
@click.option("--top-k", default=config.TOP_K, help="Number of documents to retrieve")
def main(question: str, sources: bool, top_k: int):
    """
    Query the Tazkiyah RAG pipeline.
    
    QUESTION: Your question about the Quran
    """
    console.print("\n[bold cyan]Tazkiyah RAG Query[/bold cyan]\n")
    
    # Initialize RAG
    rag = TazkiyahRAG()
    
    # Check collection
    stats = rag.get_collection_stats()
    if stats["count"] == 0:
        console.print("[red]Error: No documents indexed![/red]")
        console.print("[dim]Run: python -m rag.index_chunks <chunks.jsonl>[/dim]")
        sys.exit(1)
    
    console.print(f"[dim]Collection: {stats['name']} ({stats['count']} docs)[/dim]\n")
    
    # Show question
    console.print(Panel(question, title="Question", border_style="blue"))
    console.print()
    
    # Query
    console.print("[cyan]Querying...[/cyan]\n")
    result = rag.query(question, return_sources=sources)
    
    # Show answer
    console.print(Panel(
        Markdown(result["result"]),
        title="Answer",
        border_style="green",
    ))
    
    # Show sources if requested
    if sources and "source_documents" in result:
        console.print("\n[bold]Sources:[/bold]")
        for i, doc in enumerate(result["source_documents"], 1):
            meta = doc.metadata
            verse_key = meta.get("verse_key", "?")
            surah = meta.get("surah_name", "")
            
            console.print(f"\n  [cyan]{i}. Verse {verse_key}[/cyan] ({surah})")
            
            # Show snippet of content
            content = doc.page_content
            if len(content) > 200:
                content = content[:200] + "..."
            console.print(f"     [dim]{content}[/dim]")
    
    console.print()


if __name__ == "__main__":
    main()
