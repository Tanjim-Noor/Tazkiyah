from __future__ import annotations

from fastapi import APIRouter, Depends

from backend.api.deps import get_rag_service
from backend.schemas.config import ConfigResponse
from backend.services.rag_service import RAGService

router = APIRouter(prefix="/config", tags=["config"])


@router.get("", response_model=ConfigResponse)
def config_info(service: RAGService = Depends(get_rag_service)) -> ConfigResponse:
    return ConfigResponse(**service.runtime_config())
