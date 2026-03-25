export const QURAN_API_TESTING_ROUTE = '/quran-api-testing'

export const QURAN_API_TESTING_DEFAULT_VERSE = '13:28'

export const QURAN_API_TESTING_INCLUDE_OPTIONS = [
  'arabic',
  'transliteration',
  'translations',
  'tafsirs',
  'metadata',
  'footnotes',
  'raw',
] as const

export const QURAN_API_TESTING_DEFAULT_INCLUDE: Array<
  (typeof QURAN_API_TESTING_INCLUDE_OPTIONS)[number]
> = ['arabic', 'translations', 'metadata']

export const QURAN_API_TESTING_DEFAULT_TRANSLATION_IDS = '20,85'
export const QURAN_API_TESTING_DEFAULT_TAFSIR_IDS = '169'
