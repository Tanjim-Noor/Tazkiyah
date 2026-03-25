import type { FormEvent } from 'react'

interface ChatInputBarProps {
  query: string
  onQueryChange: (value: string) => void
  onSubmit: () => void | Promise<void>
  disabled: boolean
}

export function ChatInputBar({ query, onQueryChange, onSubmit, disabled }: ChatInputBarProps) {
  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    await onSubmit()
  }

  return (
    <form className="sanctuary-input-bar" onSubmit={(event) => void handleSubmit(event)}>
      <button type="button" className="icon-button" aria-label="Attach note" disabled={disabled}>
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <path d="M8 12.5V7.8a4.2 4.2 0 1 1 8.4 0v8.2a6.2 6.2 0 0 1-12.4 0V8.7" />
        </svg>
      </button>

      <textarea
        rows={1}
        value={query}
        onChange={(event) => onQueryChange(event.target.value)}
        placeholder="Share your situation..."
        disabled={disabled}
      />

      <button type="submit" className="send-button" disabled={disabled || !query.trim()} aria-label="Send message">
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <path d="m5 12 14-7-4 7 4 7z" />
        </svg>
      </button>
    </form>
  )
}
