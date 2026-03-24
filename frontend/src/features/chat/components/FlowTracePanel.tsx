import type { ChatDiagnostics } from '../types'

interface FlowTracePanelProps {
  diagnostics: ChatDiagnostics
}

export function FlowTracePanel({ diagnostics }: FlowTracePanelProps) {
  return (
    <div className="panel">
      <h2>Flow Trace</h2>
      <dl className="config-grid">
        <div>
          <dt>Request ID</dt>
          <dd>{diagnostics.requestId || 'n/a'}</dd>
        </div>
        <div>
          <dt>Stage</dt>
          <dd>{diagnostics.stage}</dd>
        </div>
        <div>
          <dt>Stream Events</dt>
          <dd>{diagnostics.streamEventCount}</dd>
        </div>
        <div>
          <dt>Token Chunks</dt>
          <dd>{diagnostics.tokenChunkCount}</dd>
        </div>
        <div>
          <dt>Fallback Used</dt>
          <dd>{diagnostics.fallbackUsed ? 'yes' : 'no'}</dd>
        </div>
        <div>
          <dt>Last Event</dt>
          <dd>{diagnostics.lastEvent || 'n/a'}</dd>
        </div>
      </dl>
      <ul className="trace-list">
        {diagnostics.trace.slice(-15).map((entry) => (
          <li key={`${entry.timestamp}-${entry.stage}`}>
            <code>{entry.timestamp}</code>
            <span>{entry.stage}</span>
            <p>{entry.detail}</p>
          </li>
        ))}
      </ul>
    </div>
  )
}
