import type { SourceItem } from '../../../common/types'

interface VerseSourceCardProps {
  source: SourceItem
}

export function VerseSourceCard({ source }: VerseSourceCardProps) {
  return (
    <article className="verse-card">
      <p className="verse-card-label">Verse</p>
      <p className="verse-card-value">{source.verse_id}</p>

      <p className="verse-card-label">Surah / Ayah</p>
      <p className="verse-card-value">
        {source.surah_name ?? 'Surah'} {source.surah_number ?? '?'}:{source.verse_number ?? '?'}
      </p>

      <p className="verse-card-label">Translation</p>
      <p className="verse-card-value verse-card-muted">
        Referenced in the guidance response above.
      </p>
    </article>
  )
}
