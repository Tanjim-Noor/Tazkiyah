import type { ConfigResponse } from '../common/types'

interface ConfigSummaryProps {
  config?: ConfigResponse
  isLoading: boolean
}

export function ConfigSummary({ config, isLoading }: ConfigSummaryProps) {
  if (isLoading) {
    return <p className="muted">Loading runtime configuration...</p>
  }

  if (!config) {
    return <p className="muted">Configuration not loaded.</p>
  }

  return (
    <dl className="config-grid">
      <div>
        <dt>LLM Model</dt>
        <dd>{config.llm_model}</dd>
      </div>
      <div>
        <dt>Embedding Model</dt>
        <dd>{config.embedding_model}</dd>
      </div>
      <div>
        <dt>Top K</dt>
        <dd>{config.top_k}</dd>
      </div>
      <div>
        <dt>Vector Count</dt>
        <dd>{config.vector_count}</dd>
      </div>
    </dl>
  )
}
