import { API_ENDPOINTS } from '../common/constants'
import { createLogger } from '../common/utils/logger'
import { readSSEStream } from '../common/utils/sse'
import type {
  ChatFinalPayload,
  ChatRequest,
  ConfigResponse,
  HealthResponse,
  SSEEvent,
} from '../common/types'
import { API_BASE_URL } from './env'

function toAbsoluteUrl(path: string): string {
  return `${API_BASE_URL}${path}`
}

async function fetchJson<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(toAbsoluteUrl(path), init)

  if (!response.ok) {
    const body = await response.text()
    throw new Error(`Request failed (${response.status}): ${body || response.statusText}`)
  }

  return (await response.json()) as T
}

export function getHealth(): Promise<HealthResponse> {
  return fetchJson<HealthResponse>(API_ENDPOINTS.health)
}

export function getConfig(): Promise<ConfigResponse> {
  return fetchJson<ConfigResponse>(API_ENDPOINTS.config)
}

export function sendChatSync(
  request: ChatRequest,
  requestId?: string,
): Promise<ChatFinalPayload> {
  const logger = createLogger({ scope: 'api-chat-sync', requestId })
  logger.info('Sending sync chat request', { request })

  return fetchJson<ChatFinalPayload>(API_ENDPOINTS.chatSync, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(request),
  }).then((result) => {
    logger.info('Sync chat response received', {
      hasAnswer: Boolean(result.answer),
      sources: result.sources.length,
    })
    return result
  })
}

export async function* sendChatStream(
  request: ChatRequest,
  signal?: AbortSignal,
  requestId?: string,
): AsyncGenerator<SSEEvent> {
  const logger = createLogger({ scope: 'api-chat-stream', requestId })
  logger.info('Opening SSE chat stream', { request })

  const response = await fetch(toAbsoluteUrl(API_ENDPOINTS.chatStream), {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(request),
    signal,
  })

  logger.info('SSE stream response received', {
    status: response.status,
    ok: response.ok,
    contentType: response.headers.get('content-type'),
  })

  if (!response.ok) {
    const body = await response.text()
    throw new Error(`Stream request failed (${response.status}): ${body || response.statusText}`)
  }

  for await (const event of readSSEStream(response)) {
    logger.debug(`SSE event from API layer: ${event.event}`)
    yield event
  }

  logger.info('SSE stream closed')
}
