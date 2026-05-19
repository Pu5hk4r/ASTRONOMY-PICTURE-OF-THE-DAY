/**
 * src/main.jsx — App entry point
 *
 * WHY QueryClientProvider wraps everything?
 * TanStack Query uses a QueryClient to store its cache.
 * Wrapping the app in QueryClientProvider makes the cache available
 * to every component — no prop drilling needed.
 *
 * WHY BrowserRouter wraps everything?
 * React Router needs to read the browser URL to know which page to show.
 * BrowserRouter provides that context to all nested Route components.
 */

import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import App from "./App";
import "./index.css";   // Tailwind base styles

// WHY these defaults?
// staleTime: 0 means data is immediately stale (TanStack Query default)
// We override per-query in useApod.js where appropriate.
// retry: 1 — retry failed requests once. NASA API can have transient errors.
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,  // don't refetch when user alt-tabs back
    },
  },
});

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <App />
      </BrowserRouter>
      {/* ReactQueryDevtools: visible only in dev — lets you inspect the cache */}
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  </React.StrictMode>
);
