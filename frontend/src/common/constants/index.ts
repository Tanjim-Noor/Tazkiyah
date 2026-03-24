export const API_PREFIX = '/api/v1'

export const API_ENDPOINTS = {
  health: '/health',
  config: `${API_PREFIX}/config`,
  chatStream: `${API_PREFIX}/chat`,
  chatSync: `${API_PREFIX}/chat/sync`,
} as const

export const DEFAULT_CHAT_TOP_K = 5
export const DEFAULT_CHAT_TEMPERATURE = 0.3

export const CHAT_LIMITS = {
  topKMin: 1,
  topKMax: 20,
  temperatureMin: 0,
  temperatureMax: 2,
} as const
