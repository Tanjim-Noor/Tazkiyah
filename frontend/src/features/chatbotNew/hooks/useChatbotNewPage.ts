import { useMemo, useState } from 'react'

import { buildPromptStyleHint } from '../services/chatbotNewService'
import type { ChatbotNewPageState, ReflectionMode } from '../types'

const DEFAULT_STATE: ChatbotNewPageState = {
  reflectionMode: 'guided',
  showCompassionateNudge: true,
}

export function useChatbotNewPage() {
  const [state, setState] = useState<ChatbotNewPageState>(DEFAULT_STATE)

  const promptHint = useMemo(
    () => buildPromptStyleHint(state.reflectionMode, state.showCompassionateNudge),
    [state.reflectionMode, state.showCompassionateNudge],
  )

  const setReflectionMode = (reflectionMode: ReflectionMode) => {
    setState((previous) => ({ ...previous, reflectionMode }))
  }

  const setCompassionateNudge = (showCompassionateNudge: boolean) => {
    setState((previous) => ({ ...previous, showCompassionateNudge }))
  }

  return {
    state,
    promptHint,
    setReflectionMode,
    setCompassionateNudge,
  }
}
