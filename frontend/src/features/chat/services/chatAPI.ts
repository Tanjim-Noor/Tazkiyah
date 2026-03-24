import {
  DEFAULT_CHAT_TEMPERATURE,
  DEFAULT_CHAT_TOP_K,
} from '../../../common/constants'
import type { ChatRequest } from '../../../common/types'
import { clampTemperature, clampTopK } from '../../../common/utils/validation'
import { sendChatStream, sendChatSync } from '../../../config/api'

export function normalizeChatRequest(request: ChatRequest): ChatRequest {
  return {
    query: request.query.trim(),
    top_k: clampTopK(request.top_k ?? DEFAULT_CHAT_TOP_K),
    temperature: clampTemperature(request.temperature ?? DEFAULT_CHAT_TEMPERATURE),
    return_sources: request.return_sources ?? true,
  }
}

export { sendChatStream, sendChatSync }
