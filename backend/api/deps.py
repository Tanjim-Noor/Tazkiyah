from __future__ import annotations

from fastapi import Request

from backend.services.quran_api_testing_service import QuranAPITestingService
from backend.services.rag_service import RAGService


def get_rag_service(request: Request) -> RAGService:
    return request.app.state.rag_service


def get_quran_api_testing_service(request: Request) -> QuranAPITestingService:
    return request.app.state.quran_api_testing_service
