interface ErrorBannerProps {
  message: string
  onRetry?: () => void
  onCancel?: () => void
}

export function ErrorBanner({ message, onRetry, onCancel }: ErrorBannerProps) {
  return (
    <div className="status status-error panel-inline" role="alert">
      <span>{message}</span>
      <div className="panel-actions">
        {onRetry ? (
          <button type="button" onClick={onRetry}>
            Retry
          </button>
        ) : null}
        {onCancel ? (
          <button type="button" onClick={onCancel}>
            Cancel
          </button>
        ) : null}
      </div>
    </div>
  )
}
