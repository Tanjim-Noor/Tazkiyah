import { CHAT_LIMITS } from '../constants'

export function clampTopK(value: number | undefined): number | undefined {
  if (value === undefined || Number.isNaN(value)) return undefined
  return Math.min(CHAT_LIMITS.topKMax, Math.max(CHAT_LIMITS.topKMin, Math.round(value)))
}

export function clampTemperature(value: number | undefined): number | undefined {
  if (value === undefined || Number.isNaN(value)) return undefined
  const clamped = Math.min(
    CHAT_LIMITS.temperatureMax,
    Math.max(CHAT_LIMITS.temperatureMin, value),
  )
  return Number(clamped.toFixed(2))
}

export function toErrorMessage(error: unknown, fallback = 'Unexpected error'): string {
  if (error instanceof Error && error.message) return error.message
  return fallback
}
