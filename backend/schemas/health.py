from __future__ import annotations

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    service: str
    vectorstore_ready: bool
    llm_ready: bool
