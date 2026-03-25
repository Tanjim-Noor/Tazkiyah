import { useCallback, useMemo, useRef, useState } from 'react'

import type { ChatRequest, SourceItem } from '../../../common/types'
import { createLogger } from '../../../common/utils/logger'
import { toErrorMessage } from '../../../common/utils/validation'
import {
  normalizeChatRequest,
  sendChatStream,
  sendChatSync,
} from '../../chat/services/chatAPI'
import type {
  ChatDiagnostics,
  ChatMessage,
  ChatStage,
  ChatState,
} from '../../chat/types'

interface FallbackStatus {
  active: boolean
  message: string | null
}

function makeId(): string {
  return `${Date.now()}-${Math.random().toString(36).slice(2, 10)}`
}

const initialState: ChatState = {
  messages: [],
  currentStreamText: '',
  currentCategory: null,
  isStreaming: false,
  error: null,
  diagnostics: {
    requestId: null,
    stage: 'idle',
    streamEventCount: 0,
    tokenChunkCount: 0,
    fallbackUsed: false,
    lastEvent: null,
    trace: [],
  },
}

function traceEntry(stage: ChatStage, detail: string) {
  return {
    timestamp: new Date().toISOString(),
    stage,
    detail,
  }
}

function isServiceUnavailableError(value: unknown): boolean {
  if (!(value instanceof Error)) return false
  return /\(503\)|\b503\b|service unavailable/i.test(value.message)
}

