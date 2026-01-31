"""
RAG Chunk Processor for Tazkiyah

Processes raw Quran JSON data into clean, RAG-ready chunks:
- Cleans HTML tags from tafsir and other fields
- Formats translation footnotes inline
- Creates structured chunks for vector embedding
- Supports multiple output formats

Author: Tazkiyah Project
"""

import html
import json
import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterator

# Configure module logger
logger = logging.getLogger(__name__)


# HTML cleaning patterns
HTML_TAG_PATTERN = re.compile(r'<[^>]+>')
MULTIPLE_SPACES = re.compile(r'\s+')
MULTIPLE_NEWLINES = re.compile(r'\n{3,}')


@dataclass
class ChunkConfig:
    """Configuration for chunk generation."""
    
    # Content inclusion
    include_arabic: bool = True
    include_translation: bool = True
    include_tafsir: bool = True
    include_footnotes: bool = True
    include_metadata: bool = True
    
    # Formatting
    clean_html: bool = True
    inline_footnotes: bool = True  # Put footnotes inline vs separate section
    max_tafsir_length: int = 0  # 0 = no limit
    
    # Chunk structure
    chunk_format: str = "structured"  # "structured", "prose", "minimal"
    separator: str = "\n\n"
    
    # Output
    output_format: str = "jsonl"  # "jsonl", "json", "txt"
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "include_arabic": self.include_arabic,
            "include_translation": self.include_translation,
            "include_tafsir": self.include_tafsir,
            "include_footnotes": self.include_footnotes,
            "include_metadata": self.include_metadata,
            "clean_html": self.clean_html,
            "inline_footnotes": self.inline_footnotes,
            "max_tafsir_length": self.max_tafsir_length,
            "chunk_format": self.chunk_format,
            "output_format": self.output_format,
        }


@dataclass
class ProcessingStats:
    """Statistics for processing."""
    
    verses_processed: int = 0
    chunks_created: int = 0
    html_cleaned: int = 0
    footnotes_processed: int = 0
    tafsirs_truncated: int = 0
    errors: list[dict[str, Any]] = field(default_factory=list)
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "verses_processed": self.verses_processed,
            "chunks_created": self.chunks_created,
            "html_cleaned": self.html_cleaned,
            "footnotes_processed": self.footnotes_processed,
            "tafsirs_truncated": self.tafsirs_truncated,
            "error_count": len(self.errors),
        }


class HTMLCleaner:
    """Cleans HTML from tafsir and other text fields."""
    
    # Tags that should be converted to newlines
    BLOCK_TAGS = {'p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'br', 'li'}
    
    # Tags that should be removed entirely (with content)
    REMOVE_TAGS = {'script', 'style'}
    
    @staticmethod
    def clean(text: str) -> str:
        """
        Clean HTML from text while preserving readability.
        
        Args:
            text: HTML-containing text
            
        Returns:
            Clean plain text
        """
        if not text:
            return ""
        
        # Decode HTML entities first
        text = html.unescape(text)
        
        # Remove script and style tags with content
        text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.IGNORECASE | re.DOTALL)
        
        # Convert block-level tags to newlines
        for tag in HTMLCleaner.BLOCK_TAGS:
            text = re.sub(rf'<{tag}[^>]*>', '\n', text, flags=re.IGNORECASE)
            text = re.sub(rf'</{tag}>', '\n', text, flags=re.IGNORECASE)
        
        # Handle <br> tags specifically
        text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)
        
        # Remove all remaining HTML tags
        text = HTML_TAG_PATTERN.sub('', text)
        
        # Clean up whitespace
        text = MULTIPLE_SPACES.sub(' ', text)
        text = MULTIPLE_NEWLINES.sub('\n\n', text)
        
        # Strip leading/trailing whitespace from each line
        lines = [line.strip() for line in text.split('\n')]
        text = '\n'.join(lines)
        
        # Final strip
        return text.strip()
    
    @staticmethod
    def extract_headings(text: str) -> list[str]:
        """
        Extract heading texts from HTML.
        
        Args:
            text: HTML-containing text
            
        Returns:
            List of heading texts
        """
        headings = []
        pattern = re.compile(r'<h[1-6][^>]*>(.*?)</h[1-6]>', re.IGNORECASE | re.DOTALL)
        for match in pattern.finditer(text):
            heading_text = HTML_TAG_PATTERN.sub('', match.group(1)).strip()
            if heading_text:
                headings.append(heading_text)
        return headings


