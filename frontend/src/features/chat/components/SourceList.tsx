import type { SourceItem } from '../../../common/types'

interface SourceListProps {
  sources: SourceItem[]
}

export function SourceList({ sources }: SourceListProps) {
  return (
    <div className="panel">
      <h2>Sources</h2>
      {sources.length === 0 ? <p className="muted">No sources returned.</p> : null}
      <ul className="source-list">
        {sources.map((source) => (
          <li key={`${source.verse_id}-${source.score ?? 'na'}`}>
            <strong>{source.verse_id}</strong>
            <span>
              {source.surah_name ?? 'Unknown surah'}
              {source.verse_number ? `:${source.verse_number}` : ''}
            </span>
            <span>{source.score !== null ? `Score: ${source.score.toFixed(4)}` : 'Score: n/a'}</span>
          </li>
        ))}
      </ul>
    </div>
  )
}
