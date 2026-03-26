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
    <div>
      <form
        className="relative flex items-end gap-3 rounded-2xl bg-surface-container-lowest p-3 pr-4 shadow-[0_10px_40px_-10px_rgba(0,0,0,0.05)] transition-all duration-500 focus-within:ring-1 focus-within:ring-primary/20"
        onSubmit={(event) => void handleSubmit(event)}
      >
        <button
          type="button"
          className="p-3 text-on-surface-variant/40 transition-colors hover:text-primary"
          aria-label="Add context"
          disabled={disabled}
        >
          <span className="material-symbols-outlined">add_circle</span>
        </button>

        <textarea
          className="max-h-30 min-h-11 w-full resize-none border-0 bg-transparent py-3 text-base text-on-surface shadow-none outline-none placeholder:text-on-surface-variant/40 focus-visible:ring-0"
          rows={1}
          value={query}
          onChange={(event) => onQueryChange(event.target.value)}
          placeholder="Seek guidance or share a reflection..."
          disabled={disabled}
        />

        <button
          type="submit"
          className="rounded-xl bg-linear-to-br from-primary to-primary-container p-2.5 text-white shadow-lg shadow-primary/20 transition-all hover:scale-[1.02] active:scale-[0.98] disabled:cursor-not-allowed disabled:opacity-45"
          disabled={disabled || !query.trim()}
          aria-label="Send message"
        >
          <span className="material-symbols-outlined text-[20px]" style={{ fontVariationSettings: "'FILL' 1" }}>
            arrow_upward
          </span>
        </button>
      </form>
      <p className="mt-3 text-center text-[10px] font-medium uppercase tracking-widest text-on-surface-variant/40">
        Reflect in peace. Your words are a path to wisdom.
      </p>
    </div>
  )
}
