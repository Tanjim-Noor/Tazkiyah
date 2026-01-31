#!/usr/bin/env python3
"""
Quran Data Collection CLI

A command-line tool for collecting Quran data from the Quran Foundation API.
Supports translations, tafsirs, and outputs to JSONL or JSON format.

Usage:
    python collect_quran.py --help
    python collect_quran.py --list-resources
    python collect_quran.py --all --translations 131,85 --output quran.jsonl
    python collect_quran.py --surah-range 1 10 --translations 131 --tafsirs 169

Author: Tazkiyah Project
"""

import json
import logging
import sys
from pathlib import Path

import click

from collector import QuranDataCollector
from quran_api import QuranAPIClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def parse_int_list(ctx, param, value: str | None) -> list[int]:
    """Parse comma-separated integer list."""
    if not value:
        return []
    try:
        return [int(x.strip()) for x in value.split(",") if x.strip()]
    except ValueError as e:
        raise click.BadParameter(f"Invalid integer list: {value}") from e


def setup_logging(verbose: bool, debug: bool) -> None:
    """Configure logging based on verbosity flags."""
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.getLogger("urllib3").setLevel(logging.DEBUG)
    elif verbose:
        logging.getLogger().setLevel(logging.INFO)
    else:
        logging.getLogger().setLevel(logging.WARNING)
        # Keep our loggers at INFO level
        logging.getLogger("collector").setLevel(logging.INFO)
        logging.getLogger("quran_api").setLevel(logging.INFO)


