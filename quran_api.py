"""
Quran Foundation API Client

A thread-safe HTTP client for the Quran Foundation API with:
- Connection pooling via requests.Session
- Automatic retry logic with exponential backoff
- Circuit breaker pattern for rate limit protection
- Configurable delays between requests

Author: Tazkiyah Project
"""

import logging
import threading
import time
from dataclasses import dataclass, field
from typing import Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

# Configure module logger
logger = logging.getLogger(__name__)


@dataclass
class CircuitBreakerState:
    """Thread-safe circuit breaker state management."""
    
    consecutive_failures: int = 0
    is_open: bool = False
    last_failure_time: float = 0.0
    current_concurrency: int = 3
    original_concurrency: int = 3
    
    # Configuration
    failure_threshold: int = 5
    pause_duration: float = 60.0
    concurrency_reduction_factor: float = 0.5
    
    # Thread safety
    _lock: threading.Lock = field(default_factory=threading.Lock)
    
    def record_success(self) -> None:
        """Record a successful request, reset failure count."""
        with self._lock:
            self.consecutive_failures = 0
            self.is_open = False
    
    def record_failure(self) -> bool:
        """
        Record a failed request (429 rate limit).
        
        Returns:
            bool: True if circuit breaker should trip (threshold reached)
        """
        with self._lock:
            self.consecutive_failures += 1
            self.last_failure_time = time.time()
            
            if self.consecutive_failures >= self.failure_threshold:
                self.is_open = True
                return True
            return False
    
    def should_allow_request(self) -> bool:
        """Check if requests should be allowed through."""
        with self._lock:
            if not self.is_open:
                return True
            
            # Check if pause duration has elapsed
            elapsed = time.time() - self.last_failure_time
            if elapsed >= self.pause_duration:
                self.is_open = False
                self.consecutive_failures = 0
                return True
            
            return False
    
    def reduce_concurrency(self) -> int:
        """
        Reduce concurrency after circuit breaker trips.
        
        Returns:
            int: New concurrency level
        """
        with self._lock:
            new_concurrency = max(
                1, 
                int(self.current_concurrency * self.concurrency_reduction_factor)
            )
            old_concurrency = self.current_concurrency
            self.current_concurrency = new_concurrency
            logger.warning(
                f"Rate limited. Pausing {self.pause_duration}s. "
                f"Reducing concurrency {old_concurrency}→{new_concurrency}"
            )
            return new_concurrency
    
    def get_concurrency(self) -> int:
        """Get current concurrency level."""
        with self._lock:
            return self.current_concurrency
    
    def reset(self) -> None:
        """Reset circuit breaker to initial state."""
        with self._lock:
            self.consecutive_failures = 0
            self.is_open = False
            self.current_concurrency = self.original_concurrency


