import {
  QueryClient,
  QueryClientProvider,
} from '@tanstack/react-query'
import type { PropsWithChildren } from 'react'
import { useMemo } from 'react'

import { AppErrorBoundary } from '../config/error'

export function AppProvider({ children }: PropsWithChildren) {
  const queryClient = useMemo(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            retry: 1,
            refetchOnWindowFocus: false,
          },
        },
      }),
    [],
  )

  return (
    <AppErrorBoundary>
      <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
    </AppErrorBoundary>
  )
}
