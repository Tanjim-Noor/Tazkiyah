import type { ReflectionMode } from '../types'

export const NEW_CHATBOT_ROUTE = '/chatbot-new'

export const REFLECTION_MODE_LABELS: Record<ReflectionMode, string> = {
  guided: 'Guided reflection',
  direct: 'Direct answer',
}
