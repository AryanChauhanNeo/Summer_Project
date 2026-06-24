# sensors/sensor_simulator.py
import random

class SensorSimulator:
    def __init__(self):
        self.battery     = 100.0   # starts fully charged
        self.temperature = -62.0   # realistic Mars average in Celsius

    # ------------------------------------------------------------------
    # PRIMARY METHOD: called once per tick from main.py
    # ------------------------------------------------------------------
    def update(self, rover):
        """
        Updates all sensor readings based on current rover state.
        Returns the complete sensors block for the JSON payload.
        """
        self._update_battery(rover)
        self._update_temperature()
        return self.get_readings(rover)

    # ------------------------------------------------------------------
    # INTERNAL UPDATERS
    # ------------------------------------------------------------------
    def _update_battery(self, rover):
        """
        Battery drains faster when moving, slower when idle.
        Kills rover if battery hits zero.
        Real rovers use solar panels + battery — drain varies by activity.
        """
        if rover.state == "MOVING":
            drain = round(random.uniform(0.25, 0.35), 3)  # ~0.3% per tick
        elif rover.state == "IDLE":
            drain = round(random.uniform(0.03, 0.07), 3)  # ~0.05% per tick
        else:
            drain = 0.0  # ARRIVED or DEAD_BATTERY — no drain

        self.battery = round(max(0.0, self.battery - drain), 2)

        # Kill rover if battery depleted
        if self.battery <= 0.0:
            rover.state = "DEAD_BATTERY"

    def _update_temperature(self):
        """
        Temperature drifts slowly each tick within realistic Mars range.
        Mars surface: -125°C (night) to +20°C (equator midday).
        Our simulation stays in the -80°C to -40°C range — typical mid-latitude.
        """
        drift = round(random.uniform(-0.5, 0.5), 2)
        self.temperature = round(
            max(-80.0, min(-40.0, self.temperature + drift)), 1
        )

    # ------------------------------------------------------------------
    # READINGS: returns exact sensors block matching data contract
    # ------------------------------------------------------------------
    def get_readings(self, rover):
        """
        Returns the sensors block exactly as defined in the data contract.
        obstacle_detected is injected here from rover.is_obstacle_ahead()
        """
        return {
            "battery_level_percent": self.battery,
            "temperature_celsius":   self.temperature,
            "obstacle_detected":     False  # placeholder — main.py injects real value
        }


# ------------------------------------------------------------------
# QUICK TEST — run this file directly to verify
# ------------------------------------------------------------------
if __name__ == "__main__":
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    from terrain.terrain_generator import MarsTerrainGenerator
    from rover.rover import Rover

    # Setup
    terrain = MarsTerrainGenerator(rows=10, cols=10, obstacle_density=0.10)
    _, start, goal = terrain.generate()
    terrain.print_grid()

    rover  = Rover(start, goal)
    sensor = SensorSimulator()

    print(f"{'Tick':<6} {'Battery':>10} {'Temp (°C)':>12} {'State':>14}")
    print("-" * 48)

    for tick in range(1, 20):
        rover.move_towards_goal(terrain)
        readings = sensor.update(rover)

        print(f"{tick:<6} "
              f"{readings['battery_level_percent']:>9}% "
              f"{readings['temperature_celsius']:>11}°C "
              f"{rover.state:>14}")

        if rover.state in ("ARRIVED", "DEAD_BATTERY"):
            break