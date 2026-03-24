import type { ChatMessage } from '../types'

interface TranscriptAreaProps {
  messages: ChatMessage[]
  currentStreamText: string
  currentCategory: string | null
}

export function TranscriptArea({
  messages,
  currentStreamText,
  currentCategory,
}: TranscriptAreaProps) {
  return (
    <div className="panel transcript">
      <h2>Transcript</h2>
      {messages.length === 0 && !currentStreamText ? (
        <p className="muted">No messages yet.</p>
      ) : null}

      {messages.map((message) => (
        <article key={message.id} className={`message message-${message.role}`}>
          <h3>{message.role === 'user' ? 'You' : 'Assistant'}</h3>
          {message.category ? <p className="category">Category: {message.category}</p> : null}
          <p>{message.content}</p>
        </article>
      ))}

      {currentStreamText ? (
        <article className="message message-assistant message-streaming">
          <h3>Assistant (streaming)</h3>
          {currentCategory ? <p className="category">Category: {currentCategory}</p> : null}
          <p>{currentStreamText}</p>
        </article>
      ) : null}
    </div>
  )
}
