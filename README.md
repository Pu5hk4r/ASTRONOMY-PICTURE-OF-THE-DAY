# 🌌 APOD Explorer

APOD Explorer is a full-stack web application designed to bring the universe to your screen. Powered by the NASA Astronomy Picture of the Day (APOD) API, it features a stunning, premium UI with a cosmic theme, glassmorphism design, and robust caching via a FastAPI backend.

![APOD Explorer Banner](frontend/src/assets/hero.png) *(Note: Add a screenshot of your beautiful UI here!)*

---

## ✨ Key Features

### 🎨 Frontend (React + Vite)
- **Premium Cosmic UI**: A custom-built, vanilla CSS design system featuring a dynamic, multi-layered starry background animation and elegant glassmorphism panels.
- **Today's APOD**: Instantly view today's stunning astronomy image or video with an accompanying scientific explanation.
- **Cosmic Archive Search**: Search through historical APODs by keyword with a responsive grid layout and hover micro-animations.
- **Time Travel (By Date)**: Use the built-in calendar picker to travel back in time and discover the APOD for any specific historical date.
- **Live Stats**: View real-time statistics of the archived pictures, videos, and images in the glowing footer.
- **State Management**: Utilizes **TanStack Query** for intelligent caching, background refetching, and seamless loading states.
- **Routing**: Client-side routing with **React Router v6**.

### ⚙️ Backend (FastAPI + Python)
- **NASA API Integration**: Seamlessly fetches and processes data from the official NASA APOD API.
- **High Performance**: Built with **FastAPI** for lightning-fast asynchronous request handling.
- **Modular Architecture**: Clean separation of concerns with dedicated routers and service layers.
- **CORS Configured**: Fully configured to allow seamless communication with the frontend dev server.

---

## 🛠️ Technology Stack

| Frontend | Backend | DevOps |
| --- | --- | --- |
| React 19 | FastAPI | Docker |
| Vite | Uvicorn | Docker Compose |
| React Router v6 | Python 3 | Git |
| TanStack Query | Axios | |
| Vanilla CSS (Glassmorphism) | | |

---

## 🚀 Getting Started

### Prerequisites
- Node.js (v18+)
- Python (3.9+)
- NASA API Key (Optional, defaults to `DEMO_KEY`)

### 1. Backend Setup

Open a terminal and navigate to the `backend` directory:
```bash
cd backend
```

Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

Set up your environment variables (create a `.env` file based on `.env.example`):
```env
NASA_API_KEY=your_api_key_here
```

Run the FastAPI server:
```bash
uvicorn app.main:app --reload --port 8000
```
*The backend will now be running at http://localhost:8000*

### 2. Frontend Setup

Open a new terminal and navigate to the `frontend` directory:
```bash
cd frontend
```

Install dependencies:
```bash
npm install
```

Start the Vite development server:
```bash
npm run dev
```
*The frontend will now be running at http://localhost:5174 (or 5173)*

---

## 🐳 Docker Setup (Optional)

If you prefer to run the entire stack using Docker, a `docker-compose.yml` file is included at the root of the project.

```bash
docker-compose up --build
```
This will spin up both the FastAPI backend and the React frontend in isolated containers.

---

## 📂 Project Structure

```text
apod-explorer/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI entry point
│   │   ├── routers/         # API Route definitions
│   │   └── services/        # Business logic and NASA API integration
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── api/             # Axios API client
│   │   ├── components/      # Reusable UI components (Layout, ApodCard)
│   │   ├── hooks/           # TanStack Query custom hooks
│   │   ├── pages/           # Route components (Today, Search, Date)
│   │   ├── index.css        # Premium Cosmic CSS Design System
│   │   └── main.jsx         # React application entry point
│   ├── package.json
│   └── vite.config.js
└── docker-compose.yml
```

---

## 🎨 Design Philosophy

The UI was crafted with a "Premium & Alive" philosophy:
- **No Tailwind Dependency**: Built entirely with Vanilla CSS for maximum control over complex animations and pseudo-elements.
- **Glassmorphism**: Extensive use of `backdrop-filter: blur` to create depth against the starry background.
- **Micro-interactions**: Hovering over cards scales the images and elevates the containers with glowing shadows, making the interface feel responsive and modern.

---

## 📝 License

This project is licensed under the MIT License.

*Powered by the [NASA API](https://api.nasa.gov/). Crafted for the cosmos.*
