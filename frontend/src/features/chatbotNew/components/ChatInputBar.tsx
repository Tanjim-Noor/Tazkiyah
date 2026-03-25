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
    <form
      className="grid grid-cols-[1fr_auto] items-center gap-2.5 rounded-[20px] border border-border/60 bg-white/85 p-2.5 shadow-[0_16px_36px_rgba(28,28,24,0.07)] md:grid-cols-[auto_1fr_auto] md:rounded-full md:px-3 md:py-2.5"
      onSubmit={(event) => void handleSubmit(event)}
    >
      <button
        type="button"
        className="hidden size-[34px] place-items-center rounded-full bg-control text-[color:var(--color-sanctuary-subtle)] md:grid"
        aria-label="Attach note"
        disabled={disabled}
      >
        <svg
          viewBox="0 0 24 24"
          aria-hidden="true"
          className="size-[18px] fill-none stroke-current [stroke-linecap:round] [stroke-linejoin:round] [stroke-width:1.7]"
        >
          <path d="M8 12.5V7.8a4.2 4.2 0 1 1 8.4 0v8.2a6.2 6.2 0 0 1-12.4 0V8.7" />
        </svg>
      </button>

      <textarea
        className="min-h-11 max-h-[120px] w-full resize-none rounded-2xl border-0 bg-transparent px-2 py-2.5 text-[0.95rem] text-foreground shadow-none outline-none focus-visible:ring-0"
        rows={1}
        value={query}
        onChange={(event) => onQueryChange(event.target.value)}
        placeholder="Share your situation..."
        disabled={disabled}
      />

      <button
        type="submit"
        className="grid size-10 place-items-center rounded-full bg-linear-to-br from-[color:var(--color-sanctuary-accent)] to-[#7c9a84] text-white shadow-[0_8px_16px_rgba(72,101,81,0.28)] transition disabled:cursor-not-allowed disabled:opacity-45"
        disabled={disabled || !query.trim()}
        aria-label="Send message"
      >
        <svg viewBox="0 0 24 24" aria-hidden="true" className="size-[18px] fill-current stroke-none">
          <path d="m5 12 14-7-4 7 4 7z" />
        </svg>
      </button>
    </form>
  )
}
