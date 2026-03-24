from __future__ import annotations

import asyncio
import json
import time
import urllib.request
from typing import Any

from backend.config import settings
from backend.services.rag_service import RAGService

HTTP_URL = "http://127.0.0.1:8000/api/v1/chat"
PAYLOAD = {
    "query": "Give a short reflection about patience",
    "top_k": 3,
    "temperature": 0.3,
    "return_sources": True,
}


def test_http_sse() -> dict[str, Any]:
    data = json.dumps(PAYLOAD).encode("utf-8")
    req = urllib.request.Request(
        HTTP_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    started = time.time()
    result: dict[str, Any] = {
        "status": None,
        "first_byte_seconds": None,
        "first_chunk_seconds": None,
        "first_byte": "",
        "first_chunk_preview": "",
        "error": None,
    }

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            result["status"] = resp.status
            first_byte = resp.read(1)
            result["first_byte_seconds"] = round(time.time() - started, 3)
            result["first_byte"] = first_byte.decode("utf-8", errors="replace")

            first_chunk = resp.read(255)
            result["first_chunk_seconds"] = round(time.time() - started, 3)
            result["first_chunk_preview"] = (
                first_byte + first_chunk
            ).decode("utf-8", errors="replace")
    except Exception as exc:  # noqa: BLE001
        result["error"] = repr(exc)

    return result


async def test_internal_stream() -> dict[str, Any]:
    service = RAGService(settings)
    started = time.time()
    result: dict[str, Any] = {
        "first_event_seconds": None,
        "first_event": None,
        "second_event_seconds": None,
        "second_event": None,
        "error": None,
    }

    try:
        stream = service.stream_answer(
            query=PAYLOAD["query"],
            top_k=PAYLOAD["top_k"],
            temperature=PAYLOAD["temperature"],
            return_sources=PAYLOAD["return_sources"],
        )

        first = await anext(stream)
        result["first_event_seconds"] = round(time.time() - started, 3)
        result["first_event"] = first.get("event")

        second = await anext(stream)
        result["second_event_seconds"] = round(time.time() - started, 3)
        result["second_event"] = second.get("event")
    except Exception as exc:  # noqa: BLE001
        result["error"] = repr(exc)

    return result


def main() -> None:
    print("=== INTERNAL STREAM TEST ===")
    internal = asyncio.run(test_internal_stream())
    print(json.dumps(internal, indent=2, ensure_ascii=False))

    print("\n=== HTTP SSE TEST ===")
    http = test_http_sse()
    print(json.dumps(http, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
