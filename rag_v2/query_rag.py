#!/usr/bin/env python3
"""
Tazkiyah RAG v2 - CLI Query

Usage:
    python -m rag_v2.query_rag "What is the meaning of Bismillah?"
    python -m rag_v2.query_rag --no-sources "Explain Al-Fatiha"
    python -m rag_v2.query_rag --top-k 10 "What does the Quran say about patience?"
"""
import sys
import logging

import click
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from rag_v2 import config
from rag_v2.rag_pipeline import TazkiyahRAGv2

console = Console()
logger = logging.getLogger(__name__)


@click.command()
@click.argument("question", type=str)
@click.option("--sources/--no-sources", default=True, help="Show source documents")
@click.option("--top-k", default=config.TOP_K, help="Number of documents to retrieve")
def main(question: str, sources: bool, top_k: int):
    """Query the Tazkiyah RAG v2 pipeline."""

    console.print("\n[bold cyan]Tazkiyah RAG v2 — Query[/bold cyan]\n")

    # Initialize
    rag = TazkiyahRAGv2()

    stats = rag.get_collection_stats()
    if stats["count"] == 0:
        console.print("[red]No documents indexed![/red]")
        console.print("[dim]Run: python -m rag_v2.index_data[/dim]")
        sys.exit(1)

    console.print(
        f"[dim]Collection: {stats['name']} ({stats['count']} docs) | "
        f"LLM: {stats['llm_model']}[/dim]\n"
    )

    # Show question
    console.print(Panel(question, title="Question", border_style="blue"))
    console.print()

    # Query
    console.print("[cyan]Querying...[/cyan]\n")

    # Temporarily override top_k
    original_top_k = config.TOP_K
    config.TOP_K = top_k

    result = rag.query(question, return_sources=sources)

    config.TOP_K = original_top_k

    # Show answer
    console.print(
        Panel(
            Markdown(result["result"]),
            title="Answer",
            border_style="green",
        )
    )

    # Show sources
    if sources and "source_documents" in result:
        console.print("\n[bold]Sources:[/bold]")
        scores = result.get("scores", [])
        for i, doc in enumerate(result["source_documents"], 1):
            meta = doc.metadata
            verse_key = meta.get("verse_key", "?")
            surah = meta.get("surah_name", "")
            score = scores[i - 1] if i - 1 < len(scores) else 0

            console.print(
                f"\n  [cyan]{i}. Verse {verse_key}[/cyan] ({surah}) "
                f"[dim]score: {score:.4f}[/dim]"
            )

            content = doc.page_content
            if len(content) > 200:
                content = content[:200] + "..."
            console.print(f"     [dim]{content}[/dim]")

    console.print()


if __name__ == "__main__":
    main()
