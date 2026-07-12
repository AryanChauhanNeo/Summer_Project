# telemetry/telemetry_manager.py
import json
from datetime import datetime, timezone


class TelemetryManager:
    def __init__(self, output_file="telemetry_output.json",
                       log_file="mission_log.jsonl"):
        self.output_file = output_file
        self.log_file    = log_file

        # Clear the log file at the start of each new simulation run
        # This prevents old runs from piling up in mission_log.jsonl
        with open(self.log_file, "w") as f:
            f.write("")

    # ------------------------------------------------------------------
    # PRIMARY METHOD: called once per tick from main.py
    # ------------------------------------------------------------------
    def build_payload(self, rover, sensor_readings, obstacle_ahead):
        """
        Assembles the exact JSON structure from the data contract.
        Every field name here matches what TM3 and TM2 expect.
        """
        # Inject real obstacle value into sensor block
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
    # OUTPUT METHODS
    # ------------------------------------------------------------------
    def print_payload(self, payload):
        def default_serializer(obj):
            if isinstance(obj, bool):
                return bool(obj)
            raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
        print(json.dumps(payload, indent=2, default=default_serializer))

    def save_snapshot(self, payload):
        with open(self.output_file, "w") as f:
            json.dump(payload, f, indent=2, default=str)

    def append_log(self, payload):
        with open(self.log_file, "a") as f:
            f.write(json.dumps(payload, default=str) + "\n")

    def save_all(self, payload):
        """
        Convenience method — call this once per tick from main.py.
        Does snapshot + log append in one call.
        """
        self.save_snapshot(payload)
        self.append_log(payload)


# ------------------------------------------------------------------
# QUICK TEST — run this file directly to verify
# ------------------------------------------------------------------
if __name__ == "__main__":
    import sys
    import os
    # This line makes sure Python finds terrain, rover, sensors as top-level packages
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    from terrain.terrain_generator import MarsTerrainGenerator
    from rover.rover               import Rover
    from sensors.sensor_simulator  import SensorSimulator

    # Setup
    terrain = MarsTerrainGenerator(rows=10, cols=10, obstacle_density=0.10)
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