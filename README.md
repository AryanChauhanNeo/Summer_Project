# 🚀 Mars Rover Monitoring & Navigation Simulator

> A modular Mars Rover Mission Control System that simulates rover telemetry, AI navigation, terrain analysis, and a real-time mission dashboard using FastAPI and Streamlit.
---

# 📖 Project Overview

This project simulates a **Mars Rover Mission Control System** where different independent modules communicate through a centralized FastAPI backend.

The rover continuously generates telemetry data, a navigation engine computes the optimal route, and a Streamlit dashboard visualizes the rover's status in real time.

The project demonstrates concepts commonly used in industrial IIoT and robotics systems such as:

- Real-time telemetry streaming
- REST API communication
- Modular microservice architecture
- Mission monitoring dashboard
- Team-based backend integration
- Simulation-driven testing

---

# 🏗 System Architecture

```
                 +-----------------------+
                 |  Rover Simulation     |
                 |  (Telemetry Module)   |
                 +-----------+-----------+
                             |
                    POST /telemetry
                             |
                             ▼
                  +----------------------+
                  |   FastAPI Backend    |
                  |  Shared API Server   |
                  +----+-----------+-----+
                       |           |
          GET /telemetry      GET /navigation
                       |           |
                       ▼           ▼
               +-------------------------+
               | Streamlit Dashboard     |
               | Mission Control UI      |
               +-------------------------+

                             ▲
                             |
                    POST /navigation
                             |
                 +-----------------------+
                 | Navigation Engine     |
                 | (Path Planning)       |
                 +-----------------------+
```

---

# ✨ Features

## 🚗 Rover Simulation

- Simulates rover movement
- Generates live telemetry
- Battery monitoring
- Temperature monitoring
- Speed tracking
- Mission logging

---

## 🛰 Telemetry Module

Generates structured telemetry including:

- Timestamp
- Current Position
- Destination
- Rover State
- Speed
- Battery Level
- Temperature
- Obstacle Detection

Example:

```json
{
  "timestamp": "...",
  "system_status": {
    "state": "MOVING",
    "speed_kmh": 2.3
  },
  "navigation": {
    "current_position": [5,7],
    "destination": [15,20]
  },
  "sensors": {
    "battery_level_percent": 91,
    "temperature_celsius": -42,
    "obstacle_detected": false
  }
}
```

---

## 🧭 Navigation Engine

Computes rover route and provides:

- Planned Route
- Distance Remaining
- Heading
- Estimated Time
- Obstacles

Example:

```json
{
    "route": [[5,7],[6,8],[7,9]],
    "obstacles": [],
    "distance_remaining": 15,
    "heading": "NE",
    "estimated_time_sec": 48
}
```

---

## 📊 Mission Control Dashboard

Built using Streamlit.

Displays:

- Live Rover Position
- Navigation Route
- Battery Percentage
- Temperature
- Rover Speed
- Distance Remaining
- Mission Status
- Terrain Visualization

---

# ⚙ Tech Stack

| Layer | Technology |
|--------|------------|
| Language | Python |
| Backend | FastAPI |
| Dashboard | Streamlit |
| API | REST API |
| Visualization | Plotly |
| HTTP Client | Requests |
| Validation | Pydantic |
| Deployment | Render |

---

# 📁 Project Structure

```
mars-rover-monitoring/

│
├── backend/
│   ├── app/
│   ├── routes/
│   ├── models/
│   ├── services/
│   └── main.py
│
├── dashboard/
│   ├── components/
│   ├── pages/
│   ├── services/
│   ├── data/
│   └── app.py
│
├── Navigation/
│
├── telemetry/
│
├── terrain/
│
├── rover/
│
├── sensors/
│
└── README.md
```

---

# 🔌 REST API

## Telemetry

### POST

```
POST /telemetry
```

Uploads rover telemetry.

### GET

```
GET /telemetry
```

Returns latest rover telemetry.

---

## Navigation

### POST

```
POST /navigation
```

Uploads navigation plan.

### GET

```
GET /navigation
```

Returns latest planned route.

---

## Terrain

### POST

```
POST /terrain
```

Uploads terrain information.

### GET

```
GET /terrain
```

Returns terrain map.

---

# 🚀 Getting Started

## Clone Repository

```bash
git clone https://github.com/yourusername/mars-rover-monitoring.git
```

---

## Backend

```bash
cd backend

pip install -r requirements.txt

uvicorn app.main:app --reload
```

Backend:

```
http://127.0.0.1:8000
```

Swagger:

```
http://127.0.0.1:8000/docs
```

---

## Dashboard

```bash
cd dashboard

pip install -r requirements.txt

python -m streamlit run app.py
```

---

# ☁ Deployment

Backend deployed on **Render**

```
https://mars-rover-backend.onrender.com
```

Dashboard communicates with the deployed backend using REST APIs.

---

# 👥 Team Responsibilities

### Member 1 — Rover Telemetry

Responsible for:

- Rover Simulation
- Telemetry Generation
- Battery
- Temperature
- Speed
- Telemetry API Integration

---

### Member 2 — Navigation

Responsible for:

- Path Planning
- Route Generation
- Obstacle Detection
- Navigation API Integration

---

### Member 3 — Mission Control Dashboard

Responsible for:

- Streamlit Dashboard
- API Integration
- Live Visualization
- Mission Monitoring
- Data Processing

---

# 📌 Engineering Highlights

- Modular architecture
- REST-based communication
- Separation of concerns
- Centralized backend
- Real-time dashboard updates
- Team-friendly development workflow
- Easy deployment on cloud

---

# 🔮 Future Enhancements

- WebSocket-based live streaming
- MongoDB persistence
- User authentication
- AI obstacle avoidance
- Rover command center
- Multi-rover support
- Historical mission analytics
- Docker & Kubernetes deployment

---

# 🎯 Interview Talking Points

This project demonstrates practical backend engineering concepts beyond basic CRUD applications:

- Designing REST APIs with FastAPI
- Building modular services
- Integrating multiple independent modules through a shared backend
- Processing real-time telemetry data
- Separating simulation, backend, and visualization layers
- Creating a live monitoring dashboard with Streamlit
- Deploying services to the cloud using Render
- Collaborating in a Git-based multi-developer workflow

---

# 📜 License

This project is intended for educational and demonstration purposes.
