from __future__ import annotations

import logging
from collections.abc import AsyncIterator

from fastapi import APIRouter, Depends
from fastapi import HTTPException
from fastapi.responses import StreamingResponse

from backend.api.deps import get_rag_service
from backend.schemas.chat import ChatRequest
from backend.services.rag_service import RAGService

router = APIRouter(prefix="/chat", tags=["chat"])
logger = logging.getLogger(__name__)


@router.post("", response_class=StreamingResponse)
async def chat_stream(
    payload: ChatRequest,
    service: RAGService = Depends(get_rag_service),
) -> StreamingResponse:
    async def event_generator() -> AsyncIterator[str]:
        try:
            async for item in service.stream_answer(
                query=payload.query,
                top_k=payload.top_k,
                temperature=payload.temperature,
                return_sources=payload.return_sources,
            ):
                yield service.format_sse(item["event"], item["data"])
        except Exception as exc:
            logger.exception("Streaming chat request failed")
            yield service.format_sse("error", {"message": str(exc)})

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )


@router.post("/sync")
def chat_sync(
    payload: ChatRequest,
    service: RAGService = Depends(get_rag_service),
) -> dict:
    """Non-streaming endpoint for clients that do not support SSE (Swagger, simple REST)."""
    try:
        return service.answer(
            query=payload.query,
            top_k=payload.top_k,
            temperature=payload.temperature,
            return_sources=payload.return_sources,
        )
    except Exception as exc:
        logger.exception("Sync chat request failed")
        raise HTTPException(
            status_code=503,
            detail={
                "message": "Chat backend is unavailable",
                "reason": str(exc),
            },
        ) from exc
