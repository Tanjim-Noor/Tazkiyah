from __future__ import annotations

from backend.config import Settings


def category_modifier_map(settings: Settings) -> dict[str, str]:
    return {
        settings.category_factual: (
            "Focus on precision and cite exact verse references. "
            "Keep claims tightly grounded in retrieved text."
        ),
        settings.category_emotional: (
            "Respond with empathy, reassurance, and gentle tone while remaining faithful to Quranic context. "
            "Include practical spiritual guidance."
        ),
        settings.category_creative: (
            "Use engaging, clear language and helpful analogies without inventing Quranic content. "
            "Keep meaning accurate and contextual."
        ),
    }


def build_final_prompt(*, settings: Settings, query: str, context: str, category_instruction: str) -> str:
    return (
        f"System instruction:\n{settings.base_system_prompt}\n\n"
        f"Category guidance:\n{category_instruction}\n\n"
        "Use only the context below to answer the user query. "
        "If context is insufficient, clearly say so.\n\n"
        f"Context:\n{context}\n\n"
        f"User query:\n{query}\n\n"
        "Answer with verse citations when relevant."
    )


def build_classifier_prompt(settings: Settings, query: str) -> str:
    categories = ", ".join(settings.categories)
    return (
        "Classify the user query into exactly one category. "
        "Return only the category label and nothing else.\n"
        f"Allowed categories: {categories}\n"
        f"User query: {query}"
    )