class FootnoteProcessor:
    """Processes footnotes in translation text."""
    
    FOOTNOTE_MARKER = re.compile(r'\[(\d+)\]')
    
    @staticmethod
    def inline_footnotes(
        translation: str,
        footnotes: dict[str, str],
        translation_name: str | None = None,
    ) -> str:
        """
        Inline footnote content into translation text.
        
        Args:
            translation: Translation text with [N] markers
            footnotes: Footnotes dictionary
            translation_name: Name of translation (for prefixed keys)
            
        Returns:
            Translation with footnotes inlined
        """
        if not footnotes:
            return translation
        
        def replace_footnote(match):
            num = match.group(1)
            # Try direct key first
            footnote_text = footnotes.get(num)
            # Try prefixed key if translation name provided
            if not footnote_text and translation_name:
                footnote_text = footnotes.get(f"{translation_name}:{num}")
            
            if footnote_text:
                # Clean footnote text (remove any HTML)
                clean_footnote = HTMLCleaner.clean(footnote_text)
                return f" ({clean_footnote})"
            return match.group(0)  # Keep original marker if no footnote found
        
        return FootnoteProcessor.FOOTNOTE_MARKER.sub(replace_footnote, translation)
    
    @staticmethod
    def format_footnotes_section(
        footnotes: dict[str, str],
    ) -> str:
        """
        Format footnotes as a separate section.
        
        Args:
            footnotes: Footnotes dictionary
            
        Returns:
            Formatted footnotes section
        """
        if not footnotes:
            return ""
        
        lines = ["Footnotes:"]
        for key, text in sorted(footnotes.items()):
            clean_text = HTMLCleaner.clean(text)
            # Extract just the number from prefixed keys
            display_key = key.split(":")[-1] if ":" in key else key
            lines.append(f"  [{display_key}] {clean_text}")
        
        return "\n".join(lines)


