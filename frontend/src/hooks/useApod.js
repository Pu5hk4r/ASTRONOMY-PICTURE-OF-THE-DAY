/**
 * src/hooks/useApod.js
 *
 * WHY TanStack Query instead of useEffect + useState?
 *
 * The naive approach (useEffect + fetch + useState) forces you to manually handle:
 *   - loading state
 *   - error state
 *   - caching (if user goes back, do you refetch?)
 *   - deduplication (if two components need today's APOD, do you fetch twice?)
 *   - stale data (when do you refetch in the background?)
 *
 * TanStack Query handles ALL of that. You write one hook, get everything.
 *
 * HOW useQuery works:
 *   queryKey: a unique array that identifies this query. If two components
 *             use the same key, they share the same cached result — no duplicate fetches.
 *   queryFn:  the async function that fetches data
 *   staleTime: how long before the data is considered stale and refetched
 *
 * WHY staleTime: 5 * 60 * 1000 (5 minutes) for today's APOD?
 *   APOD changes once per day. No point refetching every time the user
 *   switches browser tabs. 5 minutes is a good balance.
 */

import { useQuery } from "@tanstack/react-query";
import { apodApi } from "../api/apodApi";

export function useTodayApod() {
  return useQuery({
    queryKey: ["apod", "today"],
    queryFn: apodApi.getToday,
    staleTime: 5 * 60 * 1000,   // 5 minutes
    retry: 2,                    // retry failed requests twice before showing error
  });
}

export function useApodByDate(date) {
  return useQuery({
    queryKey: ["apod", "date", date],
    queryFn: () => apodApi.getByDate(date),
    enabled: !!date,             // WHY enabled? Don't run the query if date is null/undefined
    staleTime: Infinity,         // Historical APODs never change — cache forever
  });
}

export function useApodSearch(params) {
  return useQuery({
    queryKey: ["apod", "search", params],   // params object is part of the key
    queryFn: () => apodApi.search(params),  // so different filters = different cache entries
    staleTime: 2 * 60 * 1000,
    placeholderData: (prev) => prev,        // WHY? Show previous page while next page loads
                                            // instead of showing a loading spinner
  });
}

export function useApodStats() {
  return useQuery({
    queryKey: ["apod", "stats"],
    queryFn: apodApi.getStats,
    staleTime: 30 * 1000,       // stats change as new APODs are added
  });
}
