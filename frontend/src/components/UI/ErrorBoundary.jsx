import React from 'react'

export default class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false, message: '' }
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, message: error.message }
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="flex min-h-screen items-center justify-center bg-background px-6 text-foreground">
          <div className="max-w-xl rounded-3xl border border-destructive/20 bg-destructive/10 p-8">
            <p className="text-xs uppercase tracking-[0.3em] text-destructive">UI fallback</p>
            <h1 className="mt-3 text-2xl font-semibold">Something broke while rendering SentimentIQ.</h1>
            <p className="mt-3 text-sm text-muted-foreground">{this.state.message}</p>
          </div>
        </div>
      )
    }

    return this.props.children
  }
}
