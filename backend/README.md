# Mars Rover Monitoring & Navigation — Backend

Shared FastAPI backend for the **Smart Mars Rover Monitoring & Navigation
Simulator** team project. It is the single integration point between all
three team members, who work from different cities:

| Member | Responsibility | Talks to backend via |
|---|---|---|
| **Member 1** | Rover / Battery / Temperature simulation, telemetry generation | `POST /telemetry` |
| **Member 2** | AI Navigation, A* pathfinding, obstacle detection | `POST /navigation` |
| **Member 3 (You)** | Streamlit dashboard, backend, integration, testing | `GET /telemetry`, `GET /navigation` |

```
Member 1 ──POST /telemetry──▶  ┌───────────────┐
                                │   FastAPI      │──GET /telemetry──▶ Dashboard
Member 2 ──POST /navigation──▶ │   Backend      │──GET /navigation─▶ Dashboard
                                └───────────────┘
```

---

## 1. Folder structure

```
backend/
├── app/
│   ├── main.py          # FastAPI app: routers, CORS, exception handlers, startup
│   └── config.py        # Environment-driven settings (host, port, CORS, env)
├── models/
│   ├── telemetry.py      # Pydantic schema for telemetry payloads
│   └── navigation.py     # Pydantic schema for navigation payloads
├── routes/
│   ├── telemetry.py       # POST/GET /telemetry endpoints
│   └── navigation.py      # POST/GET /navigation endpoints
├── services/
│   └── storage.py         # In-memory storage (swap-ready for MongoDB/PostgreSQL)
├── utils/
│   └── logging_config.py  # Centralised logging setup
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

**Why this layout?** Each concern lives in exactly one place:
- **models/** define *what* the data looks like (validation rules, types).
- **routes/** define *how* the data moves in and out (HTTP verbs, status codes).
- **services/** define *where* the data lives (currently in memory).
- **app/** wires everything together and holds configuration.

This means, for example, that switching storage from memory to MongoDB
later only touches `services/storage.py` — routes and models don't change.

---

## 2. API flow

### Telemetry

| Method | Path | Called by | Purpose |
|---|---|---|---|
| `POST` | `/telemetry` | Member 1 | Push the latest rover reading. Overwrites the previous one. |
| `GET` | `/telemetry` | Member 2, Dashboard | Fetch the most recently posted reading. Returns `404` if nothing has been posted yet. |

**Telemetry JSON shape** (see `models/telemetry.py`):
```json
{
  "timestamp": "2026-06-01T11:39:38Z",
  "system_status": { "state": "MOVING", "speed_kmh": 2.0 },
  "navigation": { "current_position": [4, 7], "destination": [9, 9] },
  "sensors": {
    "battery_level_percent": 85.5,
    "temperature_celsius": -62.3,
    "obstacle_detected": false
  }
}
```

### Navigation

| Method | Path | Called by | Purpose |
|---|---|---|---|
| `POST` | `/navigation` | Member 2 | Push the latest planned route. Overwrites the previous one. |
| `GET` | `/navigation` | Dashboard | Fetch the most recently posted route. Returns `404` if nothing has been posted yet. |

**Navigation JSON shape** (see `models/navigation.py`):
```json
{
  "route": [[4, 7], [5, 7], [6, 8], [7, 8], [8, 9], [9, 9]],
  "obstacles": [[5, 6], [7, 7], [8, 8]],
  "distance_remaining": 5.4,
  "heading": "NE",
  "estimated_time_sec": 180
}
```

### GET vs POST, in plain terms

- **POST** = "here is new data, please store it." Used by Member 1 and
  Member 2's simulators, which *generate* new readings.
- **GET** = "give me whatever is currently stored." Used by anything that
  *consumes* data — Member 2 reading rover telemetry, and the dashboard
  reading both telemetry and navigation.

Only the **latest** reading of each type is kept — this mirrors a live
monitoring dashboard, not a historical log.

---

## 3. How each member integrates

### Member 1 (Rover Simulator)
On every simulation tick, `POST` a telemetry JSON (matching the shape
above) to:
```
http://<backend-host>:8000/telemetry
```
A `201 Created` response with the stored data confirms success. A `422`
means the payload didn't match the schema — check the `errors` field in
the response for exactly which field failed.

### Member 2 (AI Navigation)
1. `GET /telemetry` to read the rover's current position and obstacles.
2. Run A* pathfinding / route planning.
3. `POST` the resulting route JSON (matching the shape above) to:
```
http://<backend-host>:8000/navigation
```

### Dashboard (Member 3 / you)
Poll both endpoints on a timer (e.g. every 1–3 seconds):
```
GET http://<backend-host>:8000/telemetry
GET http://<backend-host>:8000/navigation
```
Both return `404` until the first `POST` has happened — handle that
gracefully (e.g. show "Waiting for rover data...").

> **Heads-up on your existing dashboard code:** looking at
> `dashboard/services/api_client.py`, it currently calls
> `{ROVER_API_URL}/api/telemetry` and `{NAV_API_URL}/api/navigation`
> (with an `/api` prefix), and its "live mode" expects the flat
> `x, y, battery, temperature...` shape used by your local demo JSON
> files. This backend implements the routes and JSON shape **exactly as
> specified** in the project brief (`/telemetry`, `/navigation`, nested
> shape shown above) — since the dashboard was explicitly out of scope
> here, I didn't touch it. When you're ready to wire them together,
> you'll want to either (a) point `ROVER_API_URL` at this backend and
> add a small adapter in `api_client.py` that maps this nested schema to
> the flat one your components expect, or (b) ask me to add matching
> `/api/telemetry` and `/api/navigation` aliases on the backend. Either
> is a small change — just flagging it now so it's not a surprise later.

---

## 4. Local development

**Requirements:** Python 3.10+

```bash
cd backend

# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. (optional) copy the env example — defaults already work locally
cp .env.example .env

# 4. Run the server
uvicorn app.main:app --reload
```

The API is now live at **http://localhost:8000**.

- Swagger UI (interactive docs, try requests right in the browser):
  **http://localhost:8000/docs**
- ReDoc (readable reference docs): **http://localhost:8000/redoc**
- Health check: **http://localhost:8000/health**

### Quick manual test with curl

```bash
# Post telemetry
curl -X POST http://localhost:8000/telemetry \
  -H "Content-Type: application/json" \
  -d '{
        "timestamp": "2026-06-01T11:39:38Z",
        "system_status": {"state": "MOVING", "speed_kmh": 2.0},
        "navigation": {"current_position": [4, 7], "destination": [9, 9]},
        "sensors": {"battery_level_percent": 85.5, "temperature_celsius": -62.3, "obstacle_detected": false}
      }'

# Read it back
curl http://localhost:8000/telemetry
```

---

## 5. Future deployment (Render / Railway)

No code changes are required to deploy — only environment variables and
a start command.

1. Push the `backend/` folder to a Git repository.
2. Create a new **Web Service** on Render (or a new project on Railway)
   pointing at that repo.
3. **Build command:**
   ```
   pip install -r requirements.txt
   ```
4. **Start command:**
   ```
   uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
   Both Render and Railway inject the `PORT` environment variable
   automatically — the app already reads `HOST`/`PORT` from the
   environment via `app/config.py`, so this just works.
5. Set environment variables in the platform's dashboard (mirroring
   `.env.example`), at minimum:
   - `ENVIRONMENT=production`
   - `CORS_ORIGINS_RAW=<your deployed dashboard URL>`
6. Once deployed, share the public URL (e.g.
   `https://your-app.onrender.com`) with Member 1 and Member 2 — they
   simply point their `POST` requests at that URL instead of
   `localhost:8000`. Nothing else changes.

---

## 6. Design notes

- **No database, by design.** The brief calls for in-memory storage only.
  `services/storage.py` isolates this behind a small class with
  `save_*` / `get_latest_*` methods, so a future swap to MongoDB or
  PostgreSQL only requires rewriting that one file.
- **Validation is strict but informative.** Malformed payloads return a
  `422` with a field-by-field error list instead of crashing the server
  or silently accepting bad data.
- **CORS is open by default** (`CORS_ORIGINS_RAW=*`) since teammates are
  on different networks during development. Tighten it via the env var
  before a public deployment.
- **Thread-safe in-memory store**, so concurrent POSTs/GETs from three
  teammates hitting the same shared backend can't corrupt each other's
  data.
- **Swagger docs are generated for free** from the Pydantic models —
  no manual API documentation to keep in sync.
