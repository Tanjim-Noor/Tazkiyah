from __future__ import annotations

from collections.abc import AsyncIterator

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from backend.api.deps import get_rag_service
from backend.schemas.chat import ChatRequest
from backend.services.rag_service import RAGService

router = APIRouter(prefix="/chat", tags=["chat"])


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
            yield service.format_sse("error", {"message": str(exc)})

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )
