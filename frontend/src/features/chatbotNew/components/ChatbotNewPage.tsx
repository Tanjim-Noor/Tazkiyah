import { useMemo } from 'react'
import { Link } from 'react-router-dom'

import { useConfigQuery } from '../../../common/hooks/useConfigQuery'
import { useHealthQuery } from '../../../common/hooks/useHealthQuery'
import { ChatbotNewChat } from './ChatbotNewChat'
import { REFLECTION_MODE_LABELS } from '../constants'
import { useChatbotNewPage } from '../hooks/useChatbotNewPage'

export function ChatbotNewPage() {
  const healthQuery = useHealthQuery()
  const configQuery = useConfigQuery()
  const { state, promptHint, setReflectionMode, setCompassionateNudge } = useChatbotNewPage()

  const bootstrapError = useMemo(() => {
    const healthError = healthQuery.error instanceof Error ? healthQuery.error.message : ''
    const configError = configQuery.error instanceof Error ? configQuery.error.message : ''
    return [healthError, configError].filter(Boolean).join(' | ')
  }, [healthQuery.error, configQuery.error])

  const backendReachable = !bootstrapError && Boolean(healthQuery.data)

  return (
    <main className="grid min-h-screen w-full bg-background text-foreground md:grid-cols-[304px_minmax(0,1fr)]">
      <aside className="relative flex flex-col gap-4 border-b border-border bg-panel/95 p-4 md:h-screen md:overflow-hidden md:rounded-r-[20px] md:border-r md:border-b-0 md:p-5 md:pb-28 md:shadow-[10px_0_36px_rgba(28,28,24,0.06)]">
        <div>
          <p className="text-[0.72rem] font-bold uppercase tracking-[0.08em] text-sanctuary-subtle">
            Digital Sanctuary
          </p>
          <h1 className="mt-0.5 font-serif text-[2rem] text-sanctuary-ink">Tazkiyah</h1>
          <p className="mt-1 text-[0.95rem] text-sanctuary-subtle">Quranic Guidance</p>
        </div>

        <nav className="grid gap-2" aria-label="Guidance sections">
          <button
            type="button"
            className="rounded-xl bg-user px-3 py-2.5 text-left text-sm font-medium text-sanctuary-action focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sanctuary-accent"
            aria-pressed="true"
          >
            New Guidance
          </button>
          <button
            type="button"
            className="rounded-xl px-3 py-2.5 text-left text-sm font-medium text-sanctuary-subtle transition hover:bg-control focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sanctuary-accent"
          >
            History
          </button>
          <button
            type="button"
            className="rounded-xl px-3 py-2.5 text-left text-sm font-medium text-sanctuary-subtle transition hover:bg-control focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sanctuary-accent"
          >
            Saved Verses
          </button>
          <button
            type="button"
            className="rounded-xl px-3 py-2.5 text-left text-sm font-medium text-sanctuary-subtle transition hover:bg-control focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sanctuary-accent"
          >
            Notes
          </button>
        </nav>

        <section className="grid content-start rounded-2xl border border-border/60 bg-assistant/80 p-4 shadow-[0_10px_24px_rgba(28,28,24,0.05)]">
          <h2 className="mb-2 font-serif text-lg text-sanctuary-ink">Guidance Style</h2>
          <div className="mb-2.5 grid gap-2">
            <label htmlFor="reflection-mode" className="text-sm text-sanctuary-ink">
              Answer style
            </label>
            <select
              id="reflection-mode"
              value={state.reflectionMode}
              onChange={(event) => setReflectionMode(event.target.value as keyof typeof REFLECTION_MODE_LABELS)}
              className="rounded-[10px] border border-border bg-input px-2.5 py-2 text-sm text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sanctuary-accent"
            >
              {Object.entries(REFLECTION_MODE_LABELS).map(([mode, label]) => (
                <option key={mode} value={mode}>
                  {label}
                </option>
              ))}
            </select>
          </div>

          <label className="flex items-center gap-2 text-sm text-sanctuary-ink" htmlFor="compassionate-nudge">
            <input
              id="compassionate-nudge"
              type="checkbox"
              checked={state.showCompassionateNudge}
              onChange={(event) => setCompassionateNudge(event.target.checked)}
              className="size-4 accent-sanctuary-accent"
            />
            Add a compassionate reminder
          </label>

          <p className="mt-2.5 text-sm text-sanctuary-accent">Prompt style hint: {promptHint}</p>
        </section>

        <footer className="mt-2 flex items-center gap-2.5 rounded-2xl bg-assistant/90 p-2.5 md:absolute md:right-4 md:bottom-4 md:left-4 md:mt-0">
          <div
            className="grid size-9 place-items-center rounded-full bg-user text-[0.75rem] font-bold text-sanctuary-action"
            aria-hidden="true"
          >
            DR
          </div>
          <div>
            <p className="text-sm font-semibold text-sanctuary-ink">Dr. Ar-Razi</p>
            <p className="text-[0.82rem] text-sanctuary-subtle">Resident Guide</p>
          </div>
          <Link
            className="ml-auto whitespace-nowrap rounded-full bg-control px-3 py-2 text-[0.82rem] text-sanctuary-action no-underline transition hover:bg-user focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sanctuary-accent"
            to="/"
          >
            Legacy Page
          </Link>
        </footer>
      </aside>

      <section className="grid min-w-0 p-3 md:h-screen md:px-[clamp(24px,4vw,56px)] md:pt-3.5 md:pb-5">
        <div className="mx-auto grid min-h-0 w-full max-w-[1180px] grid-rows-[auto_minmax(0,1fr)] gap-3">
          <section className="flex flex-wrap gap-2" aria-live="polite">
            <span
              className={`rounded-full px-2.5 py-1.5 text-xs ${
                backendReachable
                  ? 'bg-control text-sanctuary-action'
                  : 'bg-sanctuary-warn-bg text-sanctuary-warn-fg'
              }`}
            >
              {backendReachable ? 'Live stream ready' : 'Preparing service connection'}
            </span>
            <span className="rounded-full bg-sanctuary-pill px-2.5 py-1.5 text-xs text-sanctuary-subtle">
              Vector records: {configQuery.data?.vector_count ?? '...'}
            </span>
            {bootstrapError ? (
              <span className="rounded-full bg-sanctuary-warn-bg px-2.5 py-1.5 text-xs text-sanctuary-warn-fg">
                {bootstrapError}
              </span>
            ) : null}
          </section>
          <ChatbotNewChat isBackendReady={backendReachable} />
        </div>
      </section>
    </main>
  )
}

