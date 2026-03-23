from __future__ import annotations

from fastapi import APIRouter, Depends

from backend.api.deps import get_rag_service
from backend.schemas.health import HealthResponse
from backend.services.rag_service import RAGService

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health(service: RAGService = Depends(get_rag_service)) -> HealthResponse:
    return HealthResponse(**service.health())
