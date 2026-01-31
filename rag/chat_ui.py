#!/usr/bin/env python3
"""
Tazkiyah Chat UI - Gradio 6.0 Web Interface

Based on Context7 documentation for Gradio 6.0:
- Message format: {"role": "user/assistant", "content": "..."}
- NO tuple format (removed in 6.0)

Usage:
    python -m rag.chat_ui
"""
import logging
import sys
import time
from datetime import datetime

import gradio as gr

from rag.rag_pipeline import TazkiyahRAG
from rag import config

# ============================================================================
# Logging Setup
# ============================================================================
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format=config.LOG_FORMAT,
)
logger = logging.getLogger(__name__)


# ============================================================================
# Global State
# ============================================================================
# Debug log buffer for UI display
debug_logs: list[str] = []


def log_debug(message: str):
    """Add timestamped message to debug log."""
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    # Split multi-line messages for better formatting
    for line in message.split("\n"):
        entry = f"[{timestamp}] {line}"
        debug_logs.append(entry)
    logger.debug(message)
    # Keep last 500 entries for detailed pipeline logs
    while len(debug_logs) > 500:
        debug_logs.pop(0)


def get_debug_log_text() -> str:
    """Get debug logs as text."""
    return "\n".join(debug_logs[-200:])  # Show last 200 lines


# ============================================================================
# RAG Instance
# ============================================================================
log_debug("Initializing TazkiyahRAG...")

try:
    rag = TazkiyahRAG()
    stats = rag.get_collection_stats()
    log_debug(f"RAG initialized: {stats['count']} documents in {stats['name']}")
    
    if stats["count"] == 0:
        log_debug("WARNING: No documents indexed!")
except Exception as e:
    log_debug(f"ERROR initializing RAG: {e}")
    rag = None


# ============================================================================
# Chat Functions (Gradio 6.0 format)
# ============================================================================
def user_message(user_input: str, history: list[dict]) -> tuple[str, list[dict]]:
    """
    Handle user message submission.
    
    Gradio 6.0 format: history is list of {"role": "...", "content": "..."}
    """
    if not user_input.strip():
        return "", history
    
    log_debug(f"User: {user_input[:100]}...")
    
    # Add user message to history (Gradio 6.0 dict format)
    history = history + [{"role": "user", "content": user_input}]
    
    return "", history


def bot_response(history: list[dict]) -> tuple[list[dict], str]:
    """
    Generate bot response.
    
    Gradio 6.0 format: Append {"role": "assistant", "content": "..."} to history.
    Returns (updated_history, debug_logs_text)
    """
    if not history:
        return history, get_debug_log_text()
    
    # Get last user message
    last_msg = history[-1]
    if last_msg.get("role") != "user":
        return history, get_debug_log_text()
    
    # Extract text from content (Gradio 6.0 can pass list of dicts or plain string)
    content = last_msg.get("content", "")
    if isinstance(content, list):
        # Gradio 6.0 multimodal format: [{"text": "...", "type": "text"}, ...]
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
            "content": "❌ Error: RAG system not initialized. Please check the logs."
        })
        return history, get_debug_log_text()
    
    # Check for indexed documents
    stats = rag.get_collection_stats()
    if stats["count"] == 0:
        log_debug("ERROR: No documents indexed")
        history.append({
            "role": "assistant",
            "content": "⚠️ No documents indexed yet. Run:\n```\npython -m rag.index_chunks fatiha.chunks.jsonl\n```"
        })
        return history, get_debug_log_text()
    
    # Debug callback to capture each RAG step
    def rag_debug_callback(step: str, data: str):
        log_debug(f"[{step}]\n{data}")
    
    # Query RAG with debug callback
    log_debug("=" * 60)
    log_debug("RAG PIPELINE START")
    log_debug("=" * 60)
    start_time = time.time()
    
    try:
        result = rag.query(
            user_question, 
            return_sources=True,
            debug_callback=rag_debug_callback
        )
        elapsed = time.time() - start_time
        log_debug("=" * 60)
        log_debug(f"RAG PIPELINE COMPLETE ({elapsed:.2f}s)")
        log_debug("=" * 60)
        
        # Build response with sources and scores
        answer = result["result"]
        
        # Add source references with scores (if enabled in config)
        if config.SHOW_SOURCES and "source_documents" in result and result["source_documents"]:
            sources = result["source_documents"]
            scores = result.get("scores", [])
            
            answer += "\n\n---\n**Sources:**\n"
            for i, doc in enumerate(sources[:config.MAX_SOURCES_DISPLAY], 1):
                meta = doc.metadata
                verse_key = meta.get("verse_key", "?")
                surah = meta.get("surah_name", "")
                score = scores[i-1] if i-1 < len(scores) else 0
                answer += f"- Verse {verse_key} ({surah}) [score: {score:.4f}]\n"
        
        # Append assistant message (Gradio 6.0 dict format)
        history.append({"role": "assistant", "content": answer})
        
    except Exception as e:
        log_debug(f"ERROR in RAG query: {e}")
        logger.exception("RAG query failed")
        history.append({
            "role": "assistant",
            "content": f"❌ Error: {str(e)}"
        })
    
    return history, get_debug_log_text()