class QuranAPIClient:
    """
    Thread-safe client for the Quran Foundation API.
    
    Features:
    - Connection pooling for efficient HTTP requests
    - Automatic retries on 502, 503, 504 errors
    - Rate limiting with configurable delay
    - Circuit breaker for 429 rate limit protection
    
    Example:
        >>> client = QuranAPIClient()
        >>> chapters = client.get_chapters()
        >>> verses = client.get_verses_by_chapter(1, translations=[131, 85])
    """
    
    BASE_URL = "https://api.quran.com"
    API_VERSION = "v4"
    
    def __init__(
        self,
        base_url: str | None = None,
        rate_limit_delay: float = 0.3,
        timeout: tuple[float, float] = (5.0, 30.0),
        max_retries: int = 3,
        concurrency: int = 3,
        circuit_breaker_threshold: int = 5,
        circuit_breaker_pause: float = 60.0,
    ) -> None:
        """
        Initialize the Quran API client.
        
        Args:
            base_url: API base URL (default: pre-production endpoint)
            rate_limit_delay: Minimum seconds between requests (default: 0.3)
            timeout: (connect_timeout, read_timeout) in seconds
            max_retries: Maximum retry attempts for 5xx errors
            concurrency: Initial concurrency level for parallel operations
            circuit_breaker_threshold: Consecutive 429s before tripping
            circuit_breaker_pause: Seconds to pause when circuit breaker trips
        """
        self.base_url = (base_url or self.BASE_URL).rstrip("/")
        self.rate_limit_delay = rate_limit_delay
        self.timeout = timeout
        
        # Thread-safe state
        self._last_request_time: float = 0.0
        self._request_lock = threading.Lock()
        
        # Circuit breaker
        self.circuit_breaker = CircuitBreakerState(
            failure_threshold=circuit_breaker_threshold,
            pause_duration=circuit_breaker_pause,
            current_concurrency=concurrency,
            original_concurrency=concurrency,
        )
        
        # Configure session with retry logic
        self._session = self._create_session(max_retries)
        
        logger.info(
            f"QuranAPIClient initialized: base_url={self.base_url}, "
            f"delay={rate_limit_delay}s, concurrency={concurrency}"
        )
    
    def _create_session(self, max_retries: int) -> requests.Session:
        """Create a requests session with retry configuration."""
        session = requests.Session()
        
        # Configure retry strategy for 5xx errors (not 429 - handled by circuit breaker)
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=0.5,
            status_forcelist=[502, 503, 504],
            allowed_methods=["GET"],
            raise_on_status=False,  # Don't raise, let us handle
        )
        
        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=10,
            pool_maxsize=10,
        )
        
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        
        # Set default headers
        session.headers.update({
            "Accept": "application/json",
            "User-Agent": "Tazkiyah-QuranCollector/1.0",
        })
        
        return session
    
    def _enforce_rate_limit(self) -> None:
        """Enforce minimum delay between requests (thread-safe)."""
        with self._request_lock:
            elapsed = time.time() - self._last_request_time
            if elapsed < self.rate_limit_delay:
                sleep_time = self.rate_limit_delay - elapsed
                time.sleep(sleep_time)
            self._last_request_time = time.time()
    
    def _wait_for_circuit_breaker(self) -> None:
        """Wait if circuit breaker is open."""
        while not self.circuit_breaker.should_allow_request():
            remaining = (
                self.circuit_breaker.pause_duration - 
                (time.time() - self.circuit_breaker.last_failure_time)
            )
            if remaining > 0:
                logger.info(f"Circuit breaker open. Waiting {remaining:.1f}s...")
                time.sleep(min(remaining, 5.0))  # Check every 5s
    
    def _request(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Make an API request with rate limiting and circuit breaker.
        
        Args:
            endpoint: API endpoint path (e.g., "/content/api/v4/chapters")
            params: Query parameters
            
        Returns:
            JSON response as dictionary
            
        Raises:
            requests.HTTPError: On non-recoverable HTTP errors
            requests.RequestException: On network errors
        """
        # Wait for circuit breaker if needed
        self._wait_for_circuit_breaker()
        
        # Enforce rate limit
        self._enforce_rate_limit()
        
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self._session.get(
                url,
                params=params,
                timeout=self.timeout,
            )
            
            # Handle rate limiting (429)
            if response.status_code == 429:
                should_trip = self.circuit_breaker.record_failure()
                if should_trip:
                    self.circuit_breaker.reduce_concurrency()
                    time.sleep(self.circuit_breaker.pause_duration)
                else:
                    # Exponential backoff for individual 429
                    backoff = 2 ** self.circuit_breaker.consecutive_failures
                    logger.warning(f"Rate limited (429). Backing off {backoff}s...")
                    time.sleep(backoff)
                
                # Retry the request
                return self._request(endpoint, params)
            
            # Success - reset circuit breaker
            if response.ok:
                self.circuit_breaker.record_success()
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.Timeout as e:
            logger.error(f"Request timeout: {url}")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {url} - {e}")
            raise
    
    def get_chapters(self, language: str = "en") -> list[dict[str, Any]]:
        """
        Get all 114 chapters with metadata.
        
        Args:
            language: Language for translated names (default: "en")
            
        Returns:
            List of chapter dictionaries
        """
        endpoint = f"/api/{self.API_VERSION}/chapters"
        response = self._request(endpoint, params={"language": language})
        return response.get("chapters", [])
    
    def get_chapter(self, chapter_number: int, language: str = "en") -> dict[str, Any]:
        """
        Get a specific chapter by number.
        
        Args:
            chapter_number: Chapter number (1-114)
            language: Language for translated names
            
        Returns:
            Chapter dictionary
        """
        endpoint = f"/api/{self.API_VERSION}/chapters/{chapter_number}"
        response = self._request(endpoint, params={"language": language})
        return response.get("chapter", {})
    
    def get_verses_by_chapter(
        self,
        chapter_number: int,
        translations: list[int] | None = None,
        page: int = 1,
        per_page: int = 50,
        language: str = "en",
        fields: list[str] | None = None,
    ) -> dict[str, Any]:
        """
        Get verses for a chapter with optional translations.
        
        Args:
            chapter_number: Chapter number (1-114)
            translations: List of translation IDs to include
            page: Page number for pagination
            per_page: Results per page (max 50)
            language: Language code
            fields: Specific verse fields to include
            
        Returns:
            Dictionary with 'verses' list and 'pagination' info
        """
        endpoint = f"/api/{self.API_VERSION}/verses/by_chapter/{chapter_number}"
        
        params: dict[str, Any] = {
            "language": language,
            "page": page,
            "per_page": min(per_page, 50),  # API max is 50
        }
        
        if translations:
            params["translations"] = ",".join(map(str, translations))
        
        if fields:
            params["fields"] = ",".join(fields)
        
        return self._request(endpoint, params=params)
    
    def get_all_verses_by_chapter(
        self,
        chapter_number: int,
        translations: list[int] | None = None,
        per_page: int = 50,
        fields: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get ALL verses for a chapter, handling pagination automatically.
        
        Args:
            chapter_number: Chapter number (1-114)
            translations: List of translation IDs to include
            per_page: Results per page (max 50)
            fields: Verse fields to include (default includes text_uthmani)
            
        Returns:
            Complete list of verses for the chapter
        """
        all_verses: list[dict[str, Any]] = []
        page = 1
        
        # Default fields to include Arabic text
        if fields is None:
            fields = ["text_uthmani"]
        
        while True:
            response = self.get_verses_by_chapter(
                chapter_number=chapter_number,
                translations=translations,
                page=page,
                per_page=per_page,
                fields=fields,
            )
            
            verses = response.get("verses", [])
            all_verses.extend(verses)
            
            pagination = response.get("pagination", {})
            next_page = pagination.get("next_page")
            
            if next_page is None:
                break
            
            page = next_page
        
        return all_verses
    
    def get_tafsir_by_ayah(
        self,
        tafsir_id: int,
        verse_key: str,
    ) -> dict[str, Any] | None:
        """
        Get tafsir for a specific verse.
        
        Args:
            tafsir_id: Tafsir resource ID
            verse_key: Verse key in format "chapter:verse" (e.g., "2:255")
            
        Returns:
            Tafsir dictionary or None if not found
        """
        endpoint = f"/api/{self.API_VERSION}/tafsirs/{tafsir_id}/by_ayah/{verse_key}"
        
        try:
            response = self._request(endpoint)
            return response.get("tafsir")
        except requests.HTTPError as e:
            if e.response is not None and e.response.status_code == 404:
                logger.debug(f"Tafsir not found: {tafsir_id} for {verse_key}")
                return None
            raise
    
    def get_translations_list(self, language: str | None = None) -> list[dict[str, Any]]:
        """
        Get list of available translations.
        
        Args:
            language: Filter by language code (optional)
            
        Returns:
            List of translation resource dictionaries
        """
        endpoint = f"/api/{self.API_VERSION}/resources/translations"
        params = {"language": language} if language else {}
        response = self._request(endpoint, params=params)
        return response.get("translations", [])
    
    def get_tafsirs_list(self, language: str | None = None) -> list[dict[str, Any]]:
        """
        Get list of available tafsirs.
        
        Args:
            language: Filter by language code (optional)
            
        Returns:
            List of tafsir resource dictionaries
        """
        endpoint = f"/api/{self.API_VERSION}/resources/tafsirs"
        params = {"language": language} if language else {}
        response = self._request(endpoint, params=params)
        return response.get("tafsirs", [])
    
    def get_concurrency(self) -> int:
        """Get current concurrency level (may be reduced by circuit breaker)."""
        return self.circuit_breaker.get_concurrency()
    
    def close(self) -> None:
        """Close the HTTP session."""
        self._session.close()
        logger.info("QuranAPIClient session closed")
    
    def __enter__(self) -> "QuranAPIClient":
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()


# Module-level convenience functions
_default_client: QuranAPIClient | None = None


def get_client(**kwargs) -> QuranAPIClient:
    """Get or create a default API client instance."""
    global _default_client
    if _default_client is None:
        _default_client = QuranAPIClient(**kwargs)
    return _default_client


def close_client() -> None:
    """Close the default client if it exists."""
    global _default_client
    if _default_client is not None:
        _default_client.close()
        _default_client = None
