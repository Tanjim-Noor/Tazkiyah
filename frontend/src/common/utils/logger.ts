export type LogLevel = 'debug' | 'info' | 'warn' | 'error'

interface TraceContext {
  requestId?: string
  scope: string
}

function log(level: LogLevel, context: TraceContext, message: string, meta?: unknown) {
  const timestamp = new Date().toISOString()
  const prefix = `[${timestamp}] [${context.scope}]${context.requestId ? ` [${context.requestId}]` : ''}`

  if (level === 'debug') {
    console.debug(prefix, message, meta ?? '')
    return
  }

  if (level === 'info') {
    console.info(prefix, message, meta ?? '')
    return
  }

  if (level === 'warn') {
    console.warn(prefix, message, meta ?? '')
    return
  }

  console.error(prefix, message, meta ?? '')
}

export function createLogger(context: TraceContext) {
  return {
    debug: (message: string, meta?: unknown) => log('debug', context, message, meta),
    info: (message: string, meta?: unknown) => log('info', context, message, meta),
    warn: (message: string, meta?: unknown) => log('warn', context, message, meta),
    error: (message: string, meta?: unknown) => log('error', context, message, meta),
  }
}
