import type { FormEvent } from 'react'
import { useState } from 'react'

import { DEFAULT_CHAT_TEMPERATURE, DEFAULT_CHAT_TOP_K } from '../../../common/constants'
import type { ChatRequest } from '../../../common/types'

interface ChatFormProps {
  isStreaming: boolean
  isBackendReady: boolean
  onSubmit: (request: ChatRequest) => void
}

export function ChatForm({ isStreaming, isBackendReady, onSubmit }: ChatFormProps) {
  const [query, setQuery] = useState('')
  const [topK, setTopK] = useState(DEFAULT_CHAT_TOP_K)
  const [temperature, setTemperature] = useState(DEFAULT_CHAT_TEMPERATURE)
  const [returnSources, setReturnSources] = useState(true)

  const isDisabled = isStreaming || !isBackendReady
  const canSubmit = query.trim().length > 0 && !isDisabled

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    if (!canSubmit) return

    onSubmit({
      query,
      top_k: topK,
      temperature,
      return_sources: returnSources,
    })
    setQuery('')
  }

  return (
    <form className="chat-form" onSubmit={handleSubmit}>
      <label>
        Query
        <textarea
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder="Ask for Quranic guidance"
          rows={4}
          disabled={isDisabled}
        />
      </label>

      <div className="chat-controls">
        <label>
          Top K
          <input
            type="number"
            min={1}
            max={20}
            value={topK}
            onChange={(event) => setTopK(Number(event.target.value))}
            disabled={isDisabled}
          />
        </label>

        <label>
          Temperature
          <input
            type="number"
            min={0}
            max={2}
            step={0.1}
            value={temperature}
            onChange={(event) => setTemperature(Number(event.target.value))}
            disabled={isDisabled}
          />
        </label>

        <label className="checkbox-label">
          <input
            type="checkbox"
            checked={returnSources}
            onChange={(event) => setReturnSources(event.target.checked)}
            disabled={isDisabled}
          />
          Return sources
        </label>
      </div>

      <button type="submit" disabled={!canSubmit}>
        {isStreaming ? 'Streaming...' : isBackendReady ? 'Send' : 'Backend not ready'}
      </button>
      {!isBackendReady && !isStreaming ? (
        <p className="muted">Chat is disabled because backend is unreachable.</p>
      ) : null}
    </form>
  )
}
