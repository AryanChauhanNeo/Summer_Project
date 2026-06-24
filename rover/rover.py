# rover/rover.py

class Rover:
    def __init__(self, start_pos, goal_pos):
        self.position = list(start_pos)   # [row, col] → maps to current_position in JSON
        self.goal     = list(goal_pos)    # [row, col] → maps to destination in JSON
        self.state    = "IDLE"            # starts idle, changes once movement begins
        self.speed    = 0.0               # km/h — 0 when idle or stuck
        self._path    = None              # reserved for TM2's A* path (Week 3)

    # ------------------------------------------------------------------
    # PRIMARY METHOD: called once per simulation tick from main.py
    # ------------------------------------------------------------------
    def move_towards_goal(self, terrain):
        """
        Moves the rover one cell closer to goal each tick.
        Uses greedy movement now — TM2 will replace this with A* in Week 3
        by setting self._path before this method is called.
        """
        # Don't move if simulation is already over
        if self.state in ("ARRIVED", "DEAD_BATTERY"):
            self.speed = 0.0
            return

        # --- If TM2 has provided an A* path, follow it ---
        if self._path and len(self._path) > 0:
            next_cell     = self._path.pop(0)
            self.position = list(next_cell)
            self.state    = "MOVING"
            self.speed    = self._calculate_speed()
            self._check_arrival()
            return

        # --- Default: greedy movement ---
        next_cell = self._greedy_next_cell(terrain)

        if next_cell is None:
            self.speed = 0.0
            return

        self.position = list(next_cell)
        self.state    = "MOVING"
        self.speed    = self._calculate_speed()
        self._check_arrival()

    # ------------------------------------------------------------------
    # SENSOR SUPPORT: used by sensor_simulator.py for obstacle_detected
    # ------------------------------------------------------------------
    def is_obstacle_ahead(self, terrain):
        """
        Checks only the immediate next cell in the rover's direction of travel.
        Returns True if blocked, False if clear.
        """
        next_cell = self._greedy_next_cell(terrain, peek_only=True)
        if next_cell is None:
            return False
        return terrain.is_obstacle(next_cell[0], next_cell[1])

    # ------------------------------------------------------------------
    # TM2 INTEGRATION HOOK: Team Member 2 calls this to inject A* path
    # ------------------------------------------------------------------
    def set_path(self, path):
        """
        TM2 calls this in Week 3 to hand over their A* computed path.
        path = list of (row, col) tuples leading to the goal.
        """
        self._path = list(path)

    # ------------------------------------------------------------------
    # INTERNAL HELPERS
    # ------------------------------------------------------------------
    def _greedy_next_cell(self, terrain, peek_only=False):
        """
        Tries to move one step closer to goal.
        Tries row axis first, then column axis as fallback.
        Returns next (row, col) or None if stuck/arrived.
        """
        r,  c  = self.position
        gr, gc = self.goal

        # Determine preferred direction
        if   r < gr: primary = (r + 1, c)
        elif r > gr: primary = (r - 1, c)
        elif c < gc: primary = (r, c + 1)
        elif c > gc: primary = (r, c - 1)
        else:
            return None  # already at goal

        # Try primary direction
        if not terrain.is_obstacle(primary[0], primary[1]):
            return primary

        # Primary blocked — try column axis as fallback
        if   c < gc: fallback = (r, c + 1)
        elif c > gc: fallback = (r, c - 1)
        else:
            return None

        if not terrain.is_obstacle(fallback[0], fallback[1]):
            return fallback

        return None  # both directions blocked this tick

    def _calculate_speed(self):
        """
        Produces a realistic speed value that varies slightly each step.
        Range: 1.5 to 2.5 km/h
        """
        r, c = self.position
        variation = (hash((r, c)) % 11) * 0.1
        return round(1.5 + variation, 1)

    def _check_arrival(self):
        """Marks rover as ARRIVED if it has reached the goal."""
        if self.position == self.goal:
            self.state = "ARRIVED"
            self.speed = 0.0

    def __repr__(self):
        return (f"Rover(pos={self.position}, goal={self.goal}, "
                f"state={self.state}, speed={self.speed})")


# ------------------------------------------------------------------
# QUICK TEST — run this file directly to verify
# ------------------------------------------------------------------
if __name__ == "__main__":
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    from terrain.terrain_generator import MarsTerrainGenerator

    terrain = MarsTerrainGenerator(rows=10, cols=10, obstacle_density=0.10)
    _, start, goal = terrain.generate()
    terrain.print_grid()

    rover = Rover(start, goal)
    print(f"Starting: {rover}\n")

    for step in range(1, 31):
        rover.move_towards_goal(terrain)
        obs = rover.is_obstacle_ahead(terrain)
        print(f"Tick {step:02d} | pos={rover.position} | "
              f"state={rover.state} | speed={rover.speed} | "
              f"obstacle_ahead={obs}")

        if rover.state in ("ARRIVED", "DEAD_BATTERY"):
            break