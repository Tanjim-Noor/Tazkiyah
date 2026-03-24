import type { PropsWithChildren } from 'react'
import { Component } from 'react'

interface ErrorBoundaryState {
  hasError: boolean
  message: string
}

export class AppErrorBoundary extends Component<PropsWithChildren, ErrorBoundaryState> {
  public state: ErrorBoundaryState = { hasError: false, message: '' }

  public static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, message: error.message }
  }

  public componentDidCatch(error: Error): void {
    console.error('Unhandled frontend error:', error)
  }

  public render() {
    if (this.state.hasError) {
      return (
        <div className="error-shell">
          <h2>Something went wrong</h2>
          <p>{this.state.message || 'Please refresh and try again.'}</p>
        </div>
      )
    }

    return this.props.children
  }
}