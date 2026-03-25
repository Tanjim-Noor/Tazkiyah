import type { SourceItem } from '../../../common/types'

interface VerseSourceCardProps {
  source: SourceItem
}

export function VerseSourceCard({ source }: VerseSourceCardProps) {
  const optionalSource = source as SourceItem & {
    arabic_text?: string | null
    translation?: string | null
  }

  return (
    <article className="animate-sanctuary-fade-in space-y-4 rounded-xl border-l-4 border-primary bg-surface-container-lowest p-6 shadow-sm">
      {optionalSource.arabic_text ? (
        <p className="font-serif text-right text-2xl leading-loose tracking-wide text-primary" dir="rtl">
          {optionalSource.arabic_text}
        </p>
      ) : null}
      <div className="space-y-1">
        <p className="font-serif text-base leading-relaxed italic text-on-surface">
          {optionalSource.translation ?? 'Referenced in the guidance response above.'}
        </p>
        <div className="flex items-center justify-between border-t border-outline-variant/15 pt-3">
          <span className="text-xs font-semibold uppercase tracking-widest text-on-surface-variant/60">
            {source.surah_name ?? 'Surah'} [{source.surah_number ?? '?'}:{source.verse_number ?? '?'}]
          </span>
          <div className="flex gap-3">
            <button aria-label="Play recitation" className="material-symbols-outlined text-sm text-primary">
              play_circle
            </button>
            <button aria-label="Bookmark verse" className="material-symbols-outlined text-sm text-primary">
              bookmark
            </button>
            <button aria-label="Share verse" className="material-symbols-outlined text-sm text-primary">
              share
            </button>
          </div>
        </div>
      </div>
    </article>
  )
}
