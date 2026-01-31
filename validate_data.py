#!/usr/bin/env python3
"""
Quran Data Validation Script

Validates collected Quran data for:
- Complete verse coverage (6236 verses across 114 surahs)
- Valid JSON structure
- Proper UTF-8 encoding of Arabic text
- Required fields presence
- Translation and tafsir content

Usage:
    python validate_data.py quran_data.jsonl
    python validate_data.py quran_data.json --output report.txt

Author: Tazkiyah Project
"""

import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import click

# Expected verse counts for each surah
SURAH_VERSE_COUNTS = {
    1: 7, 2: 286, 3: 200, 4: 176, 5: 120, 6: 165, 7: 206, 8: 75, 9: 129, 10: 109,
    11: 123, 12: 111, 13: 43, 14: 52, 15: 99, 16: 128, 17: 111, 18: 110, 19: 98, 20: 135,
    21: 112, 22: 78, 23: 118, 24: 64, 25: 77, 26: 227, 27: 93, 28: 88, 29: 69, 30: 60,
    31: 34, 32: 30, 33: 73, 34: 54, 35: 45, 36: 83, 37: 182, 38: 88, 39: 75, 40: 85,
    41: 54, 42: 53, 43: 89, 44: 59, 45: 37, 46: 35, 47: 38, 48: 29, 49: 18, 50: 45,
    51: 60, 52: 49, 53: 62, 54: 55, 55: 78, 56: 96, 57: 29, 58: 22, 59: 24, 60: 13,
    61: 14, 62: 11, 63: 11, 64: 18, 65: 12, 66: 12, 67: 30, 68: 52, 69: 52, 70: 44,
    71: 28, 72: 28, 73: 20, 74: 56, 75: 40, 76: 31, 77: 50, 78: 40, 79: 46, 80: 42,
    81: 29, 82: 19, 83: 36, 84: 25, 85: 22, 86: 17, 87: 19, 88: 26, 89: 30, 90: 20,
    91: 15, 92: 21, 93: 11, 94: 8, 95: 8, 96: 19, 97: 5, 98: 8, 99: 8, 100: 11,
    101: 11, 102: 8, 103: 3, 104: 9, 105: 5, 106: 4, 107: 7, 108: 3, 109: 6, 110: 3,
    111: 5, 112: 4, 113: 5, 114: 6,
}

TOTAL_VERSES = sum(SURAH_VERSE_COUNTS.values())  # 6236


@click.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option(
    "--output", "-o",
    type=click.Path(),
    help="Output file for validation report."
)
@click.option(
    "--verbose", "-v",
    is_flag=True,
    help="Show detailed validation output."
)
@click.option(
    "--strict",
    is_flag=True,
    help="Strict mode: fail on any warning."
)
@click.help_option("--help", "-h")
def main(
    input_file: str,
    output: str | None,
    verbose: bool,
    strict: bool,
) -> None:
    """
    Validate Quran data file for completeness and correctness.
    
    \b
    Arguments:
        INPUT_FILE   Path to JSONL or JSON file to validate
    
    \b
    Examples:
        python validate_data.py quran_data.jsonl
        python validate_data.py quran_data.jsonl -v
        python validate_data.py quran_data.jsonl -o report.txt --strict
    """
    input_path = Path(input_file)
    
    click.echo(f"\n{'=' * 60}")
    click.echo("QURAN DATA VALIDATION")
    click.echo(f"{'=' * 60}")
    click.echo(f"File: {input_path}")
    click.echo(f"Size: {input_path.stat().st_size / (1024 * 1024):.2f} MB")
    click.echo("")
    
    # Run validation
    is_valid, report = validate_quran_data(str(input_path), verbose=verbose)
    
    # Display report
    click.echo(report)
    
    # Save report if requested
    if output:
        output_path = Path(output)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report)
        click.echo(f"\nReport saved to: {output_path}")
    
    # Exit with appropriate code
    if not is_valid:
        click.echo("\n❌ VALIDATION FAILED", err=True)
        sys.exit(1)
    elif strict and "WARNING" in report:
        click.echo("\n❌ VALIDATION FAILED (strict mode)", err=True)
        sys.exit(1)
    else:
        click.echo("\n✅ VALIDATION PASSED")
        sys.exit(0)


