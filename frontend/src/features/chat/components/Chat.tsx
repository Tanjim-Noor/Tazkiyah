import { useMemo } from 'react'

import { ErrorBanner } from '../../../components/ErrorBanner'
import { ChatForm } from './ChatForm'
import { FlowTracePanel } from './FlowTracePanel'
import { SourceList } from './SourceList'
import { TranscriptArea } from './TranscriptArea'
import { useChat } from '../hooks/useChat'

interface ChatProps {
  isBackendReady: boolean
}

export function Chat({ isBackendReady }: ChatProps) {
  const {
    messages,
    currentStreamText,
    currentCategory,
    isStreaming,
    error,
    sendMessage,
    cancel,
    clearError,
    diagnostics,
  } =
    useChat()

  const lastAssistantSources = useMemo(() => {
    const assistantMessages = messages.filter((message) => message.role === 'assistant')
    const latest = assistantMessages[assistantMessages.length - 1]
    return latest?.sources ?? []
  }, [messages])

  return (
    <section className="panel-stack">
      <div className="panel">
        <h2>Chat</h2>
        {error ? (
          <ErrorBanner
            message={error}
            onRetry={clearError}
            onCancel={isStreaming ? cancel : undefined}
          />
        ) : null}
        <ChatForm
          isStreaming={isStreaming}
          isBackendReady={isBackendReady}
          onSubmit={sendMessage}
        />
      </div>

      <TranscriptArea
        messages={messages}
        currentStreamText={currentStreamText}
        currentCategory={currentCategory}
      />

      <SourceList sources={lastAssistantSources} />

      <FlowTracePanel diagnostics={diagnostics} />
    </section>
  )
}