class ChunkFormatter:
    """Formats verses into RAG-ready chunks."""
    
    def __init__(self, config: ChunkConfig):
        """
        Initialize formatter.
        
        Args:
            config: Chunk configuration
        """
        self.config = config
        self.html_cleaner = HTMLCleaner()
    
    def format_verse(self, verse: dict[str, Any]) -> dict[str, Any]:
        """
        Format a verse into a RAG-ready chunk.
        
        Args:
            verse: Raw verse data
            
        Returns:
            Formatted chunk dictionary
        """
        verse_id = verse.get("verse_id", "")
        surah_name = verse.get("surah_name", "")
        surah_name_arabic = verse.get("surah_name_arabic", "")
        arabic_text = verse.get("arabic_text", "")
        translations = verse.get("translations", {})
        footnotes = verse.get("footnotes", {})
        tafsirs = verse.get("tafsirs", {})
        metadata = verse.get("metadata", {})
        
        # Build chunk text based on format
        if self.config.chunk_format == "structured":
            chunk_text = self._format_structured(
                verse_id, surah_name, surah_name_arabic,
                arabic_text, translations, footnotes, tafsirs, metadata
            )
        elif self.config.chunk_format == "prose":
            chunk_text = self._format_prose(
                verse_id, surah_name, arabic_text, translations, footnotes, tafsirs
            )
        else:  # minimal
            chunk_text = self._format_minimal(
                verse_id, arabic_text, translations, tafsirs
            )
        
        # Build output chunk
        chunk = {
            "id": verse_id,
            "text": chunk_text,
            "metadata": {
                "verse_id": verse_id,
                "surah_number": verse.get("surah_number"),
                "verse_number": verse.get("verse_number"),
                "surah_name": surah_name,
                "surah_name_arabic": surah_name_arabic,
            }
        }
        
        # Add optional metadata
        if self.config.include_metadata and metadata:
            chunk["metadata"].update({
                "juz": metadata.get("juz"),
                "hizb": metadata.get("hizb"),
                "page": metadata.get("page"),
                "revelation_place": metadata.get("revelation_place"),
            })
        
        # Add clean fields for potential direct access
        chunk["arabic_text"] = arabic_text
        chunk["translations"] = self._clean_translations(translations, footnotes)
        chunk["tafsirs"] = self._clean_tafsirs(tafsirs)
        
        if self.config.include_footnotes:
            chunk["footnotes"] = {k: HTMLCleaner.clean(v) for k, v in footnotes.items()}
        
        return chunk
    
    def _format_structured(
        self,
        verse_id: str,
        surah_name: str,
        surah_name_arabic: str,
        arabic_text: str,
        translations: dict[str, str],
        footnotes: dict[str, str],
        tafsirs: dict[str, str],
        metadata: dict[str, Any],
    ) -> str:
        """Format as structured chunk with clear sections."""
        sections = []
        
        # Header
        sections.append(f"=== Verse {verse_id} - {surah_name} ({surah_name_arabic}) ===")
        
        # Arabic
        if self.config.include_arabic and arabic_text:
            sections.append(f"Arabic:\n{arabic_text}")
        
        # Translations
        if self.config.include_translation and translations:
            trans_lines = ["Translation:"]
            for name, text in translations.items():
                clean_text = text
                if self.config.inline_footnotes and footnotes:
                    clean_text = FootnoteProcessor.inline_footnotes(text, footnotes, name)
                trans_lines.append(f"  [{name}] {clean_text}")
            sections.append("\n".join(trans_lines))
        
        # Footnotes (if not inlined)
        if self.config.include_footnotes and footnotes and not self.config.inline_footnotes:
            sections.append(FootnoteProcessor.format_footnotes_section(footnotes))
        
        # Tafsir
        if self.config.include_tafsir and tafsirs:
            for scholar, tafsir_text in tafsirs.items():
                clean_tafsir = self._process_tafsir(tafsir_text)
                sections.append(f"Tafsir ({scholar}):\n{clean_tafsir}")
        
        # Metadata summary
        if self.config.include_metadata and metadata:
            meta_parts = []
            if metadata.get("juz"):
                meta_parts.append(f"Juz {metadata['juz']}")
            if metadata.get("revelation_place"):
                meta_parts.append(f"Revealed in {metadata['revelation_place'].title()}")
            if meta_parts:
                sections.append(f"Context: {', '.join(meta_parts)}")
        
        return self.config.separator.join(sections)
    
    def _format_prose(
        self,
        verse_id: str,
        surah_name: str,
        arabic_text: str,
        translations: dict[str, str],
        footnotes: dict[str, str],
        tafsirs: dict[str, str],
    ) -> str:
        """Format as natural prose paragraph."""
        parts = []
        
        # Opening
        parts.append(f"Verse {verse_id} from Surah {surah_name}:")
        
        # Arabic
        if self.config.include_arabic and arabic_text:
            parts.append(f'"{arabic_text}"')
        
        # Primary translation
        if self.config.include_translation and translations:
            trans_name, trans_text = next(iter(translations.items()))
            if self.config.inline_footnotes and footnotes:
                trans_text = FootnoteProcessor.inline_footnotes(trans_text, footnotes, trans_name)
            parts.append(f"Translation ({trans_name}): {trans_text}")
        
        # Tafsir summary
        if self.config.include_tafsir and tafsirs:
            scholar, tafsir_text = next(iter(tafsirs.items()))
            clean_tafsir = self._process_tafsir(tafsir_text)
            # For prose, truncate long tafsir
            if len(clean_tafsir) > 1000:
                clean_tafsir = clean_tafsir[:1000] + "..."
            parts.append(f"According to {scholar}: {clean_tafsir}")
        
        return " ".join(parts)
    
    def _format_minimal(
        self,
        verse_id: str,
        arabic_text: str,
        translations: dict[str, str],
        tafsirs: dict[str, str],
    ) -> str:
        """Format as minimal text for embedding."""
        parts = [verse_id]
        
        if self.config.include_arabic and arabic_text:
            parts.append(arabic_text)
        
        if self.config.include_translation and translations:
            # Join all translations
            for text in translations.values():
                # Remove footnote markers for minimal format
                clean = re.sub(r'\[\d+\]', '', text)
                parts.append(clean)
        
        if self.config.include_tafsir and tafsirs:
            for tafsir_text in tafsirs.values():
                clean = self._process_tafsir(tafsir_text)
                if len(clean) > 500:
                    clean = clean[:500]
                parts.append(clean)
        
        return " ".join(parts)
    
    def _process_tafsir(self, tafsir_text: str) -> str:
        """Process tafsir text (clean HTML, optionally truncate)."""
        if not tafsir_text:
            return ""
        
        if self.config.clean_html:
            tafsir_text = HTMLCleaner.clean(tafsir_text)
        
        if self.config.max_tafsir_length > 0 and len(tafsir_text) > self.config.max_tafsir_length:
            tafsir_text = tafsir_text[:self.config.max_tafsir_length] + "..."
        
        return tafsir_text
    
    def _clean_translations(
        self,
        translations: dict[str, str],
        footnotes: dict[str, str],
    ) -> dict[str, str]:
        """Clean and optionally inline footnotes in translations."""
        result = {}
        for name, text in translations.items():
            if self.config.inline_footnotes and footnotes:
                result[name] = FootnoteProcessor.inline_footnotes(text, footnotes, name)
            else:
                result[name] = text
        return result
    
    def _clean_tafsirs(self, tafsirs: dict[str, str]) -> dict[str, str]:
        """Clean HTML from tafsirs."""
        result = {}
        for scholar, text in tafsirs.items():
            if self.config.clean_html:
                result[scholar] = HTMLCleaner.clean(text)
            else:
                result[scholar] = text
            
            if self.config.max_tafsir_length > 0:
                if len(result[scholar]) > self.config.max_tafsir_length:
                    result[scholar] = result[scholar][:self.config.max_tafsir_length] + "..."
        return result


