from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from backend.api.deps import get_quran_api_testing_service
from backend.schemas.quran_testing import (
    QuranResourcesResponse,
    QuranVerseTestRequest,
    QuranVerseTestResponse,
)
from backend.services.quran_api_testing_service import QuranAPITestingService

router = APIRouter(prefix="/quran-testing", tags=["quran-testing"])


@router.get("/resources", response_model=QuranResourcesResponse)
def list_quran_resources(
    language: str | None = Query(default="en", min_length=2, max_length=5),
    service: QuranAPITestingService = Depends(get_quran_api_testing_service),
) -> QuranResourcesResponse:
    return QuranResourcesResponse(**service.resources(language=language))


@router.post("/verse", response_model=QuranVerseTestResponse)
def test_quran_verse(
    payload: QuranVerseTestRequest,
    service: QuranAPITestingService = Depends(get_quran_api_testing_service),
) -> QuranVerseTestResponse:
    return QuranVerseTestResponse(**service.verse_details(payload))
