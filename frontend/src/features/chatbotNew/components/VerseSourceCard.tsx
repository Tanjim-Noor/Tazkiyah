import type { SourceItem } from '../../../common/types'

interface VerseSourceCardProps {
  source: SourceItem
}

export function VerseSourceCard({ source }: VerseSourceCardProps) {
  return (
    <article className="animate-sanctuary-fade-in space-y-4 rounded-xl border-l-4 border-primary bg-white p-6 shadow-sm">
      {source.arabic_text ? (
        <p className="font-serif text-right text-2xl leading-loose tracking-wide text-primary" dir="rtl">
          {source.arabic_text}
        </p>
      ) : null}
      <div className="space-y-1">
        <p className="font-serif text-base leading-relaxed italic text-on-surface">
          {source.translation ?? 'Referenced in the guidance response above.'}
        </p>
        <div className="flex items-center justify-between border-t border-outline-variant/15 pt-3">
          <span className="text-xs font-semibold uppercase tracking-widest text-on-surface-variant/60">
            {source.surah_name ?? 'Surah'} [{source.surah_number ?? '?'}:{source.verse_number ?? '?'}]
          </span>
          <div className="flex gap-1">
            <button aria-label="Play recitation" className="p-1.5 text-primary">
              <span className="material-symbols-outlined text-[20px]">play_circle</span>
            </button>
            <button aria-label="Bookmark verse" className="p-1.5 text-primary">
              <span className="material-symbols-outlined text-[20px]">bookmark</span>
            </button>
            <button aria-label="Share verse" className="p-1.5 text-primary">
              <span className="material-symbols-outlined text-[20px]">share</span>
            </button>
          </div>
        </div>
      </div>
    </article>
  )
}