def validate_quran_data(
    file_path: str,
    verbose: bool = False,
) -> tuple[bool, str]:
    """
    Validate Quran data file.
    
    Args:
        file_path: Path to JSONL or JSON file
        verbose: Include detailed output
        
    Returns:
        Tuple of (is_valid, report_string)
    """
    path = Path(file_path)
    report_lines: list[str] = []
    errors: list[str] = []
    warnings: list[str] = []
    
    # Determine file format
    is_jsonl = path.suffix.lower() == ".jsonl"
    
    # Load verses
    verses: list[dict[str, Any]] = []
    
    try:
        if is_jsonl:
            with open(path, "r", encoding="utf-8") as f:
                for i, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        verses.append(json.loads(line))
                    except json.JSONDecodeError as e:
                        errors.append(f"Line {i}: Invalid JSON - {e}")
        else:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    verses = data
                else:
                    errors.append("JSON file must contain an array of verses")
    except Exception as e:
        errors.append(f"Failed to read file: {e}")
        return False, "\n".join(errors)
    
    report_lines.append(f"Total verses loaded: {len(verses)}")
    report_lines.append(f"Expected verses:     {TOTAL_VERSES}")
    report_lines.append("")
    
    # Track verses by surah
    verses_by_surah: dict[int, set[int]] = defaultdict(set)
    translations_found: set[str] = set()
    tafsirs_found: set[str] = set()
    
    # Required fields
    required_fields = ["verse_id", "surah_number", "verse_number", "arabic_text"]
    
    # Validate each verse
    for i, verse in enumerate(verses):
        verse_id = verse.get("verse_id", f"verse_{i}")
        
        # Check required fields
        for field in required_fields:
            if field not in verse:
                errors.append(f"{verse_id}: Missing required field '{field}'")
        
        # Parse verse_id
        surah_num = verse.get("surah_number")
        verse_num = verse.get("verse_number")
        
        if surah_num and verse_num:
            verses_by_surah[surah_num].add(verse_num)
        
        # Check Arabic text
        arabic = verse.get("arabic_text", "")
        if not arabic:
            warnings.append(f"{verse_id}: Empty Arabic text")
        elif not has_arabic_chars(arabic):
            warnings.append(f"{verse_id}: Arabic text has no Arabic characters")
        
        # Track translations
        translations = verse.get("translations", {})
        translations_found.update(translations.keys())
        
        # Track tafsirs
        tafsirs = verse.get("tafsirs", {})
        tafsirs_found.update(tafsirs.keys())
    
    # Check verse coverage
    report_lines.append("SURAH COVERAGE:")
    report_lines.append("-" * 40)
    
    missing_surahs = []
    incomplete_surahs = []
    extra_surahs = []
    
    for surah_num in range(1, 115):
        expected = SURAH_VERSE_COUNTS[surah_num]
        actual = len(verses_by_surah.get(surah_num, set()))
        
        if actual == 0:
            missing_surahs.append(surah_num)
            errors.append(f"Surah {surah_num}: Missing (0/{expected} verses)")
        elif actual < expected:
            incomplete_surahs.append((surah_num, actual, expected))
            # Find missing verses
            found = verses_by_surah[surah_num]
            missing = [v for v in range(1, expected + 1) if v not in found]
            errors.append(f"Surah {surah_num}: Incomplete ({actual}/{expected} verses). Missing: {missing[:5]}{'...' if len(missing) > 5 else ''}")
        elif actual > expected:
            extra_surahs.append((surah_num, actual, expected))
            warnings.append(f"Surah {surah_num}: Extra verses ({actual}/{expected})")
        elif verbose:
            report_lines.append(f"  Surah {surah_num:3d}: ✓ {actual}/{expected}")
    
    # Find surahs not in expected range
    for surah_num in verses_by_surah:
        if surah_num < 1 or surah_num > 114:
            warnings.append(f"Invalid surah number: {surah_num}")
    
    report_lines.append(f"\n  Complete:   {114 - len(missing_surahs) - len(incomplete_surahs)} / 114 surahs")
    report_lines.append(f"  Missing:    {len(missing_surahs)}")
    report_lines.append(f"  Incomplete: {len(incomplete_surahs)}")
    
    # Translation coverage
    report_lines.append("\nTRANSLATIONS:")
    report_lines.append("-" * 40)
    if translations_found:
        for trans in sorted(translations_found):
            report_lines.append(f"  • {trans}")
    else:
        warnings.append("No translations found in data")
        report_lines.append("  (none)")
    
    # Tafsir coverage
    report_lines.append("\nTAFSIRS:")
    report_lines.append("-" * 40)
    if tafsirs_found:
        for tafsir in sorted(tafsirs_found):
            report_lines.append(f"  • {tafsir}")
    else:
        report_lines.append("  (none)")
    
    # Summary
    report_lines.append(f"\n{'=' * 40}")
    report_lines.append("VALIDATION SUMMARY")
    report_lines.append(f"{'=' * 40}")
    report_lines.append(f"Errors:   {len(errors)}")
    report_lines.append(f"Warnings: {len(warnings)}")
    
    if errors and verbose:
        report_lines.append("\nERRORS:")
        for err in errors[:20]:
            report_lines.append(f"  ❌ {err}")
        if len(errors) > 20:
            report_lines.append(f"  ... and {len(errors) - 20} more errors")
    
    if warnings and verbose:
        report_lines.append("\nWARNINGS:")
        for warn in warnings[:20]:
            report_lines.append(f"  ⚠️  {warn}")
        if len(warnings) > 20:
            report_lines.append(f"  ... and {len(warnings) - 20} more warnings")
    
    is_valid = len(errors) == 0
    report = "\n".join(report_lines)
    
    return is_valid, report


def has_arabic_chars(text: str) -> bool:
    """Check if text contains Arabic characters."""
    arabic_pattern = re.compile(r"[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]")
    return bool(arabic_pattern.search(text))


if __name__ == "__main__":
    main()
