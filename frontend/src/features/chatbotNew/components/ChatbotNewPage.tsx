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
    <main className="grid min-h-screen w-full bg-background text-foreground md:grid-cols-[18rem_minmax(0,1fr)]">
      <aside className="relative flex flex-col border-b border-border/30 bg-[#dcdad3]/30 p-4 backdrop-blur-md md:h-screen md:overflow-hidden md:border-r md:border-b-0 md:p-8 md:pb-28 md:shadow-[30px_0_60px_-15px_rgba(28,28,24,0.05)]">
        <div>
          <h1 className="font-serif text-2xl font-bold uppercase text-sanctuary-accent">TAZKIYAH</h1>
          <p className="mt-1 text-xs uppercase tracking-widest opacity-50">Digital Sanctuary</p>
        </div>

        <nav className="mt-6 grid gap-2" aria-label="Guidance sections">
          <button
            type="button"
            className="flex items-center gap-3 rounded-r-full bg-white/50 py-3 pr-3 pl-6 text-left text-sm font-medium uppercase tracking-wide text-sanctuary-accent transition focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sanctuary-accent"
            aria-pressed="true"
          >
            <span className="material-symbols-outlined text-xl" style={{ fontVariationSettings: "'FILL' 1" }}>
              add_circle
            </span>
            New Guidance
          </button>
          <button
            type="button"
            className="flex items-center gap-3 rounded-r-full py-3 pr-3 pl-6 text-left text-sm font-medium uppercase tracking-wide text-[#2F3A33]/50 transition hover:bg-white/30 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sanctuary-accent"
          >
            <span className="material-symbols-outlined text-xl">history</span>
            History
          </button>
          <button
            type="button"
            className="flex items-center gap-3 rounded-r-full py-3 pr-3 pl-6 text-left text-sm font-medium uppercase tracking-wide text-[#2F3A33]/50 transition hover:bg-white/30 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sanctuary-accent"
          >
            <span className="material-symbols-outlined text-xl">auto_stories</span>
            Saved Verses
          </button>
          <button
            type="button"
            className="flex items-center gap-3 rounded-r-full py-3 pr-3 pl-6 text-left text-sm font-medium uppercase tracking-wide text-[#2F3A33]/50 transition hover:bg-white/30 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sanctuary-accent"
          >
            <span className="material-symbols-outlined text-xl">edit_note</span>
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

        <footer className="mt-2 flex items-center gap-2.5 rounded-2xl bg-assistant/90 p-2.5 md:absolute md:right-6 md:bottom-6 md:left-6 md:mt-0">
          <img
            src="https://lh3.googleusercontent.com/aida-public/AB6AXuCssF8bR8RW4CZSTAoLjJlMqkkm1h6JhVSZksDZQrL3Plonk_9qhsLQ6-2KQpOtfrtUJwpka1-NrycaTsWKMcGACv_B_y_mh7s6t05d07GuzDVOr9gxzPVwyOsheIbbrBqAIoryyp14DXhOn046lb7iPvO9q-69E1jaIoiegfVoZTb25B54W8gSr--lmRqGzywTY5n9ZvMWxVG-MV6bNzqsoUS_3qN9-rw7jj1KyL-5JrOMqHFhSMba7wDXmhSrsEz-EKCCKY3Je3tc"
            alt="Dr. Ar-Razi"
            className="h-10 w-10 rounded-full object-cover"
          />
          <div>
            <p className="text-sm font-bold text-on-surface">Dr. Ar-Razi</p>
            <p className="text-[10px] uppercase opacity-60">Senior Fellow</p>
          </div>
          <Link
            className="ml-auto whitespace-nowrap rounded-full bg-control px-3 py-2 text-[0.82rem] text-sanctuary-action no-underline transition hover:bg-user focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sanctuary-accent"
            to="/"
          >
            Legacy Page
          </Link>
          <Link
            className="whitespace-nowrap rounded-full bg-control px-3 py-2 text-[0.82rem] text-sanctuary-action no-underline transition hover:bg-user focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sanctuary-accent"
            to="/quran-api-testing"
          >
            Quran API Testing
          </Link>
        </footer>
      </aside>

      <section className="grid min-w-0 min-h-0 md:h-screen">
        <div className="grid min-h-0 w-full grid-rows-[auto_minmax(0,1fr)]">
          <section className="flex flex-wrap gap-2 px-4 pt-4 md:px-8" aria-live="polite">
            <span
              className={`px-2.5 py-1.5 text-xs ${
                backendReachable
                  ? 'bg-control text-sanctuary-action rounded-full'
                  : 'bg-sanctuary-warn-bg text-sanctuary-warn-fg rounded-full'
              }`}
            >
              {backendReachable ? 'Live stream ready' : 'Preparing service connection'}
            </span>
            <span className="bg-sanctuary-pill text-sanctuary-subtle rounded-full px-2.5 py-1.5 text-xs">
              Vector records: {configQuery.data?.vector_count ?? '...'}
            </span>
            {bootstrapError ? (
              <span className="bg-sanctuary-warn-bg text-sanctuary-warn-fg rounded-full px-2.5 py-1.5 text-xs">
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

