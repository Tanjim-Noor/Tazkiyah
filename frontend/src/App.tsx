import { useMemo } from 'react'

import { ConfigSummary } from './components/ConfigSummary'
import { HealthStatus } from './components/HealthStatus'
import { useConfigQuery } from './common/hooks/useConfigQuery'
import { useHealthQuery } from './common/hooks/useHealthQuery'
import { Chat } from './features/chat/components/Chat'
import './App.css'

function App() {
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

export default App
