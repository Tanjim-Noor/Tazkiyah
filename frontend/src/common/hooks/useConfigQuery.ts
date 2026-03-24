import { useQuery } from '@tanstack/react-query'

import { getConfig } from '../../config/api'

export function useConfigQuery() {
  return useQuery({
    queryKey: ['config'],
    queryFn: getConfig,
    staleTime: 30000,
  })
}
