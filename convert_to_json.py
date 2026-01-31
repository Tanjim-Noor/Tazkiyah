#!/usr/bin/env python3
"""
JSONL to JSON Converter

Converts Quran data from JSONL (JSON Lines) format to a single JSON array.
Useful for applications that require a single JSON file.

Usage:
    python convert_to_json.py input.jsonl output.json
    python convert_to_json.py quran_data.jsonl  # outputs quran_data.json

Author: Tazkiyah Project
"""

import json
import sys
from pathlib import Path

import click
from tqdm import tqdm


@click.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.argument("output_file", type=click.Path(), required=False)
@click.option(
    "--pretty/--compact", "-p/-c",
    default=True,
    help="Pretty print JSON (default) or compact output."
)
@click.option(
    "--validate/--no-validate",
    default=True,
    help="Validate JSON structure before conversion."
)
@click.help_option("--help", "-h")
def main(
    input_file: str,
    output_file: str | None,
    pretty: bool,
    validate: bool,
) -> None:
    """
    Convert JSONL file to JSON array format.
    
    \b
    Arguments:
        INPUT_FILE   Path to input JSONL file
        OUTPUT_FILE  Path to output JSON file (optional, defaults to same name with .json)
    
    \b
    Examples:
        python convert_to_json.py quran_data.jsonl
        python convert_to_json.py quran_data.jsonl quran_array.json
        python convert_to_json.py quran_data.jsonl -c  # compact output
    """
    input_path = Path(input_file)
    
    # Determine output path
    if output_file:
        output_path = Path(output_file)
    else:
        output_path = input_path.with_suffix(".json")
    
    # Prevent overwriting input
    if input_path == output_path:
        click.echo("Error: Output file cannot be the same as input file.", err=True)
        sys.exit(1)
    
    click.echo(f"Input:  {input_path}")
    click.echo(f"Output: {output_path}")
    click.echo("")
    
    # Count lines for progress bar
    line_count = sum(1 for _ in open(input_path, "r", encoding="utf-8"))
    
    # Read and parse JSONL
    verses = []
    errors = []
    
    with open(input_path, "r", encoding="utf-8") as f:
        for i, line in enumerate(tqdm(f, total=line_count, desc="Reading JSONL"), 1):
            line = line.strip()
            if not line:
                continue
            
            try:
                verse = json.loads(line)
                verses.append(verse)
            except json.JSONDecodeError as e:
                errors.append(f"Line {i}: {e}")
    
    if errors:
        click.echo(f"\nWarning: {len(errors)} lines could not be parsed:", err=True)
        for err in errors[:5]:
            click.echo(f"  {err}", err=True)
        if len(errors) > 5:
            click.echo(f"  ... and {len(errors) - 5} more", err=True)
    
    # Validate if requested
    if validate:
        click.echo("\nValidating structure...")
        valid, issues = validate_structure(verses)
        if not valid:
            click.echo("Validation issues found:", err=True)
            for issue in issues[:10]:
                click.echo(f"  {issue}", err=True)
    
    # Write JSON
    click.echo(f"\nWriting JSON ({len(verses)} verses)...")
    
    with open(output_path, "w", encoding="utf-8") as f:
        if pretty:
            json.dump(verses, f, indent=2, ensure_ascii=False)
        else:
            json.dump(verses, f, ensure_ascii=False)
    
    # Report file sizes
    input_size = input_path.stat().st_size / (1024 * 1024)
    output_size = output_path.stat().st_size / (1024 * 1024)
    
    click.echo(f"\nDone!")
    click.echo(f"  Input size:  {input_size:.2f} MB")
    click.echo(f"  Output size: {output_size:.2f} MB")
    click.echo(f"  Verses:      {len(verses)}")


def validate_structure(verses: list[dict]) -> tuple[bool, list[str]]:
    """
    Validate the structure of verse data.
    
    Args:
        verses: List of verse dictionaries
        
    Returns:
        Tuple of (is_valid, list of issues)
    """
    issues = []
    required_fields = ["verse_id", "surah_number", "verse_number", "arabic_text"]
    
    for i, verse in enumerate(verses):
        for field in required_fields:
            if field not in verse:
                issues.append(f"Verse {i}: missing required field '{field}'")
        
        # Check verse_id format
        verse_id = verse.get("verse_id", "")
        if ":" not in verse_id:
            issues.append(f"Verse {i}: invalid verse_id format '{verse_id}'")
    
    return len(issues) == 0, issues


if __name__ == "__main__":
    main()
