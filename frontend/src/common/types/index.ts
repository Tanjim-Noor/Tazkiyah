export interface HealthResponse {
  status: string
  service: string
  vectorstore_ready: boolean
  llm_ready: boolean
}

export interface ConfigResponse {
  app_name: string
  environment: string
  llm_provider: string
  embedding_provider: string
  vectorstore_provider: string
  llm_model: string
  embedding_model: string
  collection_name: string
  top_k: number
  categories: string[]
  langsmith_tracing: boolean
  langsmith_project: string
  vector_count: number
}

export interface ChatRequest {
  query: string
  top_k?: number
  temperature?: number
  return_sources?: boolean
}

export interface SourceItem {
  verse_id: string
  surah_name: string | null
  surah_number: number | null
  verse_number: number | null
  score: number | null
}

export interface ChatFinalPayload {
  answer: string
  category: string
  sources: SourceItem[]
}

export type SSEEventType = 'meta' | 'token' | 'done' | 'error'

export type SSEEventPayloadMap = {
  meta: { category: string }
  token: { text: string }
  done: ChatFinalPayload
  error: { message: string }
}

export type SSEEvent =
  | { event: 'meta'; data: SSEEventPayloadMap['meta'] }
  | { event: 'token'; data: SSEEventPayloadMap['token'] }
  | { event: 'done'; data: SSEEventPayloadMap['done'] }
  | { event: 'error'; data: SSEEventPayloadMap['error'] }
