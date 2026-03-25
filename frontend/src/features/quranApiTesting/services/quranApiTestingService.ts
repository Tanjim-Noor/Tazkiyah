import { API_ENDPOINTS } from '../../../common/constants'
import { createLogger } from '../../../common/utils/logger'
import { API_BASE_URL } from '../../../config/env'
import type {
  QuranResourcesResponse,
  QuranVerseTestRequest,
  QuranVerseTestResponse,
} from '../types'

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

export function getQuranResources(language = 'en'): Promise<QuranResourcesResponse> {
  return fetchJson<QuranResourcesResponse>(`${API_ENDPOINTS.quranResources}?language=${language}`)
}

export function testQuranVerse(
  request: QuranVerseTestRequest,
  requestId?: string,
): Promise<QuranVerseTestResponse> {
  const logger = createLogger({ scope: 'quran-api-testing', requestId })
  logger.info('Submitting Quran API test request', {
    verse: request.verse_key,
    include: request.include,
    translationIds: request.translation_ids,
    tafsirIds: request.tafsir_ids,
  })

  return fetchJson<QuranVerseTestResponse>(API_ENDPOINTS.quranVerseTest, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(request),
  }).then((response) => {
    logger.info('Quran API test request completed', {
      warnings: response.warnings.length,
      durationMs: response.duration_ms,
    })
    return response
  })
}
