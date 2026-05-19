/**
 * src/pages/SearchPage.jsx
 *
 * WHY controlled inputs + URL search params?
 *
 * Storing filters in URL search params (e.g. /search?keyword=galaxy&page=2)
 * means users can bookmark a search, share a link, and use browser back/forward.
 * This is standard UX for search pages.
 *
 * useSearchParams() from React Router reads and writes URL params,
 * keeping your UI state in sync with the URL automatically.
 */

import { useState } from "react";
import { useSearchParams } from "react-router-dom";
import { useApodSearch } from "../hooks/useApod";
import ApodCard from "../components/ui/ApodCard";

export default function SearchPage() {
  const [searchParams, setSearchParams] = useSearchParams();

  // Read current filters from URL
  const keyword = searchParams.get("keyword") || "";
  const page = parseInt(searchParams.get("page") || "1");

  // Local state for the input field
  const [inputValue, setInputValue] = useState(keyword);

  const { data, isLoading, isError } = useApodSearch({
    keyword: keyword || undefined,
    page,
    page_size: 12,
  });

  const handleSearch = (e) => {
    e.preventDefault();
    setSearchParams({ keyword: inputValue, page: "1" });
  };

  const goToPage = (newPage) => {
    setSearchParams({ keyword, page: newPage.toString() });
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  return (
    <div className="fade-in" style={{ maxWidth: '1000px', margin: '0 auto' }}>
      <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
        <h1 style={{ fontSize: '3rem', marginBottom: '1rem' }}>Search the Cosmos</h1>
        <p style={{ color: 'var(--text-muted)' }}>Find historical astronomy pictures by keyword.</p>
      </div>

      {/* Search form */}
      <form onSubmit={handleSearch} style={{ display: 'flex', gap: '1rem', marginBottom: '3rem', justifyContent: 'center' }}>
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="e.g. galaxy, nebula, Mars..."
          className="input-glass"
          style={{ maxWidth: '500px', fontSize: '1.1rem' }}
        />
        <button type="submit" className="btn-primary">
          Search
        </button>
      </form>

      {/* Results */}
      {isLoading && (
        <div className="loader-container">
          <div className="spinner"></div>
          <p>Scanning the archives...</p>
        </div>
      )}

      {isError && (
        <div className="glass-panel" style={{ padding: '3rem', textAlign: 'center' }}>
          <h3 style={{ color: '#ff6b6b' }}>Search failed. Please try again.</h3>
        </div>
      )}

      {data && (
        <div className="slide-up">
          <p style={{ color: 'var(--text-muted)', marginBottom: '2rem', textAlign: 'center' }}>
            Found {data.total} result{data.total !== 1 ? "s" : ""}
            {keyword && ` for "${keyword}"`}
          </p>

          <div style={{ 
            display: 'grid', 
            gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', 
            gap: '2rem' 
          }}>
            {data.items.map((apod) => (
              <ApodCard key={apod.date} apod={apod} />
            ))}
          </div>

          {/* Pagination */}
          {data.total > 12 && (
            <div style={{ 
              display: 'flex', 
              justifyContent: 'center', 
              alignItems: 'center', 
              gap: '1.5rem',
              marginTop: '4rem' 
            }}>
              <button
                onClick={() => goToPage(page - 1)}
                disabled={page === 1}
                className="btn-secondary"
              >
                Previous
              </button>
              <span style={{ color: 'var(--text-muted)', fontWeight: 500 }}>
                Page {page} of {Math.ceil(data.total / 12)}
              </span>
              <button
                onClick={() => goToPage(page + 1)}
                disabled={!data.has_next}
                className="btn-secondary"
              >
                Next
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
