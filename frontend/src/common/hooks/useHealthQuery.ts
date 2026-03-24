import { useQuery } from '@tanstack/react-query'

import { getHealth } from '../../config/api'

export function useHealthQuery() {
  return useQuery({
    queryKey: ['health'],
    queryFn: getHealth,
    refetchInterval: 30000,
  })
}
