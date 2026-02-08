#!/usr/bin/env python3
"""
Tazkiyah RAG v2 - Gradio Web Chat UI

Web interface with debug panel and LangSmith integration.

Usage:
    python -m rag_v2.chat_ui
"""
import logging
import sys
import time
from datetime import datetime

import gradio as gr

from rag_v2 import config
from rag_v2.rag_pipeline import TazkiyahRAGv2

# ─── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format=config.LOG_FORMAT,
)
logger = logging.getLogger(__name__)

# ─── Debug log buffer ─────────────────────────────────────────────────────────
debug_logs: list[str] = []


def log_debug(message: str):
    """Add timestamped message to debug buffer."""
    ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    for line in message.split("\n"):
        debug_logs.append(f"[{ts}] {line}")
    logger.debug(message)
    while len(debug_logs) > 500:
        debug_logs.pop(0)


def get_debug_log_text() -> str:
    return "\n".join(debug_logs[-200:])


# ─── RAG instance ─────────────────────────────────────────────────────────────
log_debug("Initializing TazkiyahRAGv2...")

try:
    rag = TazkiyahRAGv2()
    stats = rag.get_collection_stats()
    log_debug(f"RAG v2 initialized: {stats['count']} docs in '{stats['name']}'")
    log_debug(f"  Embedding: {stats['embedding_model']}")
    log_debug(f"  LLM: {stats['llm_model']}")

    langsmith_on = (
        config.LANGSMITH_TRACING.lower() == "true" and config.LANGSMITH_API_KEY
    )
    log_debug(f"  LangSmith: {'ON (' + config.LANGSMITH_PROJECT + ')' if langsmith_on else 'OFF'}")

    if stats["count"] == 0:
        log_debug("WARNING: No documents indexed! Run: python -m rag_v2.index_data")
except Exception as e:
    log_debug(f"ERROR initializing RAG: {e}")
    rag = None


# ─── Chat functions (Gradio 6.0 dict format) ─────────────────────────────────

def user_message(user_input: str, history: list[dict]) -> tuple[str, list[dict]]:
    """Handle user submission."""
    if not user_input.strip():
        return "", history
    log_debug(f"User: {user_input[:100]}...")
    history = history + [{"role": "user", "content": user_input}]
    return "", history


def bot_response(history: list[dict]) -> tuple[list[dict], str]:
    """Generate bot response with RAG v2."""
    if not history:
        return history, get_debug_log_text()

    last_msg = history[-1]
    if last_msg.get("role") != "user":
        return history, get_debug_log_text()

    content = last_msg.get("content", "")
    if isinstance(content, list):
        user_question = " ".join(
            item.get("text", "") for item in content if isinstance(item, dict)
        )
    else:
        user_question = str(content)

    if not user_question.strip():
        return history, get_debug_log_text()

    if rag is None:
        log_debug("ERROR: RAG not initialized")
        history.append({
            "role": "assistant",
            "content": "Error: RAG system not initialized. Check logs.",
        })
        return history, get_debug_log_text()

    stats = rag.get_collection_stats()
    if stats["count"] == 0:
        history.append({
            "role": "assistant",
            "content": "No documents indexed. Run:\n```\npython -m rag_v2.index_data\n```",
        })
        return history, get_debug_log_text()

    def rag_debug_callback(step: str, data: str):
        log_debug(f"[{step}]\n{data}")

    log_debug("=" * 60)
    log_debug("RAG v2 PIPELINE START")
    log_debug("=" * 60)
    start_time = time.time()

    try:
        result = rag.query(
            user_question,
            return_sources=True,
            debug_callback=rag_debug_callback,
        )
        elapsed = time.time() - start_time
        log_debug("=" * 60)
        log_debug(f"RAG v2 PIPELINE COMPLETE ({elapsed:.2f}s)")
        log_debug("=" * 60)

        answer = result["result"]

        # Append source references
        if config.SHOW_SOURCES and "source_documents" in result and result["source_documents"]:
            sources = result["source_documents"]
            scores = result.get("scores", [])

            answer += "\n\n---\n**Sources:**\n"
            for i, doc in enumerate(sources[: config.MAX_SOURCES_DISPLAY], 1):
                meta = doc.metadata
                verse_key = meta.get("verse_key", "?")
                surah = meta.get("surah_name", "")
                score = scores[i - 1] if i - 1 < len(scores) else 0
                answer += f"- Verse {verse_key} ({surah}) [score: {score:.4f}]\n"

        history.append({"role": "assistant", "content": answer})

    except Exception as e:
        log_debug(f"ERROR in RAG query: {e}")
        logger.exception("RAG query failed")
        history.append({"role": "assistant", "content": f"Error: {str(e)}"})

    return history, get_debug_log_text()


def clear_chat() -> tuple[list[dict], str]:
    global debug_logs
    debug_logs = []
    log_debug("Chat and logs cleared")
    return [], get_debug_log_text()


def refresh_debug_logs() -> str:
    return get_debug_log_text()


# ─── Build Gradio UI ─────────────────────────────────────────────────────────

def build_ui() -> gr.Blocks:
    """Build the Gradio 6.0 web interface."""

    langsmith_on = (
        config.LANGSMITH_TRACING.lower() == "true"
        and config.LANGSMITH_API_KEY
        and config.LANGSMITH_API_KEY != "your-langsmith-api-key-here"
    )
    langsmith_badge = "ON" if langsmith_on else "OFF"

    with gr.Blocks(
        title="Tazkiyah RAG v2",
        theme=gr.themes.Soft(),
    ) as demo:
        gr.Markdown(
            f"# Tazkiyah RAG v2\n"
            f"Quranic knowledge assistant — LangChain + Ollama + LangSmith\n\n"
            f"**LLM:** `{config.LLM_MODEL}` | "
            f"**Embedding:** `{config.EMBEDDING_MODEL}` | "
            f"**LangSmith:** `{langsmith_badge}`"
        )

        with gr.Row():
            # Chat column
            with gr.Column(scale=3):
                chatbot = gr.Chatbot(
                    type="messages",
                    height=500,
                    label="Chat",
                    show_copy_button=True,
                )
                with gr.Row():
                    msg_input = gr.Textbox(
                        placeholder="Ask about the Quran...",
                        show_label=False,
                        scale=5,
                        container=False,
                    )
                    send_btn = gr.Button("Send", variant="primary", scale=1)

                with gr.Row():
                    clear_btn = gr.Button("Clear Chat", size="sm")

            # Debug column
            with gr.Column(scale=2):
                debug_box = gr.Textbox(
                    label="Debug Logs (RAG Pipeline)",
                    lines=25,
                    max_lines=30,
                    interactive=False,
                    value=get_debug_log_text,
                )
                refresh_btn = gr.Button("Refresh Logs", size="sm")

        # Wire events
        msg_input.submit(
            user_message,
            inputs=[msg_input, chatbot],
            outputs=[msg_input, chatbot],
        ).then(
            bot_response,
            inputs=[chatbot],
            outputs=[chatbot, debug_box],
        )

        send_btn.click(
            user_message,
            inputs=[msg_input, chatbot],
            outputs=[msg_input, chatbot],
        ).then(
            bot_response,
            inputs=[chatbot],
            outputs=[chatbot, debug_box],
        )

        clear_btn.click(clear_chat, outputs=[chatbot, debug_box])
        refresh_btn.click(refresh_debug_logs, outputs=[debug_box])

    return demo


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    demo = build_ui()
    demo.launch(
        server_name=config.UI_SERVER_HOST,
        server_port=config.UI_SERVER_PORT,
        share=config.UI_SHARE,
    )


if __name__ == "__main__":
    main()
