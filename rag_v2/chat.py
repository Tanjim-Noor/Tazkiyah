#!/usr/bin/env python3
"""
Tazkiyah RAG v2 - Terminal Chat

Interactive REPL chat interface.

Usage:
    python -m rag_v2.chat
"""
import sys
import logging

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt

from rag_v2 import config
from rag_v2.rag_pipeline import TazkiyahRAGv2

console = Console()
logger = logging.getLogger(__name__)


def main():
    """Interactive terminal chat with Tazkiyah RAG v2."""

    console.print("\n[bold cyan]Tazkiyah Chat v2[/bold cyan]")
    console.print("[dim]Quranic knowledge assistant — LangChain + Ollama + LangSmith[/dim]")
    console.print(f"[dim]LLM: {config.LLM_MODEL} | Embedding: {config.EMBEDDING_MODEL}[/dim]")

    langsmith_on = (
        config.LANGSMITH_TRACING.lower() == "true" and config.LANGSMITH_API_KEY
    )
    console.print(
        f"[dim]LangSmith: {'ON (' + config.LANGSMITH_PROJECT + ')' if langsmith_on else 'OFF'}[/dim]"
    )
    console.print("[dim]Type 'quit' or 'exit' to leave[/dim]\n")

    # Initialize
    rag = TazkiyahRAGv2()

    stats = rag.get_collection_stats()
    if stats["count"] == 0:
        console.print("[red]No documents indexed![/red]")
        console.print("[dim]Run: python -m rag_v2.index_data[/dim]")
        sys.exit(1)

    console.print(f"[dim]Connected: {stats['count']} documents indexed[/dim]\n")
    console.print("-" * 50)
    console.print()

    # Chat loop
    while True:
        try:
            question = Prompt.ask("[bold blue]You[/bold blue]")

            if not question.strip():
                continue

            if question.strip().lower() in ("quit", "exit", "q"):
                console.print("\n[dim]Ma'a salama![/dim]\n")
                break

            console.print()
            with console.status("[cyan]Thinking...[/cyan]"):
                result = rag.query(question, return_sources=False)

            console.print("[bold green]Tazkiyah[/bold green]:")
            console.print(Markdown(result["result"]))
            console.print()

        except KeyboardInterrupt:
            console.print("\n\n[dim]Interrupted. Goodbye![/dim]\n")
            break
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]\n")
            logger.exception("Chat error")


if __name__ == "__main__":
    main()
