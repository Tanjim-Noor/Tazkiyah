import type { ReflectionMode } from '../types'

export function buildPromptStyleHint(mode: ReflectionMode, includeCompassionNudge: boolean): string {
  const modeHint =
    mode === 'guided'
      ? 'Use a guided reflective tone with gentle checkpoints.'
      : 'Use a concise and direct guidance tone.'

  if (!includeCompassionNudge) {
    return modeHint
  }

  return `${modeHint} Add one short compassionate nudge when appropriate.`
}
