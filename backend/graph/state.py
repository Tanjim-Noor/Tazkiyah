from __future__ import annotations

from typing import Any

from langchain_core.documents import Document
from typing_extensions import NotRequired, TypedDict


class GraphState(TypedDict):
    query: str
    category: NotRequired[str]
    retrieval_query: NotRequired[str]
    category_instruction: NotRequired[str]
    documents: NotRequired[list[Document]]
    scores: NotRequired[list[float]]
    context: NotRequired[str]
    final_prompt: NotRequired[str]
    diagnostics: NotRequired[dict[str, Any]]
