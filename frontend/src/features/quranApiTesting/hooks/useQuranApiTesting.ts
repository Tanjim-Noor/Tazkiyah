import { useMemo, useState } from 'react'
import { useMutation, useQuery } from '@tanstack/react-query'

import { toErrorMessage } from '../../../common/utils/validation'
import {
  QURAN_API_TESTING_DEFAULT_INCLUDE,
  QURAN_API_TESTING_DEFAULT_TAFSIR_IDS,
  QURAN_API_TESTING_DEFAULT_TRANSLATION_IDS,
  QURAN_API_TESTING_DEFAULT_VERSE,
} from '../constants'
import { getQuranResources, testQuranVerse } from '../services/quranApiTestingService'
import type {
  QuranIncludeField,
  QuranVerseTestRequest,
  QuranVerseTestResponse,
} from '../types'

const VERSE_KEY_PATTERN = /^\d{1,3}:\d{1,3}$/

function parseResourceIds(input: string): number[] {
  return input
    .split(',')
    .map((item) => item.trim())
    .filter(Boolean)
    .map((item) => Number.parseInt(item, 10))
    .filter((item) => Number.isInteger(item) && item > 0)
}

export function useQuranApiTesting() {
  const [verseKey, setVerseKey] = useState(QURAN_API_TESTING_DEFAULT_VERSE)
  const [language, setLanguage] = useState('en')
  const [include, setInclude] = useState<QuranIncludeField[]>(QURAN_API_TESTING_DEFAULT_INCLUDE)
  const [translationIdsInput, setTranslationIdsInput] = useState(
    QURAN_API_TESTING_DEFAULT_TRANSLATION_IDS,
  )
  const [tafsirIdsInput, setTafsirIdsInput] = useState(QURAN_API_TESTING_DEFAULT_TAFSIR_IDS)
  const [lastResult, setLastResult] = useState<QuranVerseTestResponse | null>(null)
  const [formError, setFormError] = useState<string | null>(null)

  const resourcesQuery = useQuery({
    queryKey: ['quran-testing-resources', language],
    queryFn: () => getQuranResources(language),
    staleTime: 120_000,
  })

  const verseMutation = useMutation<QuranVerseTestResponse, Error, QuranVerseTestRequest>({
    mutationFn: (request) => testQuranVerse(request),
    onSuccess: (result) => {
      setLastResult(result)
      setFormError(null)
    },
    onError: (error) => {
      setFormError(toErrorMessage(error, 'Failed to test Quran API request'))
    },
  })

  const parsedTranslationIds = useMemo(() => parseResourceIds(translationIdsInput), [translationIdsInput])
  const parsedTafsirIds = useMemo(() => parseResourceIds(tafsirIdsInput), [tafsirIdsInput])

  const canSubmit = useMemo(() => {
    if (!VERSE_KEY_PATTERN.test(verseKey.trim())) return false
    return include.length > 0
  }, [include.length, verseKey])

  function toggleInclude(field: QuranIncludeField) {
    setInclude((prev) =>
      prev.includes(field) ? prev.filter((item) => item !== field) : [...prev, field],
    )
  }

  function applyPreset(variant: 'balance' | 'tafsir-heavy' | 'raw-debug') {
    if (variant === 'balance') {
      setInclude(['arabic', 'translations', 'metadata'])
      setTranslationIdsInput('20,85')
      setTafsirIdsInput('169')
      return
    }

    if (variant === 'tafsir-heavy') {
      setInclude(['arabic', 'translations', 'tafsirs', 'metadata', 'footnotes'])
      setTranslationIdsInput('20')
      setTafsirIdsInput('169')
      return
    }

    setInclude(['raw'])
    setTranslationIdsInput('20')
    setTafsirIdsInput('169')
  }

  function resetAll() {
    setVerseKey(QURAN_API_TESTING_DEFAULT_VERSE)
    setLanguage('en')
    setInclude(QURAN_API_TESTING_DEFAULT_INCLUDE)
    setTranslationIdsInput(QURAN_API_TESTING_DEFAULT_TRANSLATION_IDS)
    setTafsirIdsInput(QURAN_API_TESTING_DEFAULT_TAFSIR_IDS)
    setLastResult(null)
    setFormError(null)
    verseMutation.reset()
  }

  async function submit() {
    const normalizedVerse = verseKey.trim()
    if (!VERSE_KEY_PATTERN.test(normalizedVerse)) {
      setFormError('Verse key must follow format surah:verse (example: 13:28).')
      return
    }

    if (include.length === 0) {
      setFormError('Select at least one include option to run the test.')
      return
    }

    setFormError(null)

    await verseMutation.mutateAsync({
      verse_key: normalizedVerse,
      include,
      translation_ids: parsedTranslationIds,
      tafsir_ids: parsedTafsirIds,
      language,
    })
  }

  return {
    state: {
      verseKey,
      language,
      include,
      translationIdsInput,
      tafsirIdsInput,
      parsedTranslationIds,
      parsedTafsirIds,
      canSubmit,
      formError,
      lastResult,
      isLoading: verseMutation.isPending,
      resources: resourcesQuery.data,
      resourcesError: resourcesQuery.error instanceof Error ? resourcesQuery.error.message : null,
      resourcesLoading: resourcesQuery.isLoading,
    },
    actions: {
      setVerseKey,
      setLanguage,
      setTranslationIdsInput,
      setTafsirIdsInput,
      toggleInclude,
      applyPreset,
      submit,
      resetAll,
    },
  }
}
