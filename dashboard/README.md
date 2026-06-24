# 🚀 Mars Rover Mission Control Dashboard

A production-quality **Streamlit** recreation of the v0-generated React/Next.js
Mars Rover Mission Control Dashboard.

## Features

- **Header** – Mission title, class, and animated ACTIVE status indicator
- **Telemetry Panel** – Live-simulated X/Y coordinates, battery (with progress
  bar), temperature, speed, signal strength, and system status
- **Navigation & Terrain** – Plotly terrain map with grid, elevation contours,
  mountain ridges, craters, rock clusters, rover position (pulsing), destination
  target, obstacles, and planned waypoint route
- **Mission Logs** – Scrollable timestamped log feed with colour-coded levels
- **Alerts & Warnings** – Critical / warning alert cards with summary counts
- **Auto-refresh** – Dashboard ticks every ~3 s, simulating a live rover feed

## Quick start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the dashboard
python -m streamlit run app.py
```

Open **http://localhost:8501** – you'll land on the Home page; click
**Launch Mission Dashboard** (or use the sidebar) to view the live dashboard.

## Project structure

```
dashboard/
├── app.py                     # Entry point – page config, CSS, routing
├── pages/
│   ├── home.py                # Landing page
│   └── dashboard.py           # Main dashboard page (assembles all panels)
├── components/
│   ├── header.py              # MARS ROVER MISSION CONTROL header bar
│   ├── telemetry_panel.py     # Left column – telemetry cards
│   ├── navigation_panel.py    # Centre panel – Plotly terrain + nav stats
│   ├── mission_logs.py        # Bottom-left – scrollable log feed
│   └── alerts_panel.py        # Bottom-right – alert cards
├── services/
│   ├── api_client.py          # HTTP client (falls back to JSON when offline)
│   ├── telemetry_service.py   # Random-walk simulator around base JSON values
│   └── navigation_service.py  # Terrain, route, obstacle data
├── assets/
│   └── styles.css             # NASA dark-theme CSS (no Tailwind)
├── data/
│   ├── telemetry.json         # Base rover telemetry values
│   ├── alerts.json            # Initial alert entries
│   └── logs.json              # Initial mission log entries
├── requirements.txt
└── README.md
```

## Connecting a FastAPI backend

The dashboard is designed for zero-modification integration.

### Member 1 – Rover Simulator

Expose these endpoints from your FastAPI app:

| Method | Path            | Response schema              |
|--------|-----------------|------------------------------|
| GET    | `/api/telemetry`| `telemetry.json` object      |
| GET    | `/api/alerts`   | array of alert objects       |
| GET    | `/api/logs`     | array of log objects         |

Then set the environment variable before starting Streamlit:

```bash
export ROVER_API_URL=http://localhost:8000
python -m streamlit run app.py
```

### Member 2 – Navigation Engine

Expose:

| Method | Path             | Response schema              |
|--------|------------------|------------------------------|
| GET    | `/api/navigation` | navigation data object      |

```bash
export NAV_API_URL=http://localhost:8001
python -m streamlit run app.py
```

When neither variable is set the dashboard runs fully offline using the
bundled JSON files – no backend required.

## Colour palette

| Token      | Hex       | Usage                          |
|------------|-----------|-------------------------------|
| background | `#1a1a1a` | Page background                |
| card       | `#1e2130` | Panel / card background        |
| primary    | `#00bfff` | Headings, rover marker, links  |
| secondary  | `#7c22e0` | Heading accent, mountain fills |
| accent     | `#ffaa00` | Mission title, destination     |
| danger     | `#ef4444` | Critical alerts, obstacles     |
| warning    | `#facc15` | Warning alerts                 |
| success    | `#4ade80` | Moving status, nominal         |