@click.command()
@click.option(
    "--all", "collect_all",
    is_flag=True,
    help="Collect all 114 surahs."
)
@click.option(
    "--surah", "-s",
    type=int,
    help="Collect a specific surah (1-114)."
)
@click.option(
    "--surah-range", "-r",
    nargs=2,
    type=int,
    metavar="START END",
    help="Collect a range of surahs (e.g., -r 1 10)."
)
@click.option(
    "--translations", "-t",
    callback=parse_int_list,
    help="Comma-separated translation IDs (e.g., 131,85)."
)
@click.option(
    "--tafsirs", "-T",
    callback=parse_int_list,
    help="Comma-separated tafsir IDs (e.g., 169). Optional."
)
@click.option(
    "--output", "-o",
    type=click.Path(),
    default="quran_data.jsonl",
    help="Output file path (default: quran_data.jsonl)."
)
@click.option(
    "--output-format", "-f",
    type=click.Choice(["jsonl", "json"], case_sensitive=False),
    default="jsonl",
    help="Output format: jsonl (default) or json."
)
@click.option(
    "--concurrency", "-c",
    type=click.IntRange(1, 10),
    default=3,
    help="Parallel threads for tafsir fetching (1-10, default: 3)."
)
@click.option(
    "--batch-size", "-b",
    type=int,
    default=50,
    help="Verses to buffer before writing (default: 50)."
)
@click.option(
    "--rate-limit-delay",
    type=float,
    default=0.3,
    help="Seconds between API requests (default: 0.3)."
)
@click.option(
    "--resume",
    is_flag=True,
    help="Resume from existing file (JSONL only)."
)
@click.option(
    "--no-metadata",
    is_flag=True,
    help="Exclude verse metadata (juz, page, etc.)."
)
@click.option(
    "--config",
    type=click.Path(exists=True),
    help="Load configuration from JSON file."
)
@click.option(
    "--list-resources",
    is_flag=True,
    help="List available translations and tafsirs."
)
@click.option(
    "--validate-only",
    is_flag=True,
    help="Validate existing data file without collecting."
)
@click.option(
    "--verbose", "-v",
    is_flag=True,
    help="Enable verbose output."
)
@click.option(
    "--debug",
    is_flag=True,
    help="Enable debug output (very verbose)."
)
@click.version_option(version="1.0.0", prog_name="collect-quran")
@click.help_option("--help", "-h")
def main(
    collect_all: bool,
    surah: int | None,
    surah_range: tuple[int, int] | None,
    translations: list[int],
    tafsirs: list[int],
    output: str,
    output_format: str,
    concurrency: int,
    batch_size: int,
    rate_limit_delay: float,
    resume: bool,
    no_metadata: bool,
    config: str | None,
    list_resources: bool,
    validate_only: bool,
    verbose: bool,
    debug: bool,
) -> None:
    """
    Collect Quran data from the Quran Foundation API.
    
    \b
    Examples:
      # List available translations and tafsirs
      python collect_quran.py --list-resources
      
      # Collect all surahs with translations
      python collect_quran.py --all -t 131,85 -o quran.jsonl
      
      # Collect specific surah with tafsir
      python collect_quran.py -s 2 -t 131 -T 169 -o baqarah.jsonl
      
      # Collect range of surahs
      python collect_quran.py -r 1 10 -t 131,85 -o first_ten.jsonl
      
      # Resume interrupted collection
      python collect_quran.py --all -t 131 --resume -o quran.jsonl
    """
    setup_logging(verbose, debug)
    
    # Load configuration file if provided
    if config:
        config_data = load_config(config)
        # Merge config with CLI options (CLI takes precedence)
        translations = translations or config_data.get("translations", {}).get("ids", [])
        tafsirs = tafsirs or config_data.get("tafsirs", {}).get("ids", [])
        concurrency = concurrency or config_data.get("performance", {}).get("concurrency", 3)
        batch_size = batch_size or config_data.get("performance", {}).get("batch_size", 50)
        output_format = output_format or config_data.get("output", {}).get("format", "jsonl")
        rate_limit_delay = rate_limit_delay or config_data.get("api", {}).get("rate_limit_delay", 0.3)
    
    # Handle --list-resources
    if list_resources:
        list_available_resources()
        return
    
    # Handle --validate-only
    if validate_only:
        validate_data_file(output)
        return
    
    # Validate collection mode
    if not any([collect_all, surah, surah_range]):
        click.echo("Error: Specify collection mode: --all, --surah, or --surah-range", err=True)
        click.echo("Use --help for usage information.", err=True)
        sys.exit(1)
    
    # Validate translations
    if not translations:
        click.echo("Error: At least one translation ID is required (-t/--translations)", err=True)
        click.echo("Use --list-resources to see available translations.", err=True)
        sys.exit(1)
    
    # Validate resume with json format
    if resume and output_format == "json":
        click.echo("Error: --resume is only supported with JSONL format", err=True)
        sys.exit(1)
    
    # Ensure output file has correct extension
    output_path = Path(output)
    if output_format == "jsonl" and not output_path.suffix == ".jsonl":
        output_path = output_path.with_suffix(".jsonl")
    elif output_format == "json" and not output_path.suffix == ".json":
        output_path = output_path.with_suffix(".json")
    
    # Display collection plan
    click.echo("\n" + "=" * 60)
    click.echo("QURAN DATA COLLECTION")
    click.echo("=" * 60)
    
    if collect_all:
        click.echo("Mode:         All 114 surahs")
    elif surah:
        click.echo(f"Mode:         Single surah ({surah})")
    elif surah_range:
        click.echo(f"Mode:         Range (surahs {surah_range[0]}-{surah_range[1]})")
    
    click.echo(f"Translations: {translations}")
    click.echo(f"Tafsirs:      {tafsirs if tafsirs else 'None (skipping)'}")
    click.echo(f"Output:       {output_path}")
    click.echo(f"Format:       {output_format.upper()}")
    click.echo(f"Concurrency:  {concurrency}")
    click.echo(f"Resume:       {'Yes' if resume else 'No'}")
    click.echo("=" * 60 + "\n")
    
    # Create collector
    collector = QuranDataCollector(
        output_file=output_path,
        translations=translations,
        tafsirs=tafsirs,
        output_format=output_format,
        batch_size=batch_size,
        concurrency=concurrency,
        include_metadata=not no_metadata,
        rate_limit_delay=rate_limit_delay,
        resume=resume,
    )
    
    try:
        # Run collection
        if collect_all:
            stats = collector.collect_all()
        elif surah:
            stats = collector.collect_single(surah)
        elif surah_range:
            stats = collector.collect_range(surah_range[0], surah_range[1])
        else:
            raise click.UsageError("No collection mode specified")
        
        # Convert to JSON if needed
        if output_format == "json" and output_path.suffix == ".jsonl":
            convert_jsonl_to_json(output_path)
        
        # Display summary
        click.echo("\n" + "=" * 60)
        click.echo("COLLECTION COMPLETE")
        click.echo("=" * 60)
        click.echo(f"Chapters processed: {stats.chapters_processed}")
        click.echo(f"Verses collected:   {stats.verses_collected}")
        click.echo(f"Translations:       {stats.translations_included}")
        click.echo(f"Footnotes fetched:  {stats.footnotes_fetched}")
        click.echo(f"Tafsirs fetched:    {stats.tafsirs_fetched}")
        click.echo(f"Errors:             {len(stats.errors)}")
        click.echo(f"Output file:        {output_path}")
        click.echo("=" * 60)
        
        # Save errors if any
        if stats.errors:
            error_file = output_path.with_suffix(".errors.json")
            collector.save_errors(error_file)
            click.echo(f"Errors saved to:    {error_file}")
        
    except KeyboardInterrupt:
        click.echo("\nCollection interrupted. Progress saved.", err=True)
        sys.exit(1)
    except Exception as e:
        logger.exception("Collection failed")
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


