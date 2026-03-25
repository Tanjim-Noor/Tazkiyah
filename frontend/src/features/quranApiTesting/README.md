# Quran API Testing Feature

Internal page for validating Quran API response contracts before integrating API-backed verse details into chatbot experiences.

## Purpose

- Test verse retrieval by `verse_key`
- Validate Arabic rendering and diacritics in UI
- Validate translations and tafsir retrieval by resource IDs
- Inspect metadata, footnotes, and optional raw payload

## Boundaries

- Uses dedicated backend testing endpoints under `/api/v1/quran-testing/*`
- Does not modify or reuse chat stream state
- Keeps local state isolated to this feature

## Public Surface

- `components/QuranApiTestingPage.tsx`
- `hooks/useQuranApiTesting.ts`
- `services/quranApiTestingService.ts`
- `constants/index.ts`
- `types/index.ts`
