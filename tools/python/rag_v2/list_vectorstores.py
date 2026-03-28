#!/usr/bin/env python3
"""List available model-specific vector stores."""

from __future__ import annotations

from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from tools.python.rag_v2 import config
from tools.python.rag_v2.vectorstore_paths import discover_vectorstore_directories


console = Console()


@click.command()
@click.option(
    "--root-dir",
    default=str(config.VECTORSTORE_ROOT_DIR),
    show_default=True,
    help="Root directory that contains model-specific vector store folders.",
)
def main(root_dir: str) -> int:
    """Show which embedding-model stores already exist."""

    root_path = Path(root_dir).expanduser().resolve()
    stores = discover_vectorstore_directories(root_path)

    console.print("\n[bold cyan]Tazkiyah RAG v2 — Available Vector Stores[/bold cyan]\n")
    console.print(f"  [dim]Root:[/dim] {root_path}")
    console.print(f"  [dim]Default embedding model:[/dim] {config.EMBEDDING_MODEL}")
    console.print()

    if not stores:
        console.print("[yellow]No model-specific vector stores found.[/yellow]")
        console.print("[dim]Build the first one with:[/dim]")
        console.print(
            f"[dim]python -m tools.python.rag_v2.build_vectorstore --embedding-model \"{config.EMBEDDING_MODEL}\"[/dim]"
        )
        console.print()
        return 0

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Embedding Provider", style="cyan", no_wrap=True)
    table.add_column("Embedding Model", style="white")
    table.add_column("Collection", style="magenta")
    table.add_column("Path", style="green")

    for store_dir in stores:
        provider, model, collection = store_dir.relative_to(root_path).parts
        table.add_row(provider, model, collection, str(store_dir))

    console.print(table)
    console.print()
    console.print("[dim]Tip: switch `EMBEDDING_MODEL`, then run the builder once if the target path does not already exist.[/dim]")
    console.print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())