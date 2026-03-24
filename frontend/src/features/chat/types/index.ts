import type { ChatFinalPayload } from '../../../common/types'

export type ChatRole = 'user' | 'assistant'

export interface ChatMessage {
  id: string
  role: ChatRole
  content: string
  category?: string
  sources?: ChatFinalPayload['sources']
}

export interface ChatState {
  messages: ChatMessage[]
  currentStreamText: string
  currentCategory: string | null
  isStreaming: boolean
  error: string | null
  diagnostics: ChatDiagnostics
}

export type ChatStage =
  | 'idle'
  | 'preparing_request'
  | 'stream_connecting'
  | 'stream_active'
  | 'stream_done'
  | 'stream_timeout'
  | 'stream_error'
  | 'sync_fallback'
  | 'completed'
  | 'cancelled'

export interface ChatTraceEntry {
  timestamp: string
  stage: ChatStage
  detail: string
}

export interface ChatDiagnostics {
  requestId: string | null
  stage: ChatStage
  streamEventCount: number
  tokenChunkCount: number
  fallbackUsed: boolean
  lastEvent: string | null
  trace: ChatTraceEntry[]
}