def clear_chat() -> tuple[list[dict], str]:
    """Clear chat history and debug logs."""
    global debug_logs
    debug_logs = []
    log_debug("Chat and logs cleared")
    return [], get_debug_log_text()


def refresh_debug_logs() -> str:
    """Return current debug logs."""
    return get_debug_log_text()


# ============================================================================
# Gradio UI (Gradio 6.0 compatible)
# ============================================================================
def create_ui() -> gr.Blocks:
    """
    Create Gradio 6.0 compatible chat interface.
    
    From Context7: Use gr.Blocks with explicit component setup.
    Message format is dict with 'role' and 'content'.
    """
    with gr.Blocks(title="Tazkiyah Chat") as demo:
        gr.Markdown("""
        # 📖 Tazkiyah Chat
        ### Quranic Knowledge Assistant
        
        Ask questions about the Quran and get AI-powered answers based on authentic tafsirs.
        """)
        
        with gr.Row():
            # Main chat column
            with gr.Column(scale=3):
                # Chatbot component
                chatbot = gr.Chatbot(
                    value=[],
                    height=500,
                    show_label=False,
                )
                
                # Input row
                with gr.Row():
                    user_input = gr.Textbox(
                        placeholder="Ask about the Quran...",
                        show_label=False,
                        scale=9,
                        container=False,
                    )
                    submit_btn = gr.Button("Send", variant="primary", scale=1)
                
                # Control buttons
                with gr.Row():
                    clear_btn = gr.Button("🗑️ Clear Chat")
                    refresh_btn = gr.Button("🔄 Refresh Logs")
            
            # Debug panel column - larger for detailed logs
            with gr.Column(scale=2):
                gr.Markdown("### 🔍 RAG Pipeline Debug Logs")
                gr.Markdown("*Shows: Query → Retrieval → Context → Prompt → LLM Response*")
                debug_output = gr.Textbox(
                    value=get_debug_log_text(),
                    lines=35,
                    max_lines=50,
                    show_label=False,
                    interactive=False,
                    autoscroll=True,
                )
        
        # Wire up events
        # Submit on button click
        submit_btn.click(
            fn=user_message,
            inputs=[user_input, chatbot],
            outputs=[user_input, chatbot],
        ).then(
            fn=bot_response,
            inputs=[chatbot],
            outputs=[chatbot, debug_output],
        )
        
        # Submit on Enter key
        user_input.submit(
            fn=user_message,
            inputs=[user_input, chatbot],
            outputs=[user_input, chatbot],
        ).then(
            fn=bot_response,
            inputs=[chatbot],
            outputs=[chatbot, debug_output],
        )
        
        # Clear button
        clear_btn.click(
            fn=clear_chat,
            outputs=[chatbot, debug_output],
        )
        
        # Refresh logs button
        refresh_btn.click(
            fn=refresh_debug_logs,
            outputs=[debug_output],
        )
        
        # Footer
        gr.Markdown("""
        ---
        *Powered by LangChain + Ollama + ChromaDB | RTX 3080 optimized*
        """)
    
    return demo


# ============================================================================
# Main
# ============================================================================
def main():
    """Launch the Gradio chat UI."""
    log_debug("Starting Tazkiyah Chat UI...")
    log_debug(f"Config: TOP_K={config.TOP_K}, LLM={config.LLM_MODEL}, TEMP={config.LLM_TEMPERATURE}")
    
    # Check RAG status
    if rag is not None:
        stats = rag.get_collection_stats()
        log_debug(f"Vector store: {stats['count']} documents")
        if stats["count"] == 0:
            log_debug("WARNING: Index documents first!")
            print("\n⚠️  No documents indexed. Run:")
            print("   python -m rag.index_chunks fatiha.chunks.jsonl\n")
    else:
        log_debug("ERROR: RAG failed to initialize")
        print("\n❌ RAG initialization failed. Check logs.\n")
    
    # Create and launch UI
    demo = create_ui()
    log_debug(f"Launching Gradio server on {config.UI_SERVER_HOST}:{config.UI_SERVER_PORT}...")
    
    demo.launch(
        server_name=config.UI_SERVER_HOST,
        server_port=config.UI_SERVER_PORT,
        share=config.UI_SHARE,
        show_error=True,
    )


if __name__ == "__main__":
    main()
