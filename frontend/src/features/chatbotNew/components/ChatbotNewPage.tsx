import { useEffect, useMemo } from 'react'
import { Link } from 'react-router-dom'

import { useConfigQuery } from '../../../common/hooks/useConfigQuery'
import { useHealthQuery } from '../../../common/hooks/useHealthQuery'
import { ChatbotNewChat } from './ChatbotNewChat'
import { REFLECTION_MODE_LABELS } from '../constants'
import { useChatbotNewPage } from '../hooks/useChatbotNewPage'
import './ChatbotNewPage.css'

export function ChatbotNewPage() {
  const healthQuery = useHealthQuery()
  const configQuery = useConfigQuery()
  const { state, promptHint, setReflectionMode, setCompassionateNudge } = useChatbotNewPage()

  useEffect(() => {
    document.body.classList.add('chatbot-new-theme')

    return () => {
      document.body.classList.remove('chatbot-new-theme')
    }
  }, [])

  const bootstrapError = useMemo(() => {
    const healthError = healthQuery.error instanceof Error ? healthQuery.error.message : ''
    const configError = configQuery.error instanceof Error ? configQuery.error.message : ''
    return [healthError, configError].filter(Boolean).join(' | ')
  }, [healthQuery.error, configQuery.error])

  const backendReachable = !bootstrapError && Boolean(healthQuery.data)

  return (
    <main className="new-chatbot-shell">
      <aside className="sanctuary-sidebar">
        <div className="sidebar-brand">
          <p className="new-chatbot-eyebrow">Digital Sanctuary</p>
          <h1>Tazkiyah</h1>
          <p className="new-chatbot-lead">Quranic Guidance</p>
        </div>

        <nav className="sidebar-nav" aria-label="Guidance sections">
          <button type="button" className="sidebar-nav-item is-active">New Guidance</button>
          <button type="button" className="sidebar-nav-item">History</button>
          <button type="button" className="sidebar-nav-item">Saved Verses</button>
          <button type="button" className="sidebar-nav-item">Notes</button>
        </nav>

        <section className="new-chatbot-control-panel">
          <h2>Guidance Style</h2>
          <div className="new-chatbot-control-row">
            <label htmlFor="reflection-mode">Answer style</label>
            <select
              id="reflection-mode"
              value={state.reflectionMode}
              onChange={(event) => setReflectionMode(event.target.value as keyof typeof REFLECTION_MODE_LABELS)}
            >
              {Object.entries(REFLECTION_MODE_LABELS).map(([mode, label]) => (
                <option key={mode} value={mode}>
                  {label}
                </option>
              ))}
            </select>
          </div>

          <label className="checkbox-label" htmlFor="compassionate-nudge">
            <input
              id="compassionate-nudge"
              type="checkbox"
              checked={state.showCompassionateNudge}
              onChange={(event) => setCompassionateNudge(event.target.checked)}
            />
            Add a compassionate reminder
          </label>

          <p className="new-chatbot-hint">Prompt style hint: {promptHint}</p>
        </section>

        <footer className="sidebar-footer">
          <div className="profile-avatar" aria-hidden="true">DR</div>
          <div>
            <p className="profile-name">Dr. Ar-Razi</p>
            <p className="profile-role">Resident Guide</p>
          </div>
          <Link className="new-chatbot-link" to="/">
            Legacy Page
          </Link>
        </footer>
      </aside>

      <section className="sanctuary-main">
        <div className="sanctuary-main-inner">
          <section className="new-chatbot-status-row" aria-live="polite">
            <span className={`new-chatbot-status-pill ${backendReachable ? 'is-ok' : 'is-warn'}`}>
              {backendReachable ? 'Live stream ready' : 'Preparing service connection'}
            </span>
            <span className="new-chatbot-status-pill">
              Vector records: {configQuery.data?.vector_count ?? '...'}
            </span>
            {bootstrapError ? <span className="new-chatbot-status-pill is-warn">{bootstrapError}</span> : null}
          </section>
          <ChatbotNewChat isBackendReady={backendReachable} />
        </div>
      </section>
    </main>
  )
}
