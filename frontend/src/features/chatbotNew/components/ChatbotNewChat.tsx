import { useMemo, useState } from 'react'
import ReactMarkdown from 'react-markdown'

import type { ChatRequest, SourceItem } from '../../../common/types'
import { ChatInputBar } from './ChatInputBar'
import { VerseSourceCard } from './VerseSourceCard'
import { useChatbotNew } from '../hooks/useChatbotNew'

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
    <section className="grid h-full min-h-0 w-full grid-rows-[minmax(0,1fr)_auto_auto]">
      <div className="mx-auto grid h-full min-h-0 w-full max-w-4xl grid-rows-[auto_auto_minmax(0,1fr)] gap-4 px-4 pt-6 md:px-8 md:pt-8">
        {fallbackStatus.active && fallbackStatus.message ? (
          <div
            className="flex items-center justify-between gap-3 rounded-xl bg-control px-3 py-2.5 text-sm text-sanctuary-ink"
            role="status"
            aria-live="polite"
          >
            <p>{fallbackStatus.message}</p>
            <button
              type="button"
              onClick={() => void retryLastMessage()}
              className="rounded-lg bg-user px-3 py-2 text-sm text-sanctuary-action focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sanctuary-accent"
            >
              Retry
            </button>
          </div>
        ) : null}

        {error ? (
          <div className="flex items-center justify-between gap-3 rounded-xl bg-sanctuary-warn-bg px-3 py-2.5 text-sm text-sanctuary-warn-fg" role="alert">
            <p>{error}</p>
            <div className="flex gap-2">
              <button
                type="button"
                onClick={clearError}
                className="rounded-lg bg-white/70 px-3 py-2 text-sm text-sanctuary-warn-fg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sanctuary-accent"
              >
                Dismiss
              </button>
              <button
                type="button"
                onClick={() => void retryLastMessage()}
                className="rounded-lg bg-white/70 px-3 py-2 text-sm text-sanctuary-warn-fg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sanctuary-accent"
              >
                Retry
              </button>
              {isStreaming ? (
                <button
                  type="button"
                  onClick={cancel}
                  className="rounded-lg bg-white/70 px-3 py-2 text-sm text-sanctuary-warn-fg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sanctuary-accent"
                >
                  Stop
                </button>
              ) : null}
            </div>
          </div>
        ) : null}

        {showEmptyState ? (
          <div className="grid min-h-full place-content-center justify-items-center gap-4.5 px-1 py-[clamp(32px,7vh,84px)] text-center">
            <h2 className="font-headline font-serif text-[clamp(2rem,8vw,3.5rem)] leading-[1.18] italic text-sanctuary-ink md:text-[clamp(2.3rem,4vw,3.5rem)]">
              "What is weighing on your heart today?"
            </h2>
            <p className="max-w-[68ch] text-[1rem] leading-[1.75] text-sanctuary-subtle md:text-[clamp(1.02rem,1.25vw,1.2rem)]">
              Share your situation in your own words. We will respond with calm, Quran-grounded
              guidance and transparent verse references.
            </p>
            <div className="grid w-full max-w-lg gap-4">
              {EMPTY_STATE_SUGGESTIONS.map((suggestion) => (
                <button
                  key={suggestion}
                  type="button"
                  className="group flex items-center justify-between rounded-2xl bg-surface-container-low p-5 text-left transition-all duration-300 hover:bg-surface-container"
                  onClick={() => void onSuggestionClick(suggestion)}
                >
                  <span className="text-base font-medium text-on-surface-variant">{suggestion}</span>
                  <span className="material-symbols-outlined text-sm text-primary opacity-0 transition-opacity group-hover:opacity-100">
                    arrow_forward_ios
                  </span>
                </button>
              ))}
            </div>

            <div className="mt-8 grid w-full grid-cols-1 gap-4 md:grid-cols-2">
              <div className="flex flex-col justify-between rounded-3xl bg-primary-fixed-dim/30 p-6">
                <span className="material-symbols-outlined mb-4 text-primary">menu_book</span>
                <p className="font-serif text-sm leading-relaxed italic text-on-primary-fixed-variant">
                  "And He found you lost and guided [you]." - 93:7
                </p>
              </div>
              <div className="flex items-center gap-4 rounded-3xl bg-surface-container-high p-6">
                <div className="flex h-12 w-12 items-center justify-center rounded-full bg-surface-container-lowest">
                  <span className="material-symbols-outlined text-on-surface-variant">lightbulb</span>
                </div>
                <p className="text-xs leading-snug text-on-surface-variant">
                  Seek clarity through the timeless wisdom of the Surahs.
                </p>
              </div>
            </div>
          </div>
        ) : (
          <div className="chatbot-scrollbar grid h-full min-h-0 gap-7 overflow-auto pr-2" aria-live="polite">
            {messages.map((message) => (
              <article
                key={message.id}
                className={`grid max-w-[96%] gap-3 rounded-[20px] px-5 py-4.5 leading-[1.65] animate-sanctuary-fade-in md:max-w-[min(82ch,92%)] ${
                  message.role === 'user'
                    ? 'ml-auto rounded-tr-[10px] bg-primary-container text-on-primary-container'
                    : 'mr-auto rounded-tl-xl bg-surface-container-low text-on-surface'
                }`}
              >
                {message.role === 'user' ? (
                  <p className="m-0 whitespace-pre-wrap">{message.content}</p>
                ) : (
                  <div className="leading-7 text-sanctuary-ink [&_blockquote]:my-2.5 [&_blockquote]:rounded-[10px] [&_blockquote]:border-l-[3px] [&_blockquote]:border-l-sanctuary-accent [&_blockquote]:bg-white/80 [&_blockquote]:px-3 [&_blockquote]:py-2.5 [&_blockquote]:font-serif [&_h1]:mb-2 [&_h1]:font-serif [&_h1]:text-xl [&_h2]:mb-2 [&_h2]:font-serif [&_h2]:text-lg [&_h3]:mb-2 [&_h3]:font-serif [&_h3]:text-base [&_ol]:my-1.5 [&_ol]:ml-5 [&_p]:m-0 [&_p+p]:mt-2.5 [&_ul]:my-1.5 [&_ul]:ml-5">
                    <ReactMarkdown>{message.content}</ReactMarkdown>
                  </div>
                )}
                {message.role === 'assistant' && message.category ? (
                  <p className="m-0 text-xs text-muted">Category: {message.category}</p>
                ) : null}
                {message.role === 'assistant' && message.sources?.length ? (
                  <div className="grid grid-cols-1 gap-3 md:grid-cols-[repeat(auto-fit,minmax(220px,1fr))]">
                    {message.sources.map((source, index) => (
                      <VerseSourceCard key={`${source.verse_id}-${index}`} source={source} />
                    ))}
                  </div>
                ) : null}
              </article>
            ))}

            {isStreaming ? (
              <article className="mr-auto grid max-w-[96%] gap-3 rounded-[20px] rounded-tl-xl bg-surface-container-low px-5 py-4.5 leading-[1.65] text-on-surface animate-sanctuary-fade-in md:max-w-[min(82ch,92%)]">
                {currentCategory ? <p className="m-0 text-xs text-muted">Category: {currentCategory}</p> : null}
                {currentStreamText ? (
                  <div className="leading-7 text-sanctuary-ink [&_blockquote]:my-2.5 [&_blockquote]:rounded-[10px] [&_blockquote]:border-l-[3px] [&_blockquote]:border-l-sanctuary-accent [&_blockquote]:bg-white/80 [&_blockquote]:px-3 [&_blockquote]:py-2.5 [&_blockquote]:font-serif [&_h1]:mb-2 [&_h1]:font-serif [&_h1]:text-xl [&_h2]:mb-2 [&_h2]:font-serif [&_h2]:text-lg [&_h3]:mb-2 [&_h3]:font-serif [&_h3]:text-base [&_ol]:my-1.5 [&_ol]:ml-5 [&_p]:m-0 [&_p+p]:mt-2.5 [&_ul]:my-1.5 [&_ul]:ml-5">
                    <ReactMarkdown>{currentStreamText}</ReactMarkdown>
                  </div>
                ) : (
                  <div className="inline-flex w-fit items-center gap-1.5 rounded-full bg-sanctuary-pill px-3 py-2" aria-label="Assistant is thinking">
                    <span className="size-1.75 rounded-full bg-sanctuary-accent animate-reflective-dot" />
                    <span className="size-1.75 rounded-full bg-sanctuary-accent animate-reflective-dot [animation-delay:150ms]" />
                    <span className="size-1.75 rounded-full bg-sanctuary-accent animate-reflective-dot [animation-delay:300ms]" />
                  </div>
                )}

                {streamingSources.length ? (
                  <div className="grid grid-cols-1 gap-3 md:grid-cols-[repeat(auto-fit,minmax(220px,1fr))]">
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

      <div className="sticky bottom-0 mt-0.5 w-full bg-linear-to-t from-background via-background to-transparent pt-10 pb-6">
        <div className="mx-auto w-full max-w-3xl px-4 md:px-8">
          <ChatInputBar
            query={query}
            onQueryChange={setQuery}
            onSubmit={onSubmit}
            disabled={composerDisabled}
          />
        </div>
      </div>

      {!isBackendReady ? (
        <p className="text-sm text-muted">Backend is not ready yet. Chat will activate once health checks pass.</p>
      ) : null}
    </section>
  )
}

