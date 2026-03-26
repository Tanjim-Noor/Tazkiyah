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

function normalizeAssistantMarkdown(content: string): string {
  const lines = content.split('\n')

  for (let index = 0; index < lines.length; index += 1) {
    const line = lines[index].trim()
    const isVerseReference = /^Verse Reference(s)?:/i.test(line)
    const alreadyQuoted = lines[index].trimStart().startsWith('>')

    if (!isVerseReference || alreadyQuoted) {
      continue
    }

    const previousIndex = index - 1
    if (previousIndex >= 0) {
      const previousLine = lines[previousIndex].trim()
      const previousIsQuoteLike =
        (previousLine.startsWith('"') && previousLine.endsWith('"')) ||
        (previousLine.startsWith('\'') && previousLine.endsWith('\''))

      if (previousIsQuoteLike && !lines[previousIndex].trimStart().startsWith('>')) {
        lines[previousIndex] = `> ${lines[previousIndex].trim()}`
      }
    }

    lines[index] = `> ${lines[index].trim()}`
  }

  return lines.join('\n')
}

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
    <section className="flex h-full min-h-0 w-full flex-col overflow-hidden">
      {fallbackStatus.active && fallbackStatus.message ? (
        <div
          className="mx-8 mt-2 flex shrink-0 items-center justify-between gap-3 rounded-xl bg-control px-3 py-2.5 text-sm text-sanctuary-ink"
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
        <div className="mx-8 mt-2 flex shrink-0 items-center justify-between gap-3 rounded-xl bg-sanctuary-warn-bg px-3 py-2.5 text-sm text-sanctuary-warn-fg" role="alert">
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
        <div className="flex flex-1 flex-col items-center justify-center overflow-y-auto px-6 py-12">
          <div className="w-full max-w-3xl">
            <section className="w-full rounded-4xl bg-surface-container-lowest p-10 text-center shadow-sm md:p-14">
              <h2 className="mb-4 font-serif text-3xl font-semibold leading-relaxed italic text-on-surface">
                "What is weighing on your heart today?"
              </h2>
              <p className="mx-auto mb-10 max-w-[60ch] text-base leading-relaxed text-on-surface-variant">
                Share your situation in your own words. We will respond with calm, Quran-grounded
                guidance and transparent verse references.
              </p>
              <div className="mx-auto grid max-w-lg gap-4">
                {EMPTY_STATE_SUGGESTIONS.map((suggestion) => (
                  <button
                    key={suggestion}
                    type="button"
                    className="group flex min-h-15 items-center justify-between rounded-2xl bg-surface-container-low p-5 text-left transition-all duration-300 hover:bg-surface-container"
                    onClick={() => void onSuggestionClick(suggestion)}
                  >
                    <span className="text-base font-medium text-on-surface-variant">{suggestion}</span>
                    <span className="material-symbols-outlined text-sm text-primary opacity-0 transition-opacity group-hover:opacity-100">
                      arrow_forward_ios
                    </span>
                  </button>
                ))}
              </div>
              <div className="mt-12 flex justify-center gap-1">
                <div className="h-1.5 w-1.5 rounded-full bg-primary/20" />
                <div className="h-1.5 w-1.5 rounded-full bg-primary/40" />
                <div className="h-1.5 w-1.5 rounded-full bg-primary/20" />
              </div>
            </section>

            <div className="mt-6 grid grid-cols-1 gap-4 md:grid-cols-2">
              <div className="flex min-h-30 flex-col justify-between rounded-3xl bg-primary-fixed-dim/30 p-6">
                <span className="material-symbols-outlined mb-4 text-2xl text-primary">menu_book</span>
                <p className="font-serif text-sm leading-relaxed italic text-on-primary-fixed-variant">
                  "And He found you lost and guided [you]." - 93:7
                </p>
              </div>
              <div className="flex min-h-30 items-center gap-4 rounded-3xl bg-surface-container-high p-6">
                <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-surface-container-lowest">
                  <span className="material-symbols-outlined text-2xl text-on-surface-variant">lightbulb</span>
                </div>
                <p className="text-xs leading-snug text-on-surface-variant">
                  Seek clarity through the timeless wisdom of the Surahs.
                </p>
              </div>
            </div>
          </div>
        </div>
      ) : (
        <div className="chatbot-scrollbar flex-1 overflow-y-auto px-6 py-12" aria-live="polite">
          <div className="mx-auto w-full max-w-6xl space-y-8">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex animate-sanctuary-fade-in items-start gap-4 ${
                  message.role === 'user' ? 'justify-end' : 'justify-start'
                }`}
              >
                {message.role === 'assistant' && (
                  <div className="mt-1 flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-primary-container">
                    <span
                      className="material-symbols-outlined select-none text-[18px] text-on-primary"
                      style={{ fontVariationSettings: "'FILL' 1, 'wght' 400, 'GRAD' 0, 'opsz' 24" }}
                    >
                      auto_awesome
                    </span>
                  </div>
                )}

                {message.role === 'user' ? (
                  <div className="max-w-[75%] rounded-xl rounded-tr-md bg-primary-container p-6 text-on-primary-container shadow-sm">
                    <p className="whitespace-pre-wrap text-base leading-relaxed font-medium">{message.content}</p>
                  </div>
                ) : (
                  <div className="w-full overflow-hidden space-y-4 rounded-xl rounded-tl-md bg-surface-container-low p-8">
                    {message.category ? (
                      <p className="text-xs font-semibold uppercase tracking-widest text-on-surface-variant/60">
                        {message.category}
                      </p>
                    ) : null}
                    <div className="leading-relaxed text-on-surface-variant [&_blockquote]:my-4 [&_blockquote]:rounded-xl [&_blockquote]:border-l-4 [&_blockquote]:border-primary [&_blockquote]:bg-white [&_blockquote]:p-6 [&_blockquote]:shadow-sm [&_blockquote]:not-italic [&_blockquote_p]:font-serif [&_blockquote_p]:italic [&_blockquote_p]:text-base [&_blockquote_p]:leading-relaxed [&_blockquote_p]:text-on-surface [&_h3]:mb-3 [&_h3]:font-serif [&_h3]:text-xl [&_h3]:font-bold [&_h3]:text-primary [&_p]:text-base [&_p]:leading-relaxed [&_p]:text-on-surface-variant [&_p+p]:mt-3 [&_strong]:font-semibold [&_strong]:text-on-surface [&_ol]:my-2 [&_ol]:ml-5 [&_ol]:space-y-1 [&_ul]:my-2 [&_ul]:ml-5 [&_ul]:space-y-1">
                      <ReactMarkdown>{normalizeAssistantMarkdown(message.content)}</ReactMarkdown>
                    </div>
                    {message.sources?.length ? (
                      <div className="grid w-full grid-cols-1 gap-3 pt-2 sm:grid-cols-2">
                        {message.sources.map((source, index) => (
                          <VerseSourceCard key={`${source.verse_id}-${index}`} source={source} />
                        ))}
                      </div>
                    ) : null}
                  </div>
                )}

                {message.role === 'user' && (
                  <div className="mt-1 flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-surface-container-highest">
                    <span className="material-symbols-outlined select-none text-[18px] text-primary">person</span>
                  </div>
                )}
              </div>
            ))}

            {isStreaming ? (
              <div className="flex animate-sanctuary-fade-in items-start gap-4 justify-start">
                <div className="mt-1 flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-primary-container/20">
                  <span
                    className="material-symbols-outlined select-none text-[18px] text-primary/40"
                    style={{ fontVariationSettings: "'FILL' 1, 'wght' 400, 'GRAD' 0, 'opsz' 24" }}
                  >
                    auto_awesome
                  </span>
                </div>
                <div className="w-full overflow-hidden space-y-4 rounded-xl rounded-tl-md bg-surface-container-low p-8">
                  {currentCategory ? (
                    <p className="text-xs font-semibold uppercase tracking-widest text-on-surface-variant/60">
                      {currentCategory}
                    </p>
                  ) : null}
                  {currentStreamText ? (
                    <div className="leading-relaxed text-on-surface-variant [&_blockquote]:my-4 [&_blockquote]:rounded-xl [&_blockquote]:border-l-4 [&_blockquote]:border-primary [&_blockquote]:bg-white [&_blockquote]:p-6 [&_blockquote]:shadow-sm [&_blockquote]:not-italic [&_blockquote_p]:font-serif [&_blockquote_p]:italic [&_blockquote_p]:text-base [&_blockquote_p]:leading-relaxed [&_blockquote_p]:text-on-surface [&_h3]:mb-3 [&_h3]:font-serif [&_h3]:text-xl [&_h3]:font-bold [&_h3]:text-primary [&_p]:text-base [&_p]:leading-relaxed [&_p]:text-on-surface-variant [&_p+p]:mt-3 [&_strong]:font-semibold [&_strong]:text-on-surface [&_ol]:my-2 [&_ol]:ml-5 [&_ul]:my-2 [&_ul]:ml-5">
                      <ReactMarkdown>{normalizeAssistantMarkdown(currentStreamText)}</ReactMarkdown>
                    </div>
                  ) : (
                    <div className="flex gap-1.5 px-1 py-2" aria-label="Assistant is thinking">
                      <div className="h-1.5 w-1.5 rounded-full bg-primary/40 animate-reflective-dot" />
                      <div className="h-1.5 w-1.5 rounded-full bg-primary/40 animate-reflective-dot [animation-delay:200ms]" />
                      <div className="h-1.5 w-1.5 rounded-full bg-primary/40 animate-reflective-dot [animation-delay:400ms]" />
                    </div>
                  )}
                  {streamingSources.length ? (
                    <div className="grid w-full grid-cols-1 gap-3 pt-2 sm:grid-cols-2">
                      {streamingSources.map((source, index) => (
                        <VerseSourceCard key={`${source.verse_id}-${index}`} source={source} />
                      ))}
                    </div>
                  ) : null}
                </div>
              </div>
            ) : null}
          </div>
        </div>
      )}

      <div className="sticky bottom-0 w-full shrink-0 bg-linear-to-t from-background via-background to-transparent px-6 pt-10 pb-8">
        <div className="group relative mx-auto w-full max-w-3xl">
          <div className="pointer-events-none absolute inset-0 rounded-full bg-primary/5 opacity-0 blur-2xl transition-opacity duration-500 group-focus-within:opacity-100" />
          <ChatInputBar query={query} onQueryChange={setQuery} onSubmit={onSubmit} disabled={composerDisabled} />
        </div>
      </div>

      {!isBackendReady ? (
        <p className="shrink-0 px-8 pb-2 text-sm text-muted">Backend is not ready yet.</p>
      ) : null}
    </section>
  )
}