class ChunkProcessor:
    """
    Main processor for creating RAG chunks from Quran data.
    
    Example:
        >>> processor = ChunkProcessor(config)
        >>> processor.process_file("quran_data.json", "rag_chunks.jsonl")
    """
    
    def __init__(self, config: ChunkConfig | None = None):
        """
        Initialize processor.
        
        Args:
            config: Processing configuration (uses defaults if None)
        """
        self.config = config or ChunkConfig()
        self.formatter = ChunkFormatter(self.config)
        self.stats = ProcessingStats()
        
        logger.info(f"ChunkProcessor initialized: format={self.config.chunk_format}")
    
    def process_file(
        self,
        input_path: str | Path,
        output_path: str | Path | None = None,
    ) -> Path:
        """
        Process input file and create RAG chunks.
        
        Args:
            input_path: Path to input JSON/JSONL file
            output_path: Path to output file (auto-generated if None)
            
        Returns:
            Path to output file
        """
        input_path = Path(input_path)
        
        # Auto-generate output path if not provided
        if output_path is None:
            suffix = f".chunks.{self.config.output_format}"
            output_path = input_path.with_suffix(suffix)
        else:
            output_path = Path(output_path)
        
        logger.info(f"Processing: {input_path} -> {output_path}")
        
        # Load input data
        verses = self._load_input(input_path)
        
        # Process verses
        chunks = []
        for verse in verses:
            try:
                chunk = self.formatter.format_verse(verse)
                chunks.append(chunk)
                self.stats.verses_processed += 1
                self.stats.chunks_created += 1
                
                # Track stats
                if verse.get("tafsirs"):
                    self.stats.html_cleaned += 1
                if verse.get("footnotes"):
                    self.stats.footnotes_processed += 1
                    
            except Exception as e:
                logger.error(f"Error processing verse {verse.get('verse_id')}: {e}")
                self.stats.errors.append({
                    "verse_id": verse.get("verse_id"),
                    "error": str(e),
                })
        
        # Write output
        self._write_output(chunks, output_path)
        
        logger.info(f"Processing complete: {self.stats.to_dict()}")
        return output_path
    
    def process_verses(
        self,
        verses: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """
        Process list of verses into chunks.
        
        Args:
            verses: List of verse dictionaries
            
        Returns:
            List of chunk dictionaries
        """
        chunks = []
        for verse in verses:
            try:
                chunk = self.formatter.format_verse(verse)
                chunks.append(chunk)
                self.stats.verses_processed += 1
                self.stats.chunks_created += 1
            except Exception as e:
                logger.error(f"Error processing verse: {e}")
                self.stats.errors.append({"error": str(e)})
        return chunks
    
    def _load_input(self, path: Path) -> list[dict[str, Any]]:
        """Load verses from JSON or JSONL file."""
        with open(path, "r", encoding="utf-8") as f:
            if path.suffix.lower() == ".jsonl":
                return [json.loads(line) for line in f if line.strip()]
            else:
                data = json.load(f)
                # Handle both array and object with "verses" key
                if isinstance(data, list):
                    return data
                return data.get("verses", data.get("data", []))
    
    def _write_output(self, chunks: list[dict[str, Any]], path: Path) -> None:
        """Write chunks to output file."""
        with open(path, "w", encoding="utf-8") as f:
            if self.config.output_format == "jsonl":
                for chunk in chunks:
                    f.write(json.dumps(chunk, ensure_ascii=False) + "\n")
            elif self.config.output_format == "json":
                json.dump(chunks, f, ensure_ascii=False, indent=2)
            else:  # txt
                for chunk in chunks:
                    f.write(chunk["text"])
                    f.write("\n\n" + "=" * 60 + "\n\n")
    
    def get_stats(self) -> ProcessingStats:
        """Get processing statistics."""
        return self.stats


def clean_html_text(text: str) -> str:
    """Convenience function to clean HTML from text."""
    return HTMLCleaner.clean(text)


def process_quran_data(
    input_file: str,
    output_file: str | None = None,
    **config_kwargs,
) -> Path:
    """
    Convenience function to process Quran data.
    
    Args:
        input_file: Input JSON/JSONL file
        output_file: Output file (auto-generated if None)
        **config_kwargs: Configuration options
        
    Returns:
        Path to output file
    """
    config = ChunkConfig(**config_kwargs)
    processor = ChunkProcessor(config)
    return processor.process_file(input_file, output_file)
