#!/usr/bin/env python3
"""
Terminal Chat - Simple REPL chat interface

Usage:
    python -m rag.chat
"""
import sys
import logging

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt

from rag.rag_pipeline import TazkiyahRAG
from rag import config

console = Console()
logger = logging.getLogger(__name__)


def main():
    """Interactive terminal chat with Tazkiyah RAG."""
    console.print("\n[bold cyan]Tazkiyah Chat[/bold cyan]")
    console.print("[dim]Quranic knowledge assistant powered by RAG[/dim]")
    console.print("[dim]Type 'quit' or 'exit' to leave[/dim]\n")
    
    # Initialize RAG
    rag = TazkiyahRAG()
    
    # Check collection
    stats = rag.get_collection_stats()
    if stats["count"] == 0:
        console.print("[red]Error: No documents indexed![/red]")
        console.print("[dim]Run: python -m rag.index_chunks <chunks.jsonl>[/dim]")
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
            
            # Query RAG
            console.print()
            with console.status("[cyan]Thinking...[/cyan]"):
                result = rag.query(question, return_sources=False)
            
            # Show response
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
