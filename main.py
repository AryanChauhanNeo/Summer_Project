# main.py
import sys
import os
import time

# Ensure all modules are findable from project root
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from terrain.terrain_generator  import MarsTerrainGenerator
from rover.rover                import Rover
from sensors.sensor_simulator   import SensorSimulator
from telemetry.telemetry_manager import TelemetryManager


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