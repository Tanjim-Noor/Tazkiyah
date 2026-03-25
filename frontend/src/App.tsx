import { useMemo } from 'react'
import { Link, Navigate, Route, Routes } from 'react-router-dom'

import { ConfigSummary } from './components/ConfigSummary'
import { HealthStatus } from './components/HealthStatus'
import { useConfigQuery } from './common/hooks/useConfigQuery'
import { useHealthQuery } from './common/hooks/useHealthQuery'
import { Chat } from './features/chat/components/Chat'
import { ChatbotNewPage } from './features/chatbotNew/components/ChatbotNewPage'
import { QuranApiTestingPage } from './features/quranApiTesting/components/QuranApiTestingPage'
import './App.css'

function LegacyIntegrationPage() {
  const healthQuery = useHealthQuery()
  const configQuery = useConfigQuery()

  const bootstrapError = useMemo(() => {
    const healthError = healthQuery.error instanceof Error ? healthQuery.error.message : ''
    const configError = configQuery.error instanceof Error ? configQuery.error.message : ''
    return [healthError, configError].filter(Boolean).join(' | ')
  }, [healthQuery.error, configQuery.error])

  const backendReachable = !bootstrapError && Boolean(healthQuery.data)

  return (
    <main className="app-shell">
      <header className="panel">
        <div className="panel-title-row">
          <h1>Tazkiyah Frontend Integration</h1>
          <span className="muted">Phase 1: API integration</span>
        </div>
        <div className="flex flex-wrap gap-2 py-2 text-sm">
          <Link className="text-[#2f6f4f] no-underline" to="/chatbot-new">
            Open Chatbot New
          </Link>
          <span className="text-[#8a8d88]">|</span>
          <Link className="text-[#2f6f4f] no-underline" to="/quran-api-testing">
            Open Quran API Testing
          </Link>
        </div>
        <HealthStatus
          health={healthQuery.data}
          vectorCount={configQuery.data?.vector_count}
          isLoading={healthQuery.isLoading}
          error={bootstrapError || undefined}
        />
      </header>

      <section className="panel">
        <h2>Runtime Configuration</h2>
        <ConfigSummary config={configQuery.data} isLoading={configQuery.isLoading} />
      </section>

      <Chat isBackendReady={backendReachable} />
    </main>
  )
}

function App() {
  return (
    <Routes>
      <Route path="/" element={<LegacyIntegrationPage />} />
      <Route path="/chatbot-new" element={<ChatbotNewPage />} />
      <Route path="/quran-api-testing" element={<QuranApiTestingPage />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}

export default App
