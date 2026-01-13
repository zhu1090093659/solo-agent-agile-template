import { useState, useCallback } from 'react'
import api, { ApiError } from '@/lib/api'

interface UseApiState<T> {
  data: T | null
  error: ApiError | null
  isLoading: boolean
}

interface UseApiReturn<T> extends UseApiState<T> {
  execute: (...args: unknown[]) => Promise<T | null>
  reset: () => void
}

/**
 * Custom hook for API calls with loading and error states.
 * 
 * @example
 * const { data, error, isLoading, execute } = useApi<User[]>()
 * 
 * useEffect(() => {
 *   execute(() => api.get('/users'))
 * }, [])
 */
export function useApi<T>(): UseApiReturn<T> {
  const [state, setState] = useState<UseApiState<T>>({
    data: null,
    error: null,
    isLoading: false,
  })

  const execute = useCallback(async (
    apiCall: () => Promise<T>
  ): Promise<T | null> => {
    setState(prev => ({ ...prev, isLoading: true, error: null }))
    
    try {
      const data = await apiCall()
      setState({ data, error: null, isLoading: false })
      return data
    } catch (error) {
      const apiError = error instanceof ApiError 
        ? error 
        : new ApiError(500, 'Unknown error', error)
      setState({ data: null, error: apiError, isLoading: false })
      return null
    }
  }, [])

  const reset = useCallback(() => {
    setState({ data: null, error: null, isLoading: false })
  }, [])

  return { ...state, execute, reset }
}

export default useApi
