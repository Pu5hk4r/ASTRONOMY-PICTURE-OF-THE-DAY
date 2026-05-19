import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useApodByDate } from "../hooks/useApod";

export default function DatePage() {
  const { dateParam } = useParams();
  const navigate = useNavigate();
  
  // Default to today if no date in URL
  const todayStr = new Date().toISOString().split("T")[0];
  const [selectedDate, setSelectedDate] = useState(dateParam || todayStr);

  const { data: apod, isLoading, isError, error } = useApodByDate(dateParam);

  // Sync state when URL param changes
  useEffect(() => {
    if (dateParam) {
      setSelectedDate(dateParam);
    }
  }, [dateParam]);

  const handleDateChange = (e) => {
    const newDate = e.target.value;
    setSelectedDate(newDate);
    navigate(`/date/${newDate}`);
  };

  return (
    <div className="fade-in">
      <div className="date-picker-section glass-panel" style={{ padding: "2rem", marginBottom: "2rem", textAlign: "center" }}>
        <h2>Time Travel</h2>
        <p style={{ color: "var(--text-muted)", marginBottom: "1.5rem" }}>
          Select a date to view a historical Astronomy Picture of the Day.
        </p>
        <input 
          type="date" 
          value={selectedDate}
          max={todayStr}
          onChange={handleDateChange}
          className="input-glass"
          style={{ width: "auto", minWidth: "250px", fontSize: "1.2rem", padding: "1rem" }}
        />
      </div>

      {!dateParam ? (
        <div className="glass-panel" style={{ padding: "4rem 2rem", textAlign: "center" }}>
          <h3 style={{ color: "var(--text-muted)" }}>Please select a date above to begin your journey.</h3>
        </div>
      ) : isLoading ? (
        <div className="loader-container">
          <div className="spinner"></div>
          <p>Traveling through time...</p>
        </div>
      ) : isError ? (
        <div className="glass-panel" style={{ padding: "3rem", textAlign: "center" }}>
          <h3 style={{ color: "#ff6b6b", marginBottom: "1rem" }}>Failed to load APOD</h3>
          <p>{error.message}</p>
        </div>
      ) : apod ? (
        <div className="glass-panel slide-up" style={{ padding: "2rem" }}>
          <div style={{ marginBottom: "1.5rem" }}>
            <p style={{ color: "var(--accent-primary)", fontWeight: "600", fontSize: "0.9rem" }}>{apod.date}</p>
            <h1 style={{ margin: "0.5rem 0" }}>{apod.title}</h1>
            {apod.copyright && <p style={{ color: "var(--text-muted)", fontSize: "0.9rem" }}>© {apod.copyright}</p>}
          </div>

          {apod.media_type === "image" ? (
            <img
              src={apod.hdurl || apod.url}
              alt={apod.title}
              style={{ width: "100%", borderRadius: "12px", marginBottom: "2rem", border: "1px solid var(--border-glass)" }}
              loading="lazy"
            />
          ) : (
            <div style={{ aspectRatio: "16/9", marginBottom: "2rem", borderRadius: "12px", overflow: "hidden", border: "1px solid var(--border-glass)" }}>
              <iframe
                src={apod.url}
                title={apod.title}
                style={{ width: "100%", height: "100%", border: "none" }}
                allowFullScreen
              />
            </div>
          )}

          <p style={{ fontSize: "1.1rem", lineHeight: "1.8", color: "var(--text-main)" }}>
            {apod.explanation}
          </p>
        </div>
      ) : null}
    </div>
  );
}
