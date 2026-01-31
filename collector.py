"""
Quran Data Collector

Orchestrates data collection from the Quran Foundation API:
- Fetches chapters and verses with translations
- Optional tafsir fetching in parallel
- JSONL output with batch writes
- Resume capability at chapter level
- Signal handling for graceful shutdown

Author: Tazkiyah Project
"""

import atexit
import json
import logging
import os
import re
import signal
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, TextIO

from tqdm import tqdm

from quran_api import QuranAPIClient
from tafsir_fetcher import TafsirFetcher

# Configure module logger
logger = logging.getLogger(__name__)


@dataclass
class CollectorStats:
    """Statistics for the collection process."""
    
    chapters_processed: int = 0
    verses_collected: int = 0
    translations_included: int = 0
    tafsirs_fetched: int = 0
    errors: list[dict[str, Any]] = field(default_factory=list)
    
    def to_dict(self) -> dict[str, Any]:
        """Convert stats to dictionary."""
        return {
            "chapters_processed": self.chapters_processed,
            "verses_collected": self.verses_collected,
            "translations_included": self.translations_included,
            "tafsirs_fetched": self.tafsirs_fetched,
            "error_count": len(self.errors),
        }


@dataclass
class ResumeState:
    """State for resuming interrupted collection."""
    
    completed_chapters: set[int] = field(default_factory=set)
    last_verse_key: str | None = None
    total_verses_written: int = 0


class QuranDataCollector:
    """
    Orchestrates Quran data collection from the API.
    
    Features:
    - Batch JSONL writes (configurable batch size)
    - Chapter-level resume from existing file
    - Signal handling for graceful interruption
    - Nested progress bars (chapters → verses)
    - Optional tafsir collection
    
    Example:
        >>> collector = QuranDataCollector(
        ...     output_file="quran.jsonl",
        ...     translations=[131, 85],
        ...     tafsirs=[169],
        ... )
        >>> collector.collect_all()
    """
    
    def __init__(
        self,
        output_file: str | Path,
        translations: list[int] | None = None,
        tafsirs: list[int] | None = None,
        output_format: str = "jsonl",
        batch_size: int = 50,
        concurrency: int = 3,
        include_metadata: bool = True,
        rate_limit_delay: float = 0.3,
        resume: bool = False,
    ) -> None:
        """
        Initialize the data collector.
        
        Args:
            output_file: Path to output file (.jsonl or .json)
            translations: List of translation IDs to include
            tafsirs: List of tafsir IDs to include (optional)
            output_format: "jsonl" (default) or "json"
            batch_size: Verses to buffer before writing (default: 50)
            concurrency: Parallel threads for tafsir fetching
            include_metadata: Include verse metadata (juz, page, etc.)
            rate_limit_delay: Seconds between API requests
            resume: Resume from existing file
        """
        self.output_file = Path(output_file)
        self.translations = translations or []
        self.tafsirs = tafsirs or []
        self.output_format = output_format.lower()
        self.batch_size = batch_size
        self.concurrency = concurrency
        self.include_metadata = include_metadata
        self.resume = resume
        
        # Initialize API client
        self.api_client = QuranAPIClient(
            rate_limit_delay=rate_limit_delay,
            concurrency=concurrency,
        )
        
        # Initialize tafsir fetcher if needed
        self.tafsir_fetcher: TafsirFetcher | None = None
        self.tafsir_names: dict[int, str] = {}
        
        # State
        self.stats = CollectorStats()
        self.resume_state = ResumeState()
        self._verse_buffer: list[dict[str, Any]] = []
        self._output_handle: TextIO | None = None
        self._shutdown_requested = False
        self._chapters_cache: list[dict[str, Any]] = []
        self._translation_names: dict[int, str] = {}
        
        # Set up signal handlers for graceful shutdown
        self._setup_signal_handlers()
        
        logger.info(
            f"QuranDataCollector initialized: output={output_file}, "
            f"translations={translations}, tafsirs={tafsirs}, "
            f"format={output_format}, batch_size={batch_size}"
        )
    
    def _setup_signal_handlers(self) -> None:
        """Set up signal handlers for graceful shutdown."""
        def signal_handler(signum, frame):
            logger.warning(f"Received signal {signum}. Initiating graceful shutdown...")
            self._shutdown_requested = True
        
        # Handle SIGINT (Ctrl+C) and SIGTERM
        signal.signal(signal.SIGINT, signal_handler)
        if hasattr(signal, 'SIGTERM'):
            signal.signal(signal.SIGTERM, signal_handler)
        
        # Ensure cleanup on exit
        atexit.register(self._cleanup)
    
    def _cleanup(self) -> None:
        """Clean up resources."""
        self._flush_buffer(force=True)
        if self._output_handle:
            self._output_handle.close()
            self._output_handle = None
        self.api_client.close()
    
    def _load_resume_state(self) -> None:
        """Load resume state from existing JSONL file."""
        if not self.output_file.exists():
            logger.info("No existing file found. Starting fresh.")
            return
        
        logger.info(f"Loading resume state from {self.output_file}...")
        
        try:
            with open(self.output_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    try:
                        verse = json.loads(line)
                        verse_key = verse.get("verse_id") or verse.get("verse_key")
                        
                        if verse_key:
                            # Parse chapter from verse_key (e.g., "2:255" -> 2)
                            match = re.match(r"(\d+):\d+", verse_key)
                            if match:
                                chapter_num = int(match.group(1))
                                self.resume_state.completed_chapters.add(chapter_num)
                            
                            self.resume_state.last_verse_key = verse_key
                            self.resume_state.total_verses_written += 1
                    
                    except json.JSONDecodeError:
                        logger.warning(f"Invalid JSON line in file, skipping")
            
            logger.info(
                f"Resume state loaded: {len(self.resume_state.completed_chapters)} chapters, "
                f"{self.resume_state.total_verses_written} verses, "
                f"last={self.resume_state.last_verse_key}"
            )
            
        except Exception as e:
            logger.error(f"Error loading resume state: {e}")
    
    def _determine_complete_chapters(self, chapters: list[dict[str, Any]]) -> set[int]:
        """
        Determine which chapters are complete based on verse counts.
        
        Args:
            chapters: List of chapter metadata from API
            
        Returns:
            Set of chapter numbers that are complete
        """
        if not self.resume_state.completed_chapters:
            return set()
        
        # Create mapping of chapter number to expected verse count
        chapter_verse_counts: dict[int, int] = {
            ch["id"]: ch.get("verses_count", 0)
            for ch in chapters
        }
        
        # Count verses per chapter in existing file
        verses_per_chapter: dict[int, int] = {}
        
        if self.output_file.exists():
            with open(self.output_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    try:
                        verse = json.loads(line)
                        verse_key = verse.get("verse_id") or verse.get("verse_key")
                        if verse_key:
                            match = re.match(r"(\d+):\d+", verse_key)
                            if match:
                                ch_num = int(match.group(1))
                                verses_per_chapter[ch_num] = verses_per_chapter.get(ch_num, 0) + 1
                    except json.JSONDecodeError:
                        pass
        
        # Determine complete chapters
        complete = set()
        for ch_num, expected in chapter_verse_counts.items():
            actual = verses_per_chapter.get(ch_num, 0)
            if actual >= expected:
                complete.add(ch_num)
        
        return complete
    
    def _initialize_resources(self) -> None:
        """Initialize translation and tafsir resources."""
        # Fetch translation names
        if self.translations:
            logger.info("Fetching translation resources...")
            translations_list = self.api_client.get_translations_list()
            self._translation_names = {
                t["id"]: t.get("name", f"Translation {t['id']}")
                for t in translations_list
                if t["id"] in self.translations
            }
            logger.info(f"Found {len(self._translation_names)} translations")
        
        # Fetch tafsir names and initialize fetcher
        if self.tafsirs:
            logger.info("Fetching tafsir resources...")
            tafsirs_list = self.api_client.get_tafsirs_list()
            self.tafsir_names = {
                t["id"]: t.get("name", f"Tafsir {t['id']}")
                for t in tafsirs_list
                if t["id"] in self.tafsirs
            }
            
            self.tafsir_fetcher = TafsirFetcher(
                api_client=self.api_client,
                tafsir_ids=self.tafsirs,
                tafsir_names=self.tafsir_names,
                concurrency=self.concurrency,
                show_progress=True,
            )
            logger.info(f"Found {len(self.tafsir_names)} tafsirs")
    
    def _open_output_file(self, append: bool = False) -> None:
        """Open the output file for writing."""
        mode = "a" if append else "w"
        self._output_handle = open(
            self.output_file,
            mode,
            encoding="utf-8",
        )
    
    def _format_verse(
        self,
        verse: dict[str, Any],
        chapter: dict[str, Any],
        tafsirs: dict[str, str | None] | None = None,
    ) -> dict[str, Any]:
        """
        Format a verse into the output schema.
        
        Args:
            verse: Raw verse data from API
            chapter: Chapter metadata
            tafsirs: Optional tafsir content
            
        Returns:
            Formatted verse dictionary
        """
        verse_key = verse.get("verse_key", f"{chapter['id']}:{verse.get('verse_number')}")
        
        # Format translations
        translations_dict: dict[str, str] = {}
        for trans in verse.get("translations", []):
            trans_id = trans.get("resource_id")
            trans_name = self._translation_names.get(trans_id, f"Translation {trans_id}")
            translations_dict[trans_name] = trans.get("text", "")
        
        # Build output structure
        result: dict[str, Any] = {
            "verse_id": verse_key,
            "surah_number": chapter["id"],
            "verse_number": verse.get("verse_number"),
            "surah_name": chapter.get("name_simple", ""),
            "surah_name_arabic": chapter.get("name_arabic", ""),
            "arabic_text": verse.get("text_uthmani", ""),
            "translations": translations_dict,
        }
        
        # Add tafsirs if provided
        if tafsirs:
            # Filter out None values
            result["tafsirs"] = {k: v for k, v in tafsirs.items() if v is not None}
        else:
            result["tafsirs"] = {}
        
        # Add metadata if requested
        if self.include_metadata:
            result["metadata"] = {
                "juz": verse.get("juz_number"),
                "page": verse.get("page_number"),
                "hizb": verse.get("hizb_number"),
                "rub_el_hizb": verse.get("rub_el_hizb_number"),
                "ruku": verse.get("ruku_number"),
                "manzil": verse.get("manzil_number"),
                "sajdah": verse.get("sajdah_number"),
                "revelation_place": chapter.get("revelation_place"),
                "revelation_order": chapter.get("revelation_order"),
            }
        
        return result
    
    def _flush_buffer(self, force: bool = False) -> None:
        """
        Flush the verse buffer to the output file.
        
        Args:
            force: Flush even if buffer is not full
        """
        if not self._verse_buffer:
            return
        
        if not force and len(self._verse_buffer) < self.batch_size:
            return
        
        if not self._output_handle:
            return
        
        logger.debug(f"Flushing {len(self._verse_buffer)} verses to file")
        
        for verse in self._verse_buffer:
            json_line = json.dumps(verse, ensure_ascii=False)
            self._output_handle.write(json_line + "\n")
        
        self._output_handle.flush()
        self._verse_buffer.clear()
    
    def _add_to_buffer(self, verse: dict[str, Any]) -> None:
        """Add a verse to the buffer and flush if needed."""
        self._verse_buffer.append(verse)
        self.stats.verses_collected += 1
        
        if len(self._verse_buffer) >= self.batch_size:
            self._flush_buffer(force=True)
    
    def _collect_chapter(
        self,
        chapter: dict[str, Any],
        pbar_position: int = 1,
    ) -> bool:
        """
        Collect all verses for a chapter.
        
        Args:
            chapter: Chapter metadata
            pbar_position: Position for nested progress bar
            
        Returns:
            True if successful, False if interrupted
        """
        chapter_num = chapter["id"]
        chapter_name = chapter.get("name_simple", f"Chapter {chapter_num}")
        verses_count = chapter.get("verses_count", 0)
        
        logger.info(f"Collecting chapter {chapter_num}: {chapter_name} ({verses_count} verses)")
        
        # Fetch all verses with translations
        verses = self.api_client.get_all_verses_by_chapter(
            chapter_number=chapter_num,
            translations=self.translations,
        )
        
        if self._shutdown_requested:
            return False
        
        # Fetch tafsirs if enabled
        tafsirs_map: dict[str, dict[str, str | None]] = {}
        if self.tafsir_fetcher and self.tafsirs:
            verse_keys = [v.get("verse_key") for v in verses]
            tafsirs_map = self.tafsir_fetcher.fetch_for_verses(
                verse_keys,
                position=pbar_position,
            )
            self.stats.tafsirs_fetched += len(verse_keys) * len(self.tafsirs)
        
        if self._shutdown_requested:
            return False
        
        # Format and buffer verses
        for verse in verses:
            if self._shutdown_requested:
                return False
            
            verse_key = verse.get("verse_key", "")
            formatted = self._format_verse(
                verse=verse,
                chapter=chapter,
                tafsirs=tafsirs_map.get(verse_key),
            )
            self._add_to_buffer(formatted)
        
        self.stats.chapters_processed += 1
        return True
    
    def collect_chapters(
        self,
        chapter_numbers: list[int],
    ) -> CollectorStats:
        """
        Collect specified chapters.
        
        Args:
            chapter_numbers: List of chapter numbers to collect
            
        Returns:
            Collection statistics
        """
        # Initialize resources
        self._initialize_resources()
        
        # Fetch all chapter metadata
        logger.info("Fetching chapter metadata...")
        self._chapters_cache = self.api_client.get_chapters()
        chapters_by_id = {ch["id"]: ch for ch in self._chapters_cache}
        
        # Handle resume
        if self.resume:
            self._load_resume_state()
            complete_chapters = self._determine_complete_chapters(self._chapters_cache)
            
            # Filter out complete chapters
            original_count = len(chapter_numbers)
            chapter_numbers = [
                ch for ch in chapter_numbers
                if ch not in complete_chapters
            ]
            
            if original_count != len(chapter_numbers):
                logger.info(
                    f"Resuming: skipping {original_count - len(chapter_numbers)} "
                    f"complete chapters"
                )
        
        if not chapter_numbers:
            logger.info("No chapters to collect (all complete)")
            return self.stats
        
        # Open output file
        self._open_output_file(append=self.resume and self.output_file.exists())
        
        self.stats.translations_included = len(self.translations)
        
        # Collect chapters with progress bar
        with tqdm(
            chapter_numbers,
            desc="Chapters",
            position=0,
            unit="surah",
        ) as pbar:
            for chapter_num in pbar:
                if self._shutdown_requested:
                    logger.warning("Shutdown requested. Saving progress...")
                    break
                
                chapter = chapters_by_id.get(chapter_num)
                if not chapter:
                    logger.warning(f"Chapter {chapter_num} not found, skipping")
                    continue
                
                pbar.set_postfix({"surah": chapter.get("name_simple", "")[:15]})
                
                success = self._collect_chapter(chapter, pbar_position=1)
                if not success:
                    break
        
        # Final flush
        self._flush_buffer(force=True)
        
        # Log summary
        logger.info(
            f"Collection complete: {self.stats.chapters_processed} chapters, "
            f"{self.stats.verses_collected} verses"
        )
        
        return self.stats
    
    def collect_range(
        self,
        start: int,
        end: int,
    ) -> CollectorStats:
        """
        Collect a range of chapters.
        
        Args:
            start: Starting chapter number (1-114)
            end: Ending chapter number (1-114)
            
        Returns:
            Collection statistics
        """
        chapter_numbers = list(range(start, end + 1))
        return self.collect_chapters(chapter_numbers)
    
    def collect_all(self) -> CollectorStats:
        """
        Collect all 114 chapters.
        
        Returns:
            Collection statistics
        """
        return self.collect_range(1, 114)
    
    def collect_single(self, chapter_number: int) -> CollectorStats:
        """
        Collect a single chapter.
        
        Args:
            chapter_number: Chapter number (1-114)
            
        Returns:
            Collection statistics
        """
        return self.collect_chapters([chapter_number])
    
    def get_stats(self) -> CollectorStats:
        """Get current collection statistics."""
        return self.stats
    
    def save_errors(self, error_file: str | Path) -> None:
        """Save errors to a JSON file."""
        if not self.stats.errors:
            logger.info("No errors to save")
            return
        
        with open(error_file, "w", encoding="utf-8") as f:
            json.dump(self.stats.errors, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(self.stats.errors)} errors to {error_file}")
