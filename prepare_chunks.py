#!/usr/bin/env python3
"""
RAG Chunk Preparation CLI

Processes raw Quran JSON/JSONL data into clean, RAG-ready chunks.
Cleans HTML tags, formats footnotes, and prepares data for vector embedding.

Usage:
    python prepare_chunks.py input.json -o chunks.jsonl
    python prepare_chunks.py input.jsonl --format structured --inline-footnotes
    python prepare_chunks.py input.json --max-tafsir 1000 --format prose

Author: Tazkiyah Project
"""

import json
import logging
import sys
from pathlib import Path

import click

from chunk_processor import (
    ChunkConfig,
    ChunkProcessor,
    HTMLCleaner,
    ProcessingStats,
)


# Configure logging
def setup_logging(verbose: bool = False, debug: bool = False) -> None:
    """Configure logging based on verbosity."""
    level = logging.DEBUG if debug else logging.INFO if verbose else logging.WARNING
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


@click.command()
@click.argument(
    "input_file",
    type=click.Path(exists=True, path_type=Path),
)
@click.option(
    "--output", "-o",
    type=click.Path(path_type=Path),
    help="Output file path. Default: input.chunks.jsonl",
)
@click.option(
    "--output-format", "-f",
    type=click.Choice(["jsonl", "json", "txt"]),
    default="jsonl",
    help="Output format. Default: jsonl",
)
@click.option(
    "--chunk-format",
    type=click.Choice(["structured", "prose", "minimal"]),
    default="structured",
    help="Chunk text format. Default: structured",
)
@click.option(
    "--inline-footnotes/--separate-footnotes",
    default=True,
    help="Inline footnotes in translation text or keep separate. Default: inline",
)
@click.option(
    "--max-tafsir",
    type=int,
    default=0,
    help="Maximum tafsir length (0=unlimited). Default: 0",
)
@click.option(
    "--no-arabic",
    is_flag=True,
    help="Exclude Arabic text from chunks",
)
@click.option(
    "--no-tafsir",
    is_flag=True,
    help="Exclude tafsir from chunks",
)
@click.option(
    "--no-metadata",
    is_flag=True,
    help="Exclude metadata (juz, page, etc.) from chunks",
)
@click.option(
    "--no-footnotes",
    is_flag=True,
    help="Exclude footnotes from chunks",
)
@click.option(
    "--keep-html",
    is_flag=True,
    help="Keep HTML tags in tafsir (don't clean)",
)
@click.option(
    "--preview",
    type=int,
    default=0,
    help="Preview N chunks without writing output",
)
@click.option(
    "--stats-only",
    is_flag=True,
    help="Only show statistics, don't process",
)
@click.option(
    "--verbose", "-v",
    is_flag=True,
    help="Verbose output",
)
@click.option(
    "--debug",
    is_flag=True,
    help="Debug output",
)
@click.version_option(version="1.0.0")
def main(
    input_file: Path,
    output: Path | None,
    output_format: str,
    chunk_format: str,
    inline_footnotes: bool,
    max_tafsir: int,
    no_arabic: bool,
    no_tafsir: bool,
    no_metadata: bool,
    no_footnotes: bool,
    keep_html: bool,
    preview: int,
    stats_only: bool,
    verbose: bool,
    debug: bool,
) -> None:
    """
    Process Quran JSON/JSONL data into RAG-ready chunks.
    
    INPUT_FILE: Path to input JSON or JSONL file with verse data.
    
    \b
    Examples:
        # Basic processing
        python prepare_chunks.py quran_data.json
        
        # Custom output with prose format
        python prepare_chunks.py quran_data.jsonl -o rag_chunks.jsonl --chunk-format prose
        
        # Preview first 3 chunks
        python prepare_chunks.py quran_data.json --preview 3
        
        # Minimal format with truncated tafsir
        python prepare_chunks.py quran_data.json --chunk-format minimal --max-tafsir 500
        
        # For embedding (no HTML, inline footnotes)
        python prepare_chunks.py quran_data.json -o embeddings.jsonl --inline-footnotes
    """
    setup_logging(verbose, debug)
    
    # Build configuration
    config = ChunkConfig(
        include_arabic=not no_arabic,
        include_translation=True,
        include_tafsir=not no_tafsir,
        include_footnotes=not no_footnotes,
        include_metadata=not no_metadata,
        clean_html=not keep_html,
        inline_footnotes=inline_footnotes,
        max_tafsir_length=max_tafsir,
        chunk_format=chunk_format,
        output_format=output_format,
    )
    
    # Display configuration
    click.echo("=" * 60)
    click.echo("RAG CHUNK PROCESSOR")
    click.echo("=" * 60)
    click.echo(f"Input:           {input_file}")
    click.echo(f"Chunk format:    {chunk_format}")
    click.echo(f"Output format:   {output_format}")
    click.echo(f"Include Arabic:  {not no_arabic}")
    click.echo(f"Include Tafsir:  {not no_tafsir}")
    click.echo(f"Inline footnotes:{inline_footnotes}")
    click.echo(f"Clean HTML:      {not keep_html}")
    if max_tafsir > 0:
        click.echo(f"Max tafsir:      {max_tafsir} chars")
    click.echo("=" * 60)
    
    # Stats only mode
    if stats_only:
        _show_input_stats(input_file)
        return
    
    # Preview mode
    if preview > 0:
        _preview_chunks(input_file, config, preview)
        return
    
    # Process file
    try:
        processor = ChunkProcessor(config)
        output_path = processor.process_file(input_file, output)
        stats = processor.get_stats()
        
        # Display summary
        click.echo("\n" + "=" * 60)
        click.echo("PROCESSING COMPLETE")
        click.echo("=" * 60)
        click.echo(f"Verses processed: {stats.verses_processed}")
        click.echo(f"Chunks created:   {stats.chunks_created}")
        click.echo(f"HTML cleaned:     {stats.html_cleaned}")
        click.echo(f"Footnotes:        {stats.footnotes_processed}")
        if stats.tafsirs_truncated > 0:
            click.echo(f"Tafsirs truncated:{stats.tafsirs_truncated}")
        click.echo(f"Errors:           {len(stats.errors)}")
        click.echo(f"Output file:      {output_path}")
        click.echo("=" * 60)
        
        if stats.errors:
            click.echo("\nErrors encountered:", err=True)
            for error in stats.errors[:5]:
                click.echo(f"  - {error}", err=True)
            if len(stats.errors) > 5:
                click.echo(f"  ... and {len(stats.errors) - 5} more", err=True)
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        if debug:
            raise
        sys.exit(1)


