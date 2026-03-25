import { useMemo, useState } from 'react'
import ReactMarkdown from 'react-markdown'

import type { ChatRequest, SourceItem } from '../../../common/types'
import { ChatInputBar } from './ChatInputBar'
import { VerseSourceCard } from './VerseSourceCard'
import { useChatbotNew } from '../hooks/useChatbotNew'
import './ChatbotNewChat.css'

interface ChatbotNewChatProps {
  isBackendReady: boolean
}

const EMPTY_STATE_SUGGESTIONS = [
  'I feel anxious and need perspective',
  'I am struggling with patience in hardship',
  'I want guidance for family tension',
]

export function ChatbotNewChat({ isBackendReady }: ChatbotNewChatProps) {
  const [query, setQuery] = useState('')
  const {
    messages,
    currentStreamText,
    currentCategory,
    isStreaming,
    error,
    fallbackStatus,
    sendMessage,
    cancel,
    retryLastMessage,
    clearError,
  } = useChatbotNew()

  const showEmptyState = messages.length === 0 && !isStreaming
  const composerDisabled = isStreaming || !isBackendReady

  const submit = async (text: string) => {
    const trimmed = text.trim()
    if (!trimmed || composerDisabled) return

    const payload: ChatRequest = { query: trimmed }
    setQuery('')
    await sendMessage(payload)
  }

  const onSubmit = async () => {
    await submit(query)
  }

  const onSuggestionClick = async (suggestion: string) => {
    await submit(suggestion)
  }

  const streamingSources = useMemo<SourceItem[]>(() => {
    const assistantMessages = messages.filter((message) => message.role === 'assistant')
    const latest = assistantMessages[assistantMessages.length - 1]
    return latest?.sources ?? []
  }, [messages])

  return (
    <section className="reflective-chat-shell">
      <div className="reflective-chat-stage">
        {fallbackStatus.active && fallbackStatus.message ? (
          <div className="reflective-notice" role="status" aria-live="polite">
            <p>{fallbackStatus.message}</p>
            <button type="button" onClick={() => void retryLastMessage()}>
              Retry
            </button>
          </div>
        ) : null}

        {error ? (
          <div className="reflective-notice reflective-notice-error" role="alert">
            <p>{error}</p>
            <div className="reflective-notice-actions">
              <button type="button" onClick={clearError}>
                Dismiss
              </button>
              <button type="button" onClick={() => void retryLastMessage()}>
                Retry
              </button>
              {isStreaming ? (
                <button type="button" onClick={cancel}>
                  Stop
                </button>
              ) : null}
            </div>
          </div>
        ) : null}

        {showEmptyState ? (
          <div className="reflective-empty-state">
            <h2>What is weighing on your heart today?</h2>
            <p>
              Share your situation in your own words. We will respond with calm, Quran-grounded
              guidance and transparent verse references.
            </p>
            <div className="reflective-chip-row">
              {EMPTY_STATE_SUGGESTIONS.map((suggestion) => (
                <button
                  key={suggestion}
                  type="button"
                  className="reflective-chip"
                  onClick={() => void onSuggestionClick(suggestion)}
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </div>
        ) : (
          <div className="reflective-transcript" aria-live="polite">
            {messages.map((message) => (
              <article
                key={message.id}
                className={`reflective-bubble ${
                  message.role === 'user' ? 'reflective-bubble-user' : 'reflective-bubble-assistant'
                }`}
              >
                {message.role === 'user' ? (
                  <p className="reflective-message-text">{message.content}</p>
                ) : (
                  <div className="assistant-markdown">
                    <ReactMarkdown>{message.content}</ReactMarkdown>
                  </div>
                )}
                {message.role === 'assistant' && message.category ? (
                  <p className="reflective-message-meta">Category: {message.category}</p>
                ) : null}
                {message.role === 'assistant' && message.sources?.length ? (
                  <div className="reflective-source-grid">
                    {message.sources.map((source, index) => (
                      <VerseSourceCard key={`${source.verse_id}-${index}`} source={source} />
                    ))}
                  </div>
                ) : null}
              </article>
            ))}

            {isStreaming ? (
              <article className="reflective-bubble reflective-bubble-assistant">
                {currentCategory ? <p className="reflective-message-meta">Category: {currentCategory}</p> : null}
                {currentStreamText ? (
                  <div className="assistant-markdown">
                    <ReactMarkdown>{currentStreamText}</ReactMarkdown>
                  </div>
                ) : (
                  <div className="reflective-typing" aria-label="Assistant is thinking">
                    <span />
                    <span />
                    <span />
                  </div>
                )}

                {streamingSources.length ? (
                  <div className="reflective-source-grid">
                    {streamingSources.map((source, index) => (
                      <VerseSourceCard key={`${source.verse_id}-${index}`} source={source} />
                    ))}
                  </div>
                ) : null}
              </article>
            ) : null}
          </div>
        )}
      </div>

      <div className="reflective-input-dock">
        <ChatInputBar
          query={query}
          onQueryChange={setQuery}
          onSubmit={onSubmit}
          disabled={composerDisabled}
        />
      </div>

      {!isBackendReady ? (
        <p className="muted">Backend is not ready yet. Chat will activate once health checks pass.</p>
      ) : null}
    </section>
  )
}
