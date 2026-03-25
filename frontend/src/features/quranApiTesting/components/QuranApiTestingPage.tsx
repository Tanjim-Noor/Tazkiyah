import { Link } from 'react-router-dom'

import { toErrorMessage } from '../../../common/utils/validation'
import {
  QURAN_API_TESTING_INCLUDE_OPTIONS,
  QURAN_API_TESTING_ROUTE,
} from '../constants'
import { useQuranApiTesting } from '../hooks/useQuranApiTesting'
import type { QuranIncludeField } from '../types'

export function QuranApiTestingPage() {
  const { state, actions } = useQuranApiTesting()

  return (
    <main className="min-h-screen bg-[#f4f3ee] px-4 py-6 text-[#213028] md:px-8">
      <section className="mx-auto grid max-w-7xl gap-4">
        <header className="rounded-2xl border border-[#d5d2c8] bg-white/90 p-4 md:p-6">
          <div className="flex flex-wrap items-center gap-2">
            <h1 className="text-2xl font-semibold tracking-tight">Quran API Testing</h1>
            <span className="rounded-full bg-[#e5f0e8] px-2.5 py-1 text-xs font-medium uppercase tracking-wide text-[#1e5a3d]">
              Internal Test Harness
            </span>
          </div>
          <p className="mt-2 text-sm text-[#3f5248]">
            Validate verse retrieval, Arabic rendering, translation and tafsir payloads before chatbot
            integration.
          </p>
          <div className="mt-4 flex flex-wrap items-center gap-2 text-sm">
            <Link className="rounded-full bg-white px-3 py-1.5 text-[#174832] ring-1 ring-[#c7d3cb]" to="/">
              Legacy Page
            </Link>
            <Link
              className="rounded-full bg-white px-3 py-1.5 text-[#174832] ring-1 ring-[#c7d3cb]"
              to="/chatbot-new"
            >
              Chatbot New
            </Link>
            <span className="rounded-full bg-[#edf0eb] px-3 py-1.5 text-[#5a6a60]">
              Route: {QURAN_API_TESTING_ROUTE}
            </span>
          </div>
        </header>

        <section className="grid gap-4 lg:grid-cols-[22rem_minmax(0,1fr)]">
          <aside className="rounded-2xl border border-[#d5d2c8] bg-white/90 p-4">
            <h2 className="text-sm font-semibold uppercase tracking-wide text-[#4b5e53]">Request Builder</h2>

            <label className="mt-3 grid gap-1 text-sm" htmlFor="verse-key">
              <span>Verse key</span>
              <input
                id="verse-key"
                className="rounded-lg border border-[#cfd7d1] bg-white px-3 py-2 text-sm"
                value={state.verseKey}
                onChange={(event) => actions.setVerseKey(event.target.value)}
                placeholder="13:28"
              />
            </label>

            <label className="mt-3 grid gap-1 text-sm" htmlFor="language-code">
              <span>Language</span>
              <input
                id="language-code"
                className="rounded-lg border border-[#cfd7d1] bg-white px-3 py-2 text-sm"
                value={state.language}
                onChange={(event) => actions.setLanguage(event.target.value)}
                placeholder="en"
              />
            </label>

            <fieldset className="mt-3 rounded-lg border border-[#d9ded9] p-3">
              <legend className="px-1 text-xs font-semibold uppercase tracking-wide text-[#5c6d63]">
                Include fields
              </legend>
              <div className="mt-2 grid grid-cols-2 gap-2 text-sm">
                {QURAN_API_TESTING_INCLUDE_OPTIONS.map((item) => {
                  const checked = state.include.includes(item)
                  return (
                    <label
                      key={item}
                      className={`flex cursor-pointer items-center gap-2 rounded-md px-2 py-1.5 ${
                        checked ? 'bg-[#e9f1ea]' : 'bg-[#f8f8f5]'
                      }`}
                    >
                      <input
                        type="checkbox"
                        checked={checked}
                        onChange={() => actions.toggleInclude(item as QuranIncludeField)}
                        className="accent-[#1f6b43]"
                      />
                      <span className="text-xs uppercase tracking-wide">{item}</span>
                    </label>
                  )
                })}
              </div>
            </fieldset>

            <label className="mt-3 grid gap-1 text-sm" htmlFor="translation-ids">
              <span>Translation IDs (comma-separated)</span>
              <input
                id="translation-ids"
                className="rounded-lg border border-[#cfd7d1] bg-white px-3 py-2 text-sm"
                value={state.translationIdsInput}
                onChange={(event) => actions.setTranslationIdsInput(event.target.value)}
                placeholder="20,85"
              />
            </label>

            <label className="mt-3 grid gap-1 text-sm" htmlFor="tafsir-ids">
              <span>Tafsir IDs (comma-separated)</span>
              <input
                id="tafsir-ids"
                className="rounded-lg border border-[#cfd7d1] bg-white px-3 py-2 text-sm"
                value={state.tafsirIdsInput}
                onChange={(event) => actions.setTafsirIdsInput(event.target.value)}
                placeholder="169"
              />
            </label>

            <div className="mt-4 grid gap-2">
              <button
                type="button"
                onClick={() => void actions.submit()}
                disabled={!state.canSubmit || state.isLoading}
                className="rounded-lg bg-[#1f6b43] px-3 py-2 text-sm font-medium text-white disabled:cursor-not-allowed disabled:bg-[#9eb3a6]"
              >
                {state.isLoading ? 'Running test...' : 'Run API Test'}
              </button>
              <div className="grid grid-cols-3 gap-2 text-xs">
                <button
                  type="button"
                  className="rounded-md border border-[#cfd7d1] bg-white px-2 py-1.5"
                  onClick={() => actions.applyPreset('balance')}
                >
                  Balanced
                </button>
                <button
                  type="button"
                  className="rounded-md border border-[#cfd7d1] bg-white px-2 py-1.5"
                  onClick={() => actions.applyPreset('tafsir-heavy')}
                >
                  Tafsir Heavy
                </button>
                <button
                  type="button"
                  className="rounded-md border border-[#cfd7d1] bg-white px-2 py-1.5"
                  onClick={() => actions.applyPreset('raw-debug')}
                >
                  Raw Debug
                </button>
              </div>
              <button
                type="button"
                className="rounded-md border border-[#cfd7d1] bg-white px-2 py-1.5 text-xs"
                onClick={actions.resetAll}
              >
                Reset All
              </button>
            </div>

            {state.formError ? (
              <p className="mt-3 rounded-lg bg-[#fff1f1] px-3 py-2 text-sm text-[#9e2b2b]">{state.formError}</p>
            ) : null}
          </aside>

          <section className="grid gap-4">
            <article className="rounded-2xl border border-[#d5d2c8] bg-white/90 p-4">
              <h2 className="text-sm font-semibold uppercase tracking-wide text-[#4b5e53]">
                Resource Discovery
              </h2>
              {state.resourcesLoading ? <p className="mt-2 text-sm">Loading resources...</p> : null}
              {state.resourcesError ? (
                <p className="mt-2 rounded-lg bg-[#fff1f1] px-3 py-2 text-sm text-[#9e2b2b]">
                  {state.resourcesError}
                </p>
              ) : null}
              {state.resources ? (
                <div className="mt-3 grid gap-3 md:grid-cols-2">
                  <div className="rounded-lg bg-[#f7f8f4] p-3">
                    <p className="text-xs font-semibold uppercase tracking-wide text-[#5e6f63]">
                      Translations ({state.resources.translations.length})
                    </p>
                    <ul className="mt-2 max-h-44 overflow-auto pr-1 text-xs">
                      {state.resources.translations.slice(0, 40).map((item) => (
                        <li key={item.id} className="py-1">
                          <span className="font-medium">{item.id}</span> - {item.name}
                        </li>
                      ))}
                    </ul>
                  </div>
                  <div className="rounded-lg bg-[#f7f8f4] p-3">
                    <p className="text-xs font-semibold uppercase tracking-wide text-[#5e6f63]">
                      Tafsirs ({state.resources.tafsirs.length})
                    </p>
                    <ul className="mt-2 max-h-44 overflow-auto pr-1 text-xs">
                      {state.resources.tafsirs.slice(0, 40).map((item) => (
                        <li key={item.id} className="py-1">
                          <span className="font-medium">{item.id}</span> - {item.name}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              ) : null}
            </article>

            {state.lastResult ? (
              <article className="rounded-2xl border border-[#d5d2c8] bg-white/90 p-4">
                <div className="flex flex-wrap items-center gap-2">
                  <h2 className="text-sm font-semibold uppercase tracking-wide text-[#4b5e53]">
                    Test Result: {state.lastResult.verse_key}
                  </h2>
                  <span className="rounded-full bg-[#eef2ec] px-2 py-1 text-xs text-[#4e5f55]">
                    {state.lastResult.duration_ms} ms
                  </span>
                </div>

                {state.lastResult.warnings.length > 0 ? (
                  <div className="mt-3 rounded-lg bg-[#fff8eb] p-3 text-sm text-[#80521b]">
                    <p className="font-medium">Warnings</p>
                    <ul className="mt-1 list-disc pl-5">
                      {state.lastResult.warnings.map((warning) => (
                        <li key={warning}>{warning}</li>
                      ))}
                    </ul>
                  </div>
                ) : null}

                {state.lastResult.data.arabic_text ? (
                  <section className="mt-3 rounded-lg border border-[#d9ddd6] bg-[#fafaf8] p-3">
                    <h3 className="text-xs font-semibold uppercase tracking-wide text-[#5d6f64]">Arabic</h3>
                    <p className="mt-2 text-right text-3xl leading-[2.3] text-[#1f3329]" dir="rtl" lang="ar">
                      {state.lastResult.data.arabic_text}
                    </p>
                  </section>
                ) : null}

                {state.lastResult.data.transliteration ? (
                  <section className="mt-3 rounded-lg border border-[#d9ddd6] bg-[#fafaf8] p-3">
                    <h3 className="text-xs font-semibold uppercase tracking-wide text-[#5d6f64]">
                      Transliteration
                    </h3>
                    <p className="mt-2 text-sm italic">{state.lastResult.data.transliteration}</p>
                  </section>
                ) : null}

                {state.lastResult.data.translations.length > 0 ? (
                  <section className="mt-3 rounded-lg border border-[#d9ddd6] bg-[#fafaf8] p-3">
                    <h3 className="text-xs font-semibold uppercase tracking-wide text-[#5d6f64]">
                      Translations
                    </h3>
                    <div className="mt-2 grid gap-2">
                      {state.lastResult.data.translations.map((item) => (
                        <article key={`${item.id}-${item.name}`} className="rounded-md bg-white p-2.5 text-sm">
                          <p className="text-xs font-semibold uppercase tracking-wide text-[#536358]">
                            {item.id} - {item.name}
                          </p>
                          <p className="mt-1">{item.text}</p>
                        </article>
                      ))}
                    </div>
                  </section>
                ) : null}

                {state.lastResult.data.tafsirs.length > 0 ? (
                  <section className="mt-3 rounded-lg border border-[#d9ddd6] bg-[#fafaf8] p-3">
                    <h3 className="text-xs font-semibold uppercase tracking-wide text-[#5d6f64]">Tafsirs</h3>
                    <div className="mt-2 grid gap-2">
                      {state.lastResult.data.tafsirs.map((item) => (
                        <article key={`${item.id}-${item.name}`} className="rounded-md bg-white p-2.5 text-sm">
                          <p className="text-xs font-semibold uppercase tracking-wide text-[#536358]">
                            {item.id} - {item.name}
                          </p>
                          <p className="mt-1 whitespace-pre-wrap">{item.text}</p>
                        </article>
                      ))}
                    </div>
                  </section>
                ) : null}

                {state.lastResult.data.footnotes.length > 0 ? (
                  <section className="mt-3 rounded-lg border border-[#d9ddd6] bg-[#fafaf8] p-3">
                    <h3 className="text-xs font-semibold uppercase tracking-wide text-[#5d6f64]">Footnotes</h3>
                    <ul className="mt-2 grid gap-2 text-sm">
                      {state.lastResult.data.footnotes.map((item) => (
                        <li key={item.key} className="rounded-md bg-white p-2.5">
                          <p className="text-xs font-semibold uppercase tracking-wide text-[#536358]">
                            {item.key}
                          </p>
                          <p className="mt-1">{item.text}</p>
                        </li>
                      ))}
                    </ul>
                  </section>
                ) : null}

                {state.lastResult.data.metadata ? (
                  <section className="mt-3 rounded-lg border border-[#d9ddd6] bg-[#fafaf8] p-3">
                    <h3 className="text-xs font-semibold uppercase tracking-wide text-[#5d6f64]">Metadata</h3>
                    <dl className="mt-2 grid grid-cols-2 gap-2 text-sm md:grid-cols-4">
                      {Object.entries(state.lastResult.data.metadata).map(([key, value]) => (
                        <div key={key} className="rounded-md bg-white p-2">
                          <dt className="text-[0.68rem] uppercase tracking-wide text-[#64756b]">{key}</dt>
                          <dd className="mt-1 font-medium">{value === null ? 'N/A' : String(value)}</dd>
                        </div>
                      ))}
                    </dl>
                  </section>
                ) : null}

                {state.lastResult.data.raw ? (
                  <section className="mt-3 rounded-lg border border-[#d9ddd6] bg-[#fafaf8] p-3">
                    <h3 className="text-xs font-semibold uppercase tracking-wide text-[#5d6f64]">Raw Payload</h3>
                    <pre className="mt-2 max-h-80 overflow-auto rounded-md bg-[#1f2622] p-3 text-xs text-[#e5efe8]">
                      {JSON.stringify(state.lastResult.data.raw, null, 2)}
                    </pre>
                  </section>
                ) : null}
              </article>
            ) : (
              <article className="rounded-2xl border border-[#d5d2c8] bg-white/90 p-4 text-sm text-[#51645a]">
                Run a request to inspect Quran API response sections.
              </article>
            )}

            <article className="rounded-2xl border border-[#d5d2c8] bg-white/90 p-4">
              <h2 className="text-sm font-semibold uppercase tracking-wide text-[#4b5e53]">Checklist</h2>
              <ul className="mt-2 grid gap-1 text-sm text-[#3f5248]">
                <li>Verse retrieval by verse key</li>
                <li>Arabic script and diacritic rendering</li>
                <li>Transliteration availability</li>
                <li>Translation and tafsir by resource IDs</li>
                <li>Footnote extraction and display</li>
                <li>Metadata completeness and debugging payload</li>
              </ul>
            </article>

            {state.resourcesError ? (
              <article className="rounded-2xl border border-[#e8c6c6] bg-[#fff6f6] p-4 text-sm text-[#8d2d2d]">
                {toErrorMessage(state.resourcesError)}
              </article>
            ) : null}
          </section>
        </section>
      </section>
    </main>
  )
}
