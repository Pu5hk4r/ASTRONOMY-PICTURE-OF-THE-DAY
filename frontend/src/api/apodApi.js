/**
 * src/api/apodApi.js
 *
 * WHY a dedicated API layer?
 * Same reason as the backend service layer: keep fetch() calls out of components.
 * Components describe UI. This file owns all communication with your FastAPI backend.
 *
 * HOW Axios works:
 *   - baseURL: prepended to every request — you only write "/apod/today" not the full URL
 *   - interceptors: middleware for requests and responses
 *   - The request interceptor here handles auth (if you add it later)
 *   - The response interceptor normalises errors into a consistent shape
 */

import axios from "axios";

// WHY import.meta.env? Vite exposes env variables prefixed with VITE_
// from your .env file. This lets you use a different backend URL in dev vs prod.
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000/api",
  timeout: 10000,
});

// Response interceptor — transform errors into consistent objects
api.interceptors.response.use(
  (response) => response.data,   // unwrap .data so callers get the payload directly
  (error) => {
    const message =
      error.response?.data?.detail ||
      error.message ||
      "Something went wrong";
    return Promise.reject(new Error(message));
  }
);

// --- APOD endpoints ---

export const apodApi = {
  /** Fetch today's APOD */
  getToday: () => api.get("/apod/today"),

  /** Fetch APOD for a specific date (YYYY-MM-DD) */
  getByDate: (date) => api.get(`/apod/date/${date}`),

  /**
   * Search APODs with optional filters
   * @param {Object} params - { keyword, start_date, end_date, media_type, page, page_size }
   */
  search: (params = {}) => api.get("/apod/search", { params }),

  /** Get archive statistics */
  getStats: () => api.get("/apod/stats"),
};
