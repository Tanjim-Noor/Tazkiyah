export type QuranIncludeField =
  | 'arabic'
  | 'transliteration'
  | 'translations'
  | 'tafsirs'
  | 'metadata'
  | 'footnotes'
  | 'raw'

export interface QuranResourceItem {
  id: number
  name: string
  language_name: string | null
  author_name: string | null
}

export interface QuranResourcesResponse {
  language: string | null
  translations: QuranResourceItem[]
  tafsirs: QuranResourceItem[]
}

export interface QuranVerseTestRequest {
  verse_key: string
  include: QuranIncludeField[]
  translation_ids: number[]
  tafsir_ids: number[]
  language: string
}

export interface QuranTranslationItem {
  id: number
  name: string
  language_name: string | null
  text: string
}

export interface QuranTafsirItem {
  id: number
  name: string
  language_name: string | null
  text: string
}

export interface QuranFootnoteItem {
  key: string
  text: string
}

export interface QuranVerseMetadata {
  surah_number: number
  verse_number: number
  surah_name: string | null
  surah_name_arabic: string | null
  juz: number | null
  page: number | null
  hizb: number | null
  rub_el_hizb: number | null
  ruku: number | null
  manzil: number | null
  sajdah: number | null
  revelation_place: string | null
  revelation_order: number | null
}

export interface QuranVerseData {
  arabic_text: string | null
  transliteration: string | null
  translations: QuranTranslationItem[]
  tafsirs: QuranTafsirItem[]
  footnotes: QuranFootnoteItem[]
  metadata: QuranVerseMetadata | null
  raw: Record<string, unknown> | null
}

export interface QuranVerseTestResponse {
  verse_key: string
  requested_include: QuranIncludeField[]
  warnings: string[]
  duration_ms: number
  data: QuranVerseData
}