def _show_input_stats(input_file: Path) -> None:
    """Show statistics about input file."""
    click.echo("\nAnalyzing input file...")
    
    with open(input_file, "r", encoding="utf-8") as f:
        if input_file.suffix.lower() == ".jsonl":
            verses = [json.loads(line) for line in f if line.strip()]
        else:
            data = json.load(f)
            verses = data if isinstance(data, list) else data.get("verses", [])
    
    # Collect stats
    total = len(verses)
    with_tafsir = sum(1 for v in verses if v.get("tafsirs"))
    with_footnotes = sum(1 for v in verses if v.get("footnotes"))
    with_arabic = sum(1 for v in verses if v.get("arabic_text"))
    
    # Check HTML in tafsirs
    html_count = 0
    for v in verses:
        for tafsir in v.get("tafsirs", {}).values():
            if "<" in tafsir and ">" in tafsir:
                html_count += 1
                break
    
    # Translation stats
    translations = set()
    for v in verses:
        translations.update(v.get("translations", {}).keys())
    
    # Tafsir stats
    tafsir_sources = set()
    for v in verses:
        tafsir_sources.update(v.get("tafsirs", {}).keys())
    
    click.echo("\n" + "=" * 60)
    click.echo("INPUT FILE STATISTICS")
    click.echo("=" * 60)
    click.echo(f"Total verses:      {total}")
    click.echo(f"With Arabic text:  {with_arabic}")
    click.echo(f"With tafsir:       {with_tafsir}")
    click.echo(f"With footnotes:    {with_footnotes}")
    click.echo(f"With HTML in tafsir:{html_count}")
    click.echo(f"\nTranslations ({len(translations)}):")
    for t in sorted(translations):
        click.echo(f"  - {t}")
    click.echo(f"\nTafsir sources ({len(tafsir_sources)}):")
    for t in sorted(tafsir_sources):
        click.echo(f"  - {t}")
    click.echo("=" * 60)


def _preview_chunks(input_file: Path, config: ChunkConfig, count: int) -> None:
    """Preview chunks without writing to file."""
    from chunk_processor import ChunkProcessor
    
    with open(input_file, "r", encoding="utf-8") as f:
        if input_file.suffix.lower() == ".jsonl":
            verses = [json.loads(line) for line in f if line.strip()]
        else:
            data = json.load(f)
            verses = data if isinstance(data, list) else data.get("verses", [])
    
    processor = ChunkProcessor(config)
    chunks = processor.process_verses(verses[:count])
    
    click.echo(f"\n{'=' * 60}")
    click.echo(f"PREVIEW: First {count} chunks")
    click.echo(f"{'=' * 60}\n")
    
    for i, chunk in enumerate(chunks, 1):
        click.echo(f"--- Chunk {i}: {chunk['id']} ---")
        click.echo(chunk["text"])
        click.echo()
        
        # Show metadata summary
        click.echo("Metadata:")
        for key, value in chunk.get("metadata", {}).items():
            if value is not None:
                click.echo(f"  {key}: {value}")
        click.echo("\n" + "=" * 60 + "\n")


@click.command("clean-html")
@click.argument("text", required=False)
@click.option("--file", "-f", type=click.Path(exists=True), help="Read from file")
def clean_html_cmd(text: str | None, file: str | None) -> None:
    """
    Clean HTML tags from text.
    
    TEXT: Text to clean (or use --file to read from file)
    
    Examples:
        python prepare_chunks.py clean-html "<p>Hello</p>"
        python prepare_chunks.py clean-html -f tafsir.html
    """
    if file:
        with open(file, "r", encoding="utf-8") as f:
            text = f.read()
    
    if not text:
        click.echo("Please provide text or use --file", err=True)
        sys.exit(1)
    
    clean = HTMLCleaner.clean(text)
    click.echo(clean)


if __name__ == "__main__":
    main()
