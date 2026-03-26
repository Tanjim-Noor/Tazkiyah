import { useMemo } from 'react'
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
      <aside className="relative flex flex-col gap-4 border-b border-border/30 bg-surface-dim/30 backdrop-blur-md md:h-screen md:overflow-hidden md:border-r md:border-b-0 md:shadow-[30px_0_60px_-15px_rgba(28,28,24,0.05)]">
        <div className="shrink-0 px-8 pt-10">
          <h1 className="font-serif text-2xl font-bold text-sanctuary-accent">Tazkiyah</h1>
          <p className="mt-1 text-xs uppercase tracking-widest opacity-50">Digital Sanctuary</p>
        </div>

        <nav className="shrink-0 pr-4" aria-label="Guidance sections">
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

        <div className="flex-1 overflow-y-auto px-8 pb-28">
          <section className="mt-6 grid content-start rounded-2xl border border-border/60 bg-assistant/80 p-4 shadow-[0_10px_24px_rgba(28,28,24,0.05)]">
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
        </div>

        <footer className="mt-2 flex items-center gap-2.5 rounded-2xl bg-assistant/90 p-2.5 md:absolute md:right-0 md:bottom-0 md:left-0 md:mx-8 md:mb-6 md:mt-0">
          <img
            src="https://lh3.googleusercontent.com/aida-public/AB6AXuCssF8bR8RW4CZSTAoLjJlMqkkm1h6JhVSZksDZQrL3Plonk_9qhsLQ6-2KQpOtfrtUJwpka1-NrycaTsWKMcGACv_B_y_mh7s6t05d07GuzDVOr9gxzPVwyOsheIbbrBqAIoryyp14DXhOn046lb7iPvO9q-69E1jaIoiegfVoZTb25B54W8gSr--lmRqGzywTY5n9ZvMWxVG-MV6bNzqsoUS_3qN9-rw7jj1KyL-5JrOMqHFhSMba7wDXmhSrsEz-EKCCKY3Je3tc"
            alt="Dr. Ar-Razi"
            className="h-10 w-10 rounded-full object-cover"
          />
          <div>
            <p className="text-sm font-bold text-on-surface">Dr. Ar-Razi</p>
            <p className="text-[10px] uppercase opacity-60">Senior Fellow</p>
          </div>
        </footer>
      </aside>

      <section className="flex min-h-0 min-w-0 flex-col overflow-hidden md:h-screen">
        <header className="sticky top-0 z-50 flex shrink-0 items-center justify-between bg-[#fcf9f2]/80 px-8 py-5 backdrop-blur-xl md:px-12">
          <div className="flex flex-col">
            <span className="font-serif text-2xl font-semibold italic tracking-tight text-sanctuary-accent">Tazkiyah</span>
            <span className="text-[10px] font-medium uppercase tracking-[0.2em] text-on-surface-variant/60">
              Quranic Guidance
            </span>
          </div>
          <div className="flex items-center gap-6">
            <nav className="hidden items-center gap-8 text-sm font-medium text-[#2F3A33]/60 lg:flex">
              <a href="#" className="transition-colors duration-300 hover:text-sanctuary-accent">Library</a>
              <a href="#" className="border-b-2 border-sanctuary-accent pb-1 text-sanctuary-accent">Reflections</a>
              <a href="#" className="transition-colors duration-300 hover:text-sanctuary-accent">Scholarship</a>
            </nav>
            <div className="flex items-center gap-4">
              <button className="material-symbols-outlined text-sanctuary-accent opacity-70 transition-opacity hover:opacity-100">
                settings
              </button>
              <button className="material-symbols-outlined text-sanctuary-accent opacity-70 transition-opacity hover:opacity-100">
                account_circle
              </button>
            </div>
          </div>
        </header>

        <div className="flex shrink-0 flex-wrap gap-2 px-8 py-1.5" aria-live="polite">
          <span
            className={`rounded-full px-2.5 py-1.5 text-[10px] ${
              backendReachable ? 'bg-control text-sanctuary-action' : 'bg-sanctuary-warn-bg text-sanctuary-warn-fg'
            }`}
          >
            {backendReachable ? 'Live stream ready' : 'Preparing service connection'}
          </span>
          <span className="bg-sanctuary-pill text-sanctuary-subtle rounded-full px-2.5 py-1.5 text-[10px]">
            Vector records: {configQuery.data?.vector_count ?? '...'}
          </span>
          {bootstrapError ? (
            <span className="bg-sanctuary-warn-bg text-sanctuary-warn-fg rounded-full px-2.5 py-1.5 text-[10px]">
              {bootstrapError}
            </span>
          ) : null}
        </div>

        <div className="flex min-h-0 w-full flex-1">
          <ChatbotNewChat isBackendReady={backendReachable} />
        </div>
      </section>
    </main>
  )
}

