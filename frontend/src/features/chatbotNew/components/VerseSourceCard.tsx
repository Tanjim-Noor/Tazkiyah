import type { SourceItem } from '../../../common/types'

interface VerseSourceCardProps {
  source: SourceItem
}

export function VerseSourceCard({ source }: VerseSourceCardProps) {
  return (
    <article className="grid gap-[3px] rounded-2xl bg-white p-3 shadow-[0_10px_24px_rgba(28,28,24,0.05)] animate-sanctuary-fade-in">
      <p className="m-0 text-[0.72rem] uppercase tracking-[0.04em] text-[color:var(--color-muted)]">Verse</p>
      <p className="m-0 text-[0.9rem] text-foreground">{source.verse_id}</p>

      <p className="m-0 text-[0.72rem] uppercase tracking-[0.04em] text-[color:var(--color-muted)]">Surah / Ayah</p>
      <p className="m-0 text-[0.9rem] text-foreground">
        {source.surah_name ?? 'Surah'} {source.surah_number ?? '?'}:{source.verse_number ?? '?'}
      </p>

      <p className="m-0 text-[0.72rem] uppercase tracking-[0.04em] text-[color:var(--color-muted)]">Translation</p>
      <p className="m-0 text-[0.9rem] text-[color:var(--color-sanctuary-subtle)]">
        Referenced in the guidance response above.
      </p>
    </article>
  )
}
