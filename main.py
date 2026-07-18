# main.py

import requests
import json
import numpy as np

import sys
import os
import time

# ── Backend configuration ──────────────────────────────────────────
# Change this if backend runs on a different port
BACKEND_URL = "https://mars-rover-backend.onrender.com"

# Ensure all modules are findable from project root
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from terrain.terrain_generator  import MarsTerrainGenerator
from rover.rover                import Rover
from sensors.sensor_simulator   import SensorSimulator
from telemetry.telemetry_manager import TelemetryManager


def post_terrain_to_backend(terrain, start, goal, backend_url=BACKEND_URL):
    """
    Sends terrain grid to backend ONCE at simulation start.
    TM2 calls GET /terrain once to cache it locally.
    Never called again during simulation.
    """
    try:
        terrain_payload = {
            "grid":  terrain.grid.tolist(),
            "rows":  terrain.rows,
            "cols":  terrain.cols,
            "start": list(start),
            "goal":  list(goal)
        }
        response = requests.post(
            f"{backend_url}/terrain",
            json=terrain_payload,
            timeout=30
        )
        if response.status_code in (200, 201):
            print("[Backend] ✅ Terrain posted successfully.")
        else:
            print(f"[Backend] ⚠️ POST /terrain returned {response.status_code}")

    except requests.exceptions.ConnectionError:
        print("[Backend] ⚠️ Could not post terrain — backend not running.")
    except requests.exceptions.Timeout:
        print("[Backend] ⚠️ POST /terrain timed out.")
    except Exception as e:
        print(f"[Backend] ⚠️ Unexpected error posting terrain — {e}")


def run_simulation(ticks=50, delay=1.0):
    print("=" * 50)
    print("   MARS ROVER SIMULATION — STARTING")
    print("=" * 50)

    # ------------------------------------------------------------------
    # SETUP — initialise all modules
    # ------------------------------------------------------------------
    terrain  = MarsTerrainGenerator(rows=15, cols=15, obstacle_density=0.12)
    grid, start, goal = terrain.generate()
    terrain.print_grid()

    rover     = Rover(start, goal)
    sensor    = SensorSimulator()
    telemetry = TelemetryManager(
        output_file="telemetry_output.json",
        log_file="mission_log.jsonl"
    )
    telemetry.backend_url = BACKEND_URL  # inject configurable URL
    post_terrain_to_backend(terrain, start, goal)

    print(f"Rover initialised at {start} → destination {goal}\n")

    # ------------------------------------------------------------------
    # SIMULATION LOOP — one iteration = one tick
    # ------------------------------------------------------------------
    for tick in range(1, ticks + 1):
        print(f"\n{'─' * 50}")
        print(f"  TICK {tick}")
        print(f"{'─' * 50}")

        # Step 1: Move rover one cell toward goal
        rover.move_towards_goal(terrain)

        # Step 2: Read sensors AFTER movement
        obstacle_ahead  = rover.is_obstacle_ahead(terrain)
        sensor_readings = sensor.update(rover)

        # Step 3: Build and save telemetry payload
        payload = telemetry.build_payload(rover, sensor_readings, obstacle_ahead)
        telemetry.print_payload(payload)
        telemetry.save_all(payload)   # writes telemetry_output.json + mission_log.jsonl

        # Step 4: Check stop conditions
        if rover.state == "ARRIVED":
            print("\n✅ Mission complete — Rover reached destination!")
            _save_final_status("ARRIVED", tick)
            break

        if rover.state == "DEAD_BATTERY":
            print("\n❌ Mission failed — Battery depleted!")
            _save_final_status("DEAD_BATTERY", tick)
            break

        # Step 5: Wait before next tick
        time.sleep(delay)

    else:
        # Loop completed all ticks without arriving — mission timed out
        print(f"\n⚠️ Mission timed out after {ticks} ticks.")
        _save_final_status("TIMEOUT", ticks)

    print("\n📁 Telemetry saved to: telemetry_output.json")
    print("📋 Mission log saved to: mission_log.jsonl")
    print("=" * 50)


def _save_final_status(outcome, final_tick):
    """Writes a simple mission summary to mission_summary.txt"""
    with open("mission_summary.txt", "w") as f:
        f.write(f"Mission Outcome : {outcome}\n")
        f.write(f"Total Ticks     : {final_tick}\n")
    print(f"\n📊 Mission summary saved to: mission_summary.txt")


# ------------------------------------------------------------------
# ENTRY POINT
# ------------------------------------------------------------------
if __name__ == "__main__":
    run_simulation(ticks=100, delay=0.5)