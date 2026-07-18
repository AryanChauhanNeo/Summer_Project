# telemetry/telemetry_manager.py
import json
import requests                          # NEW — for HTTP POST to backend
from datetime import datetime, timezone


# ── Backend configuration ──────────────────────────────────────────
# Change this URL if backend runs on a different port or machine
BACKEND_URL = "http://127.0.0.1:8000"


class TelemetryManager:
    def __init__(self, output_file="telemetry_output.json",
                       log_file="mission_log.jsonl"):
        self.output_file  = output_file
        self.log_file     = log_file
        self.backend_url  = BACKEND_URL  # NEW — stored so it can be overridden

        # Clear log file at start of each new simulation run
        with open(self.log_file, "w") as f:
            f.write("")

    # ------------------------------------------------------------------
    # PRIMARY METHOD: called once per tick from main.py — UNCHANGED
    # ------------------------------------------------------------------
    def build_payload(self, rover, sensor_readings, obstacle_ahead):
        """
        Assembles the exact JSON structure from the data contract.
        Every field name here matches what the backend and dashboard expect.
        """
        sensor_readings["obstacle_detected"] = bool(obstacle_ahead)

        payload = {
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "system_status": {
                "state":     rover.state,
                "speed_kmh": rover.speed
            },
            "navigation": {
                "current_position": rover.position,
                "destination":      rover.goal
            },
            "sensors": sensor_readings
        }
        return payload

    # ------------------------------------------------------------------
    # OUTPUT METHODS — file-based (UNCHANGED)
    # ------------------------------------------------------------------
    def save_snapshot(self, payload):
        """Overwrites telemetry_output.json with latest payload every tick."""
        with open(self.output_file, "w") as f:
            json.dump(payload, f, indent=2, default=str)

    def append_log(self, payload):
        """Appends each tick's payload as one line in mission_log.jsonl."""
        with open(self.log_file, "a") as f:
            f.write(json.dumps(payload, default=str) + "\n")

    def print_payload(self, payload):
        """Prints formatted JSON to terminal."""
        def default_serializer(obj):
            if isinstance(obj, bool):
                return bool(obj)
            raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
        print(json.dumps(payload, indent=2, default=default_serializer))

    # ------------------------------------------------------------------
    # NEW — POST telemetry to FastAPI backend
    # ------------------------------------------------------------------
    def post_to_backend(self, payload):
        """
        Sends the telemetry payload to the FastAPI backend via HTTP POST.
        If the backend is unavailable, prints an error and continues —
        simulation never stops because of a network failure.
        """
        try:
            # POST the payload to /telemetry endpoint
            response = requests.post(
                f"{self.backend_url}/telemetry",
                json=payload,
                timeout=2        # don't block simulation for more than 2 seconds
            )

            # Log non-200 responses without crashing
            if response.status_code in (200, 201):
                print(f"[Backend] ✅ Telemetry posted successfully.")
            else:
                print(f"[Backend] ⚠️ POST /telemetry returned {response.status_code}")

        except requests.exceptions.ConnectionError:
            # Backend not running — simulation continues normally
            print("[Backend] Warning: Could not connect to backend. Is it running?")

        except requests.exceptions.Timeout:
            # Backend too slow — simulation continues normally
            print("[Backend] Warning: POST /telemetry timed out.")

        except Exception as e:
            # Any other unexpected error — log and continue
            print(f"[Backend] Warning: Unexpected error — {e}")

    # ------------------------------------------------------------------
    # CONVENIENCE METHOD: called once per tick from main.py
    # ------------------------------------------------------------------
    def save_all(self, payload):
        """
        Does everything in one call:
        1. Save snapshot to telemetry_output.json  (local file — unchanged)
        2. Append to mission_log.jsonl             (local log — unchanged)
        3. POST to FastAPI backend                 (NEW)
        """
        self.save_snapshot(payload)   # local file — unchanged
        self.append_log(payload)      # local log  — unchanged
        self.post_to_backend(payload) # NEW — sends to backend


# ------------------------------------------------------------------
# QUICK TEST — run this file directly to verify
# ------------------------------------------------------------------
if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    from terrain.terrain_generator import MarsTerrainGenerator
    from rover.rover               import Rover
    from sensors.sensor_simulator  import SensorSimulator

    terrain  = MarsTerrainGenerator(rows=10, cols=10, obstacle_density=0.10)
    _, start, goal = terrain.generate()
    terrain.print_grid()

    rover     = Rover(start, goal)
    sensor    = SensorSimulator()
    telemetry = TelemetryManager(
        output_file="telemetry_output.json",
        log_file="mission_log.jsonl"
    )

    print("Running 5 ticks...\n")

    for tick in range(1, 6):
        rover.move_towards_goal(terrain)
        obstacle_ahead  = rover.is_obstacle_ahead(terrain)
        sensor_readings = sensor.update(rover)
        payload         = telemetry.build_payload(rover, sensor_readings, obstacle_ahead)

        print(f"--- Tick {tick} ---")
        telemetry.print_payload(payload)
        telemetry.save_all(payload)

        if rover.state in ("ARRIVED", "DEAD_BATTERY"):
            break

    print("\n✅ Check telemetry_output.json and mission_log.jsonl in your folder.")