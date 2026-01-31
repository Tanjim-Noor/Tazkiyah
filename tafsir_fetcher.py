"""
Parallel Tafsir Fetcher

Fetches tafsir content for verses using ThreadPoolExecutor.
Respects the circuit breaker state from the API client.

Author: Tazkiyah Project
"""

import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import Any

from tqdm import tqdm

from quran_api import QuranAPIClient

# Configure module logger
logger = logging.getLogger(__name__)


@dataclass
class TafsirResult:
    """Result of a tafsir fetch operation."""
    
    verse_key: str
    tafsir_id: int
    tafsir_name: str
    text: str | None
    success: bool
    error: str | None = None


class TafsirFetcher:
    """
    Parallel tafsir fetcher using ThreadPoolExecutor.
    
    Features:
    - Configurable concurrency (1-10 threads)
    - Respects circuit breaker state from API client
    - Graceful degradation on errors
    - Progress tracking with tqdm
    
    Example:
        >>> client = QuranAPIClient()
        >>> fetcher = TafsirFetcher(client, tafsir_ids=[169])
        >>> results = fetcher.fetch_for_verses(["1:1", "1:2", "1:3"])
    """
    
    MIN_CONCURRENCY = 1
    MAX_CONCURRENCY = 10
    
    def __init__(
        self,
        api_client: QuranAPIClient,
        tafsir_ids: list[int],
        tafsir_names: dict[int, str] | None = None,
        concurrency: int = 3,
        show_progress: bool = True,
    ) -> None:
        """
        Initialize the tafsir fetcher.
        
        Args:
            api_client: QuranAPIClient instance (shared, thread-safe)
            tafsir_ids: List of tafsir IDs to fetch
            tafsir_names: Optional mapping of tafsir ID to name
            concurrency: Number of parallel threads (1-10)
            show_progress: Whether to show progress bar
        """
        self.api_client = api_client
        self.tafsir_ids = tafsir_ids
        self.tafsir_names = tafsir_names or {}
        self.show_progress = show_progress
        
        # Clamp concurrency to valid range
        self._initial_concurrency = max(
            self.MIN_CONCURRENCY,
            min(concurrency, self.MAX_CONCURRENCY)
        )
        
        # Statistics
        self.stats = {
            "total_requests": 0,
            "successful": 0,
            "failed": 0,
            "not_found": 0,
        }
        
        logger.info(
            f"TafsirFetcher initialized: tafsirs={tafsir_ids}, "
            f"concurrency={self._initial_concurrency}"
        )
    
    def _get_current_concurrency(self) -> int:
        """Get current concurrency from API client (respects circuit breaker)."""
        client_concurrency = self.api_client.get_concurrency()
        return max(
            self.MIN_CONCURRENCY,
            min(client_concurrency, self._initial_concurrency)
        )
    
    def _fetch_single_tafsir(
        self,
        verse_key: str,
        tafsir_id: int,
    ) -> TafsirResult:
        """
        Fetch a single tafsir for a verse.
        
        Args:
            verse_key: Verse key (e.g., "2:255")
            tafsir_id: Tafsir resource ID
            
        Returns:
            TafsirResult with success/failure status
        """
        tafsir_name = self.tafsir_names.get(tafsir_id, f"Tafsir {tafsir_id}")
        
        try:
            tafsir = self.api_client.get_tafsir_by_ayah(tafsir_id, verse_key)
            
            if tafsir is None:
                self.stats["not_found"] += 1
                return TafsirResult(
                    verse_key=verse_key,
                    tafsir_id=tafsir_id,
                    tafsir_name=tafsir_name,
                    text=None,
                    success=True,  # Not found is not an error
                    error=None,
                )
            
            self.stats["successful"] += 1
            return TafsirResult(
                verse_key=verse_key,
                tafsir_id=tafsir_id,
                tafsir_name=tafsir_name,
                text=tafsir.get("text", ""),
                success=True,
                error=None,
            )
            
        except Exception as e:
            self.stats["failed"] += 1
            logger.warning(f"Failed to fetch tafsir {tafsir_id} for {verse_key}: {e}")
            return TafsirResult(
                verse_key=verse_key,
                tafsir_id=tafsir_id,
                tafsir_name=tafsir_name,
                text=None,
                success=False,
                error=str(e),
            )
        finally:
            self.stats["total_requests"] += 1
    
    def fetch_for_verse(self, verse_key: str) -> dict[str, str | None]:
        """
        Fetch all tafsirs for a single verse (sequential).
        
        Args:
            verse_key: Verse key (e.g., "2:255")
            
        Returns:
            Dictionary mapping tafsir name to text (or None if not found)
        """
        result: dict[str, str | None] = {}
        
        for tafsir_id in self.tafsir_ids:
            tafsir_result = self._fetch_single_tafsir(verse_key, tafsir_id)
            result[tafsir_result.tafsir_name] = tafsir_result.text
        
        return result
    
    def fetch_for_verses(
        self,
        verse_keys: list[str],
        position: int = 1,
    ) -> dict[str, dict[str, str | None]]:
        """
        Fetch tafsirs for multiple verses in parallel.
        
        Args:
            verse_keys: List of verse keys
            position: Progress bar position (for nested bars)
            
        Returns:
            Dictionary mapping verse_key to tafsir results
        """
        if not self.tafsir_ids:
            return {vk: {} for vk in verse_keys}
        
        results: dict[str, dict[str, str | None]] = {vk: {} for vk in verse_keys}
        
        # Create all tasks: (verse_key, tafsir_id) pairs
        tasks = [
            (verse_key, tafsir_id)
            for verse_key in verse_keys
            for tafsir_id in self.tafsir_ids
        ]
        
        if not tasks:
            return results
        
        # Get current concurrency (may be reduced by circuit breaker)
        concurrency = self._get_current_concurrency()
        
        logger.debug(
            f"Fetching tafsirs for {len(verse_keys)} verses "
            f"({len(tasks)} requests, concurrency={concurrency})"
        )
        
        # Use ThreadPoolExecutor for parallel fetching
        with ThreadPoolExecutor(max_workers=concurrency) as executor:
            # Submit all tasks
            future_to_task = {
                executor.submit(self._fetch_single_tafsir, vk, tid): (vk, tid)
                for vk, tid in tasks
            }
            
            # Process completed tasks with progress bar
            iterator = as_completed(future_to_task)
            
            if self.show_progress:
                iterator = tqdm(
                    iterator,
                    total=len(tasks),
                    desc="Fetching tafsirs",
                    position=position,
                    leave=False,
                    unit="tafsir",
                )
            
            for future in iterator:
                verse_key, tafsir_id = future_to_task[future]
                
                try:
                    tafsir_result = future.result()
                    results[verse_key][tafsir_result.tafsir_name] = tafsir_result.text
                except Exception as e:
                    logger.error(f"Unexpected error fetching {tafsir_id} for {verse_key}: {e}")
                    tafsir_name = self.tafsir_names.get(tafsir_id, f"Tafsir {tafsir_id}")
                    results[verse_key][tafsir_name] = None
        
        return results
    
    def fetch_for_verses_batch(
        self,
        verses: list[dict[str, Any]],
        position: int = 1,
    ) -> list[dict[str, Any]]:
        """
        Fetch tafsirs and add them to verse dictionaries.
        
        Args:
            verses: List of verse dictionaries (must have 'verse_key')
            position: Progress bar position
            
        Returns:
            Same verses with 'tafsirs' field added
        """
        if not self.tafsir_ids:
            # No tafsirs requested, just add empty dict
            for verse in verses:
                verse["tafsirs"] = {}
            return verses
        
        # Extract verse keys
        verse_keys = [v.get("verse_key") for v in verses if v.get("verse_key")]
        
        # Fetch all tafsirs
        tafsir_results = self.fetch_for_verses(verse_keys, position=position)
        
        # Add tafsirs to verses
        for verse in verses:
            verse_key = verse.get("verse_key")
            if verse_key:
                verse["tafsirs"] = tafsir_results.get(verse_key, {})
        
        return verses
    
    def get_stats(self) -> dict[str, int]:
        """Get fetching statistics."""
        return self.stats.copy()
    
    def reset_stats(self) -> None:
        """Reset statistics counters."""
        self.stats = {
            "total_requests": 0,
            "successful": 0,
            "failed": 0,
            "not_found": 0,
        }
