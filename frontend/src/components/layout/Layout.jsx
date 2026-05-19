import { Link, NavLink, Outlet } from "react-router-dom";
import { useApodStats } from "../../hooks/useApod";

export default function Layout() {
  const { data: stats } = useApodStats();

  return (
    <div className="app-container">
      {/* Navbar */}
      <header className="glass-panel" style={{ 
        position: 'sticky', 
        top: '1rem', 
        zIndex: 100, 
        margin: '1rem auto',
        width: 'calc(100% - 2rem)',
        maxWidth: '1200px',
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center', 
        padding: '1rem 2rem' 
      }}>
        <Link to="/" style={{ display: 'flex', alignItems: 'center', gap: '0.8rem', textDecoration: 'none' }}>
          <div style={{ 
            width: '36px', 
            height: '36px', 
            background: 'linear-gradient(135deg, var(--accent-primary), var(--accent-secondary))',
            borderRadius: '50%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 0 15px var(--accent-glow)'
          }}>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"></path>
              <path d="M2 12h20"></path>
            </svg>
          </div>
          <h1 style={{ fontSize: '1.4rem', margin: 0, fontWeight: 700, color: 'white' }}>
            APOD <span style={{ color: 'var(--accent-primary)' }}>Explorer</span>
          </h1>
        </Link>
        
        <nav style={{ display: 'flex', gap: '2rem' }}>
          <NavLink 
            to="/" 
            end
            style={({ isActive }) => ({
              color: isActive ? 'var(--accent-secondary)' : 'var(--text-main)',
              fontWeight: isActive ? '600' : '400',
              textShadow: isActive ? '0 0 10px rgba(0, 210, 255, 0.4)' : 'none'
            })}
          >
            Today
          </NavLink>
          <NavLink 
            to="/search" 
            style={({ isActive }) => ({
              color: isActive ? 'var(--accent-secondary)' : 'var(--text-main)',
              fontWeight: isActive ? '600' : '400',
              textShadow: isActive ? '0 0 10px rgba(0, 210, 255, 0.4)' : 'none'
            })}
          >
            Search
          </NavLink>
          <NavLink 
            to="/date" 
            style={({ isActive }) => ({
              color: isActive ? 'var(--accent-secondary)' : 'var(--text-main)',
              fontWeight: isActive ? '600' : '400',
              textShadow: isActive ? '0 0 10px rgba(0, 210, 255, 0.4)' : 'none'
            })}
          >
            Archive
          </NavLink>
        </nav>
      </header>

      {/* Main Content Area */}
      <main className="main-content">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="glass-panel" style={{ 
        margin: '2rem auto', 
        width: 'calc(100% - 2rem)',
        maxWidth: '1200px',
        padding: '2rem',
        textAlign: 'center',
        borderBottom: 'none',
        borderRadius: '16px 16px 0 0'
      }}>
        <div style={{ display: 'flex', justifyContent: 'center', gap: '3rem', marginBottom: '1.5rem', flexWrap: 'wrap' }}>
          <div style={{ textAlign: 'center' }}>
            <p style={{ fontSize: '2rem', fontWeight: 700, color: 'var(--accent-secondary)', margin: 0 }}>
              {stats ? stats.total_apods : '...'}
            </p>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>APODs Archived</p>
          </div>
          <div style={{ textAlign: 'center' }}>
            <p style={{ fontSize: '2rem', fontWeight: 700, color: 'var(--accent-primary)', margin: 0 }}>
              {stats ? stats.total_images : '...'}
            </p>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>Images</p>
          </div>
          <div style={{ textAlign: 'center' }}>
            <p style={{ fontSize: '2rem', fontWeight: 700, color: '#ff6b6b', margin: 0 }}>
              {stats ? stats.total_videos : '...'}
            </p>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>Videos</p>
          </div>
        </div>
        
        <p style={{ color: 'var(--text-muted)', fontSize: '0.8rem', borderTop: '1px solid var(--border-glass)', paddingTop: '1.5rem' }}>
          Powered by NASA API and your local FastAPI Backend. <br/>
          Crafted with ♥ for the cosmos.
        </p>
      </footer>
    </div>
  );
}