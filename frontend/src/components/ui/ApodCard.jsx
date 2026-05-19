/**
 * src/components/ui/ApodCard.jsx
 *
 * WHY a reusable card component?
 *
 * The same APOD card appears in search results, the archive grid, and anywhere
 * else you list APODs. Defining it once means:
 *   - One place to fix a bug
 *   - One place to change the design
 *   - Props make it flexible without duplication
 *
 * This is the "single source of truth" principle applied to UI.
 */

import { Link } from "react-router-dom";

export default function ApodCard({ apod }) {
  return (
    <Link
      to={`/date/${apod.date}`}
      className="glass-panel"
      style={{ 
        display: 'block', 
        overflow: 'hidden', 
        textDecoration: 'none',
        transition: 'transform 0.3s ease, box-shadow 0.3s ease',
        cursor: 'pointer'
      }}
      onMouseEnter={(e) => {
        e.currentTarget.style.transform = 'translateY(-5px)';
        e.currentTarget.style.boxShadow = '0 12px 40px rgba(140, 100, 255, 0.2)';
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.transform = 'translateY(0)';
        e.currentTarget.style.boxShadow = '0 8px 32px 0 rgba(0, 0, 0, 0.4)';
      }}
    >
      {/* Thumbnail */}
      <div style={{ aspectRatio: '16/9', overflow: 'hidden', backgroundColor: 'var(--bg-deep)' }}>
        {apod.media_type === "image" ? (
          <img
            src={apod.url}
            alt={apod.title}
            style={{ 
              width: '100%', 
              height: '100%', 
              objectFit: 'cover',
              transition: 'transform 0.5s ease'
            }}
            onMouseEnter={(e) => e.currentTarget.style.transform = 'scale(1.05)'}
            onMouseLeave={(e) => e.currentTarget.style.transform = 'scale(1)'}
            loading="lazy"
          />
        ) : (
          <div style={{ width: '100%', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <span style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>▶ Video Embed</span>
          </div>
        )}
      </div>

      {/* Text */}
      <div style={{ padding: '1.2rem' }}>
        <p style={{ fontSize: '0.8rem', color: 'var(--accent-secondary)', marginBottom: '0.4rem', fontWeight: 600 }}>
          {apod.date}
        </p>
        <p style={{ 
          fontSize: '1rem', 
          fontWeight: 500, 
          color: 'var(--text-main)', 
          margin: 0,
          display: '-webkit-box',
          WebkitLineClamp: 2,
          WebkitBoxOrient: 'vertical',
          overflow: 'hidden'
        }}>
          {apod.title}
        </p>
      </div>
    </Link>
  );
}
