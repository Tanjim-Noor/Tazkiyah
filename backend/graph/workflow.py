from __future__ import annotations

import os
from typing import Any

from langgraph.graph import END, START, StateGraph
from langsmith import traceable

from backend.config import Settings
from backend.graph.prompts import (
    build_classifier_prompt,
    build_final_prompt,
    category_modifier_map,
)
from backend.graph.state import GraphState


def _normalize_category(raw: str, settings: Settings) -> str:
    value = (raw or "").strip().lower()
    mapping = {
        settings.category_factual.lower(): settings.category_factual,
        settings.category_emotional.lower(): settings.category_emotional,
        settings.category_creative.lower(): settings.category_creative,
        "factual": settings.category_factual,
        "informational": settings.category_factual,
        "emotional": settings.category_emotional,
        "empathetic": settings.category_emotional,
        "creative": settings.category_creative,
    }
    return mapping.get(value, settings.category_factual)


def configure_langsmith_environment(settings: Settings) -> None:
    os.environ["LANGSMITH_TRACING"] = "true" if settings.langsmith_tracing else "false"
    os.environ["LANGSMITH_PROJECT"] = settings.langsmith_project
    os.environ["LANGSMITH_ENDPOINT"] = settings.langsmith_endpoint
    if settings.langsmith_api_key:
        os.environ["LANGSMITH_API_KEY"] = settings.langsmith_api_key


def build_orchestration_graph(settings: Settings, *, llm_adapter, vector_adapter):
    modifiers = category_modifier_map(settings)

    @traceable(name="classify_query")
    def classify_query(state: GraphState) -> dict[str, Any]:
        prompt = build_classifier_prompt(settings, state["query"])
        raw_category = llm_adapter.invoke(prompt, temperature=0.0)
        category = _normalize_category(raw_category, settings)
        return {
            "category": category,
            "diagnostics": {"raw_category": raw_category.strip()},
        }

    @traceable(name="prompt_engineer")
    def prompt_engineer(state: GraphState) -> dict[str, Any]:
        category = state.get("category", settings.category_factual)
        instruction = modifiers.get(category, modifiers[settings.category_factual])
        retrieval_query = (
            f"Category: {category}. Intent guidance: {instruction}. User query: {state['query']}"
        )
        return {
            "category_instruction": instruction,
            "retrieval_query": retrieval_query,
        }

    @traceable(name="retrieve_context")
    def retrieve_context(state: GraphState) -> dict[str, Any]:
        results = vector_adapter.similarity_search_with_score(
            state.get("retrieval_query", state["query"]),
            k=settings.top_k,
        )
        docs = [doc for doc, _ in results]
        scores = [float(score) for _, score in results]
        context = "\n\n---\n\n".join(doc.page_content for doc in docs)
        return {
            "documents": docs,
            "scores": scores,
            "context": context,
        }

    @traceable(name="finalize_prompt")
    def finalize_prompt(state: GraphState) -> dict[str, Any]:
        final_prompt = build_final_prompt(
            settings=settings,
            query=state["query"],
            context=state.get("context", ""),
            category_instruction=state.get("category_instruction", ""),
        )
        return {"final_prompt": final_prompt}

    def route_by_category(state: GraphState) -> str:
        category = state.get("category", settings.category_factual)
        if category == settings.category_emotional:
            return "emotional"
        if category == settings.category_creative:
            return "creative"
        return "factual"

    graph = StateGraph(GraphState)
    graph.add_node("classify", classify_query)
    graph.add_node("factual", prompt_engineer)
    graph.add_node("emotional", prompt_engineer)
    graph.add_node("creative", prompt_engineer)
    graph.add_node("retrieve", retrieve_context)
    graph.add_node("finalize", finalize_prompt)

    graph.add_edge(START, "classify")
    graph.add_conditional_edges(
        "classify",
        route_by_category,
        {
            "factual": "factual",
            "emotional": "emotional",
            "creative": "creative",
        },
    )
    graph.add_edge("factual", "retrieve")
    graph.add_edge("emotional", "retrieve")
    graph.add_edge("creative", "retrieve")
    graph.add_edge("retrieve", "finalize")
    graph.add_edge("finalize", END)

    return graph.compile()
