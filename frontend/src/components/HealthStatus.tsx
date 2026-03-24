import type { HealthResponse } from '../common/types'

interface HealthStatusProps {
  health?: HealthResponse
  vectorCount?: number
  isLoading: boolean
  error?: string
}

export function HealthStatus({
  health,
  vectorCount,
  isLoading,
  error,
}: HealthStatusProps) {
  if (isLoading) {
    return <p className="muted">Checking backend status...</p>
  }

  if (error) {
    return <p className="status status-error">Backend unavailable: {error}</p>
  }

  const isHealthy =
    health?.status === 'ok' && health.vectorstore_ready && health.llm_ready
  const hasVectors = (vectorCount ?? 0) > 0

  if (!isHealthy || !hasVectors) {
    const reasons: string[] = []

    if (!health?.llm_ready) {
      reasons.push('llm_ready=false')
    }

    if (!health?.vectorstore_ready) {
      reasons.push('vectorstore_ready=false')
    }

    if (!hasVectors) {
      reasons.push('vector_count=0')
    }

    return (
      <p className="status status-warn">
        Backend is reachable but not fully ready.
        {reasons.length ? ` (${reasons.join(', ')})` : ''}
      </p>
    )
  }

  return <p className="status status-ok">Backend ready</p>
}