def load_config(config_path: str) -> dict:
    """Load configuration from JSON file."""
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def list_available_resources() -> None:
    """List available translations and tafsirs from the API."""
    click.echo("\nFetching available resources from Quran Foundation API...\n")
    
    client = QuranAPIClient()
    
    try:
        # Fetch translations
        click.echo("=" * 60)
        click.echo("AVAILABLE TRANSLATIONS")
        click.echo("=" * 60)
        
        translations = client.get_translations_list()
        
        # Group by language
        by_language: dict[str, list] = {}
        for t in translations:
            lang = t.get("language_name", "unknown")
            if lang not in by_language:
                by_language[lang] = []
            by_language[lang].append(t)
        
        for lang in sorted(by_language.keys()):
            click.echo(f"\n  {lang.upper()}:")
            for t in sorted(by_language[lang], key=lambda x: x.get("id", 0)):
                click.echo(f"    ID {t['id']:4d}: {t.get('name', 'Unknown')}")
        
        # Fetch tafsirs
        click.echo("\n" + "=" * 60)
        click.echo("AVAILABLE TAFSIRS")
        click.echo("=" * 60)
        
        tafsirs = client.get_tafsirs_list()
        
        # Group by language
        by_language = {}
        for t in tafsirs:
            lang = t.get("language_name", "unknown")
            if lang not in by_language:
                by_language[lang] = []
            by_language[lang].append(t)
        
        for lang in sorted(by_language.keys()):
            click.echo(f"\n  {lang.upper()}:")
            for t in sorted(by_language[lang], key=lambda x: x.get("id", 0)):
                click.echo(f"    ID {t['id']:4d}: {t.get('name', 'Unknown')}")
        
        click.echo("\n" + "=" * 60)
        click.echo("USAGE EXAMPLE")
        click.echo("=" * 60)
        click.echo("  python collect_quran.py --all -t 131,85 -T 169 -o quran.jsonl")
        click.echo("")
        
    finally:
        client.close()


def validate_data_file(file_path: str) -> None:
    """Validate an existing data file."""
    path = Path(file_path)
    
    if not path.exists():
        click.echo(f"Error: File not found: {path}", err=True)
        sys.exit(1)
    
    click.echo(f"\nValidating: {path}\n")
    
    # Import validation module
    try:
        from validate_data import validate_quran_data
        is_valid, report = validate_quran_data(str(path))
        
        if is_valid:
            click.echo("✓ Validation PASSED")
        else:
            click.echo("✗ Validation FAILED")
            click.echo(report)
            sys.exit(1)
            
    except ImportError:
        click.echo("Validation module not found. Running basic checks...")
        
        # Basic validation
        total_lines = 0
        valid_lines = 0
        errors = []
        
        with open(path, "r", encoding="utf-8") as f:
            for i, line in enumerate(f, 1):
                total_lines += 1
                try:
                    json.loads(line)
                    valid_lines += 1
                except json.JSONDecodeError as e:
                    errors.append(f"Line {i}: {e}")
        
        click.echo(f"Total lines:  {total_lines}")
        click.echo(f"Valid JSON:   {valid_lines}")
        click.echo(f"Errors:       {len(errors)}")
        
        if errors:
            click.echo("\nFirst 5 errors:")
            for err in errors[:5]:
                click.echo(f"  {err}")


def convert_jsonl_to_json(jsonl_path: Path) -> None:
    """Convert JSONL file to JSON array format."""
    json_path = jsonl_path.with_suffix(".json")
    
    click.echo(f"Converting to JSON format: {json_path}")
    
    verses = []
    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                verses.append(json.loads(line))
    
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(verses, f, indent=2, ensure_ascii=False)
    
    click.echo(f"Converted {len(verses)} verses to {json_path}")


if __name__ == "__main__":
    main()
