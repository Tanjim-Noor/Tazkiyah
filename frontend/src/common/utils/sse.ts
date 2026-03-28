import type { SSEEvent, SSEEventType } from '../types'

const VALID_EVENTS = new Set<SSEEventType>(['meta', 'sources', 'token', 'done', 'error'])

export function parseSSEChunk(buffer: string): {
  events: SSEEvent[]
  remainder: string
} {
  const normalizedBuffer = buffer.replace(/\r\n/g, '\n')
  const events: SSEEvent[] = []
  const blocks = normalizedBuffer.split('\n\n')
  const remainder = blocks.pop() ?? ''

  for (const block of blocks) {
    const lines = block.split('\n')
    const eventLine = lines.find((line) => line.startsWith('event:'))
    const dataLines = lines.filter((line) => line.startsWith('data:'))

    if (!eventLine || dataLines.length === 0) continue

    const event = eventLine.replace('event:', '').trim() as SSEEventType
    if (!VALID_EVENTS.has(event)) continue

    const rawData = dataLines
      .map((line) => line.replace('data:', '').trim())
      .join('\n')

    try {
      const parsed = JSON.parse(rawData)
      events.push({ event, data: parsed } as SSEEvent)
    } catch {
      events.push({
        event: 'error',
        data: { message: 'Failed to parse SSE payload' },
      })
    }
  }

  return { events, remainder }
}

export async function* readSSEStream(response: Response): AsyncGenerator<SSEEvent> {
  if (!response.body) {
    throw new Error('Streaming response body is missing')
  }

  const reader = response.body.getReader()
  const decoder = new TextDecoder()
  let buffer = ''

  while (true) {
    const { done, value } = await reader.read()
    if (done) break

    buffer += decoder.decode(value, { stream: true })
    const parsed = parseSSEChunk(buffer)
    buffer = parsed.remainder

    for (const event of parsed.events) {
      yield event
    }
  }

  if (buffer.trim().length > 0) {
    const parsed = parseSSEChunk(`${buffer}\n\n`)
    for (const event of parsed.events) {
      yield event
    }
  }
}
