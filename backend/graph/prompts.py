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
    output_rules = (
        "Output rules:\n"
        "1) Write a natural, seamless reply to the user which is grounded in the verse and commentary from the context only.\n" 
        "4) Use only verses that appear in Context. Do not cite from memory or external sources.\n"
        "5) When you include a verse, use this exact 2-line inline format:\n"
        "   \"<exact translation text from Context>\"\n"
        "   Verse Reference: [surah:verse]\n"
        "7) If Context is insufficient, say so briefly and do not fabricate or give your own citations.\n"
    )

    return (
        f"System instruction:\n{settings.base_system_prompt}\n\n"
        f"Category guidance:\n{category_instruction}\n\n"
        f"{output_rules}\n"
        "Use only the context below to answer the user query. "
        "If context is insufficient, clearly say so.\n\n"
        f"Context:\n{context}\n\n"
        f"User query:\n{query}\n\n"
        "Answer with verse citations given in the context when relevant."
    )


def build_classifier_prompt(settings: Settings, query: str) -> str:
    categories = ", ".join(settings.categories)
    return (
        "Classify the user query into exactly one category. "
        "Return only the category label and nothing else.\n"
        f"Allowed categories: {categories}\n"
        f"User query: {query}"
    )
