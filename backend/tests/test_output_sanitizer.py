from __future__ import annotations

from backend.services.rag_service import LLMOutputSanitizer


def test_sanitize_text_removes_meta_lines_and_keeps_answer():
    raw = (
        "I hear your anxiety, and you are not alone.\n\n"
        "Wait, I must check the provided context.\n"
        "Let me re-read the prompt.\n\n"
        "\"It was thanks to Allah's mercy that you were gentle to them.\"\n"
        "Verse Reference: [3:159]\n"
    )

    cleaned = LLMOutputSanitizer().sanitize_text(raw)

    assert "I hear your anxiety" in cleaned
    assert "Verse Reference: [3:159]" in cleaned
    assert "provided context" not in cleaned.lower()
    assert "re-read the prompt" not in cleaned.lower()


def test_stream_chunk_sanitization_strips_think_block():
    sanitizer = LLMOutputSanitizer()

    chunk_1 = sanitizer.process_chunk("Before <think>internal")
    chunk_2 = sanitizer.process_chunk(" reasoning</think> after\n")
    tail = sanitizer.finalize()

    assert chunk_1 == "Before "
    assert chunk_2 == " after\n"
    assert tail == ""