export function useChatbotNew() {
  const [state, setState] = useState<ChatState>(initialState)
  const [fallbackStatus, setFallbackStatus] = useState<FallbackStatus>({
    active: false,
    message: null,
  })
  const abortRef = useRef<AbortController | null>(null)
  const lastRequestRef = useRef<ChatRequest | null>(null)
  const currentStreamTextRef = useRef('')
  const currentCategoryRef = useRef<string | null>(null)
  const userCancelledRef = useRef(false)
  const streamTimeoutRef = useRef<number | null>(null)

  const appendTrace = useCallback((stage: ChatStage, detail: string) => {
    setState((prev) => ({
      ...prev,
      diagnostics: {
        ...prev.diagnostics,
        stage,
        trace: [...prev.diagnostics.trace, traceEntry(stage, detail)],
      },
    }))
  }, [])

  const updateDiagnostics = useCallback((updater: (prev: ChatDiagnostics) => ChatDiagnostics) => {
    setState((prev) => ({
      ...prev,
      diagnostics: updater(prev.diagnostics),
    }))
  }, [])

  const clearStreamTimeout = useCallback(() => {
    if (streamTimeoutRef.current !== null) {
      window.clearTimeout(streamTimeoutRef.current)
      streamTimeoutRef.current = null
    }
  }, [])

  const appendMessage = useCallback((message: ChatMessage) => {
    setState((prev) => ({ ...prev, messages: [...prev.messages, message] }))
  }, [])

  const finalizeAssistant = useCallback(
    (answer: string, category: string | undefined, sources: SourceItem[]) => {
      appendMessage({
        id: makeId(),
        role: 'assistant',
        content: answer,
        category,
        sources,
      })
      setState((prev) => ({
        ...prev,
        currentStreamText: '',
        currentCategory: null,
        isStreaming: false,
        error: null,
        diagnostics: {
          ...prev.diagnostics,
          stage: 'completed',
          trace: [...prev.diagnostics.trace, traceEntry('completed', 'Assistant response finalized.')],
        },
      }))
      currentStreamTextRef.current = ''
      currentCategoryRef.current = null
      clearStreamTimeout()
      setFallbackStatus({ active: false, message: null })
    },
    [appendMessage, clearStreamTimeout],
  )

  const sendMessage = useCallback(async (request: ChatRequest) => {
    const normalized = normalizeChatRequest(request)
    const requestId = `chat-new-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`
    const logger = createLogger({ scope: 'chatbot-new-flow', requestId })

    logger.info('sendMessage started', { request: normalized })

    if (!normalized.query) {
      setState((prev) => ({ ...prev, error: 'Query is required.' }))
      logger.warn('Query validation failed: empty query')
      return
    }

    lastRequestRef.current = normalized
    setFallbackStatus({ active: false, message: null })

    setState((prev) => ({
      ...prev,
      diagnostics: {
        requestId,
        stage: 'preparing_request',
        streamEventCount: 0,
        tokenChunkCount: 0,
        fallbackUsed: false,
        lastEvent: null,
        trace: [traceEntry('preparing_request', 'Request prepared and validated.')],
      },
    }))

    appendMessage({
      id: makeId(),
      role: 'user',
      content: normalized.query,
    })

    const controller = new AbortController()
    abortRef.current = controller
    userCancelledRef.current = false

    clearStreamTimeout()
    streamTimeoutRef.current = window.setTimeout(() => {
      if (!userCancelledRef.current) {
        logger.warn('No SSE events received within timeout window; aborting stream.')
        appendTrace('stream_timeout', 'No SSE event within 15s; stream aborted for fallback.')
        controller.abort()
      }
    }, 15000)

    setState((prev) => ({
      ...prev,
      isStreaming: true,
      error: null,
      currentStreamText: '',
      currentCategory: null,
      diagnostics: {
        ...prev.diagnostics,
        stage: 'stream_connecting',
        trace: [...prev.diagnostics.trace, traceEntry('stream_connecting', 'Connecting to SSE endpoint.')],
      },
    }))
    currentStreamTextRef.current = ''
    currentCategoryRef.current = null

    let gotDone = false
    let receivedAnyEvent = false

    try {
      for await (const event of sendChatStream(normalized, controller.signal, requestId)) {
        if (!receivedAnyEvent) {
          receivedAnyEvent = true
          clearStreamTimeout()
          appendTrace('stream_active', 'First SSE event received.')
        }

        logger.debug(`SSE event received: ${event.event}`, event.data)
        updateDiagnostics((prev) => ({
          ...prev,
          stage: 'stream_active',
          streamEventCount: prev.streamEventCount + 1,
          tokenChunkCount: event.event === 'token' ? prev.tokenChunkCount + 1 : prev.tokenChunkCount,
          lastEvent: event.event,
          trace: [...prev.trace, traceEntry('stream_active', `Received event: ${event.event}`)],
        }))

        if (event.event === 'meta') {
          currentCategoryRef.current = event.data.category
          setState((prev) => ({ ...prev, currentCategory: event.data.category }))
        }

        if (event.event === 'token') {
          currentStreamTextRef.current = `${currentStreamTextRef.current}${event.data.text}`
          setState((prev) => ({
            ...prev,
            currentStreamText: `${prev.currentStreamText}${event.data.text}`,
          }))
        }

        if (event.event === 'done') {
          if (gotDone) continue
          gotDone = true
          appendTrace('stream_done', 'Done event received from SSE stream.')
          finalizeAssistant(event.data.answer, event.data.category, event.data.sources)
        }

        if (event.event === 'error') {
          throw new Error(event.data.message)
        }
      }

      if (!gotDone) {
        const streamed = currentStreamTextRef.current
        if (streamed.trim()) {
          logger.warn('Stream ended without done event, using accumulated token text.')
          finalizeAssistant(streamed, currentCategoryRef.current ?? undefined, [])
        } else {
          throw new Error('Stream ended before a final payload was received.')
        }
      }
    } catch (error) {
      clearStreamTimeout()

      if (controller.signal.aborted && userCancelledRef.current) {
        logger.info('Stream cancelled by user.')
        setState((prev) => ({
          ...prev,
          isStreaming: false,
          error: 'Request cancelled.',
          currentStreamText: '',
          currentCategory: null,
          diagnostics: {
            ...prev.diagnostics,
            stage: 'cancelled',
            trace: [...prev.diagnostics.trace, traceEntry('cancelled', 'User cancelled active request.')],
          },
        }))
        setFallbackStatus({ active: false, message: null })
        currentStreamTextRef.current = ''
        currentCategoryRef.current = null
        return
      }

      try {
        const degradedReason = toErrorMessage(error)
        const fallbackMessage = isServiceUnavailableError(error)
          ? 'The live response is temporarily busy. Continuing with a steady reply path.'
          : 'The live response is taking longer than expected. Continuing with a steady reply path.'

        setFallbackStatus({ active: true, message: fallbackMessage })

        logger.warn('Streaming failed; attempting sync fallback.', {
          reason: degradedReason,
        })

        updateDiagnostics((prev) => ({
          ...prev,
          stage: 'sync_fallback',
          fallbackUsed: true,
          trace: [...prev.trace, traceEntry('sync_fallback', `Fallback to sync due to: ${degradedReason}`)],
        }))

        const fallback = await sendChatSync(normalized, requestId)
        logger.info('Sync fallback succeeded.')
        finalizeAssistant(fallback.answer, fallback.category, fallback.sources)
      } catch (fallbackError) {
        logger.error('Sync fallback failed.', {
          error: toErrorMessage(fallbackError),
        })
        setState((prev) => ({
          ...prev,
          isStreaming: false,
          error: toErrorMessage(fallbackError, toErrorMessage(error)),
          currentStreamText: '',
          currentCategory: null,
          diagnostics: {
            ...prev.diagnostics,
            stage: 'stream_error',
            trace: [
              ...prev.diagnostics.trace,
              traceEntry('stream_error', `Fallback failed: ${toErrorMessage(fallbackError, toErrorMessage(error))}`),
            ],
          },
        }))
        currentStreamTextRef.current = ''
        currentCategoryRef.current = null
      }
    }
  }, [appendMessage, appendTrace, clearStreamTimeout, finalizeAssistant, updateDiagnostics])

  const retryLastMessage = useCallback(async () => {
    const lastRequest = lastRequestRef.current
    if (!lastRequest) return

    await sendMessage(lastRequest)
  }, [sendMessage])

  const cancel = useCallback(() => {
    userCancelledRef.current = true
    appendTrace('cancelled', 'Cancellation requested by user.')
    abortRef.current?.abort()
    abortRef.current = null
    clearStreamTimeout()
  }, [appendTrace, clearStreamTimeout])

  const clearError = useCallback(() => {
    setState((prev) => ({ ...prev, error: null }))
  }, [])

  return useMemo(
    () => ({
      ...state,
      fallbackStatus,
      sendMessage,
      cancel,
      retryLastMessage,
      clearError,
      diagnostics: state.diagnostics,
    }),
    [state, fallbackStatus, sendMessage, cancel, retryLastMessage, clearError],
  )
}
