/**
 * src/pages/TodayPage.jsx
 *
 * WHY is this component so thin?
 *
 * This component's job is to RENDER, not to fetch or process data.
 *   - Data fetching → useApod hook (which calls TanStack Query)
 *   - API calls → apodApi
 *   - Business logic → FastAPI backend
 *
 * This separation means you can change how data is fetched
 * without touching a single line of JSX.
 */

import { useTodayApod } from "../hooks/useApod";

export default function TodayPage() {
  const { data: apod, isLoading, isError, error } = useTodayApod();

  if (isLoading) {
    return (
      <div className="loader-container">
        <div className="spinner"></div>
        <p>Fetching today's cosmos...</p>
      </div>
    );
  }

  if (isError) {
    return (
      <div className="glass-panel" style={{ padding: '3rem', textAlign: 'center', marginTop: '2rem' }}>
        <h2 style={{ color: '#ff6b6b' }}>Failed to load APOD</h2>
        <p>{error.message}</p>
      </div>
    );
  }

  return (
    <div className="fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      {/* Hero Media Section */}
      <div className="glass-panel slide-up" style={{ padding: '1rem', borderRadius: '24px' }}>
        {apod.media_type === "image" ? (
          <img
            src={apod.hdurl || apod.url}
            alt={apod.title}
            style={{ 
              width: "100%", 
              maxHeight: "75vh", 
              objectFit: "cover", 
              borderRadius: "16px",
              display: "block" 
            }}
            loading="lazy"
          />
        ) : (
          <div style={{ aspectRatio: "16/9", borderRadius: "16px", overflow: "hidden" }}>
            <iframe
              src={apod.url}
              title={apod.title}
              style={{ width: "100%", height: "100%", border: "none" }}
              allowFullScreen
            />
          </div>
        )}
      </div>

      {/* Content Section */}
      <div className="glass-panel slide-up" style={{ padding: '3rem', animationDelay: '0.2s' }}>
        <div style={{ borderBottom: '1px solid var(--border-glass)', paddingBottom: '1.5rem', marginBottom: '1.5rem' }}>
          <p style={{ color: 'var(--accent-secondary)', fontWeight: 600, letterSpacing: '1px', fontSize: '0.9rem', textTransform: 'uppercase' }}>
            {apod.date}
          </p>
          <h1 style={{ margin: '0.5rem 0', fontSize: 'clamp(2rem, 4vw, 3.5rem)' }}>
            {apod.title}
          </h1>
          {apod.copyright && (
            <p style={{ color: 'var(--text-muted)', fontStyle: 'italic' }}>
              Captured by © {apod.copyright}
            </p>
          )}
        </div>
        
        <p style={{ 
          fontSize: '1.15rem', 
          lineHeight: '1.8', 
          color: 'var(--text-main)', 
          maxWidth: '900px', 
          margin: '0 auto' 
        }}>
          {apod.explanation}
        </p>
      </div>
    </div>
  );
}
