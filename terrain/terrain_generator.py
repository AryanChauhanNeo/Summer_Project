# terrain/terrain_generator.py
import numpy as np
import random

EMPTY    = 0
OBSTACLE = 1
START    = 2
GOAL     = 3

class MarsTerrainGenerator:
    def __init__(self, rows=20, cols=20, obstacle_density=0.15):
        self.rows = rows
        self.cols = cols
        self.obstacle_density = obstacle_density
        self.grid = None
        self.start = None
        self.goal = None

    def generate(self):
        self.grid = np.zeros((self.rows, self.cols), dtype=int)

        # Scatter obstacles randomly
        for r in range(self.rows):
            for c in range(self.cols):
                if random.random() < self.obstacle_density:
                    self.grid[r][c] = OBSTACLE

        # Pick guaranteed-empty start and goal
        self.start = self._random_empty_cell()
        self.goal  = self._random_empty_cell(exclude=self.start)

        self.grid[self.start[0]][self.start[1]] = START
        self.grid[self.goal[0]][self.goal[1]]   = GOAL

        return self.grid, self.start, self.goal

    def _random_empty_cell(self, exclude=None):
        while True:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)
            if self.grid[r][c] == EMPTY:
                if exclude is None or (r, c) != tuple(exclude):
                    return (r, c)

    def is_obstacle(self, r, c):
        # Used by rover to check if next cell is blocked
        if 0 <= r < self.rows and 0 <= c < self.cols:
            return self.grid[r][c] == OBSTACLE
        return True  # Out of bounds = treat as obstacle

    def print_grid(self):
        symbols = {EMPTY: ".", OBSTACLE: "#", START: "S", GOAL: "G"}
        print("\n=== Mars Terrain ===")
        for row in self.grid:
            print(" ".join(symbols[cell] for cell in row))
        print(f"\nStart: {self.start}  |  Goal: {self.goal}\n")


if __name__ == "__main__":
    t = MarsTerrainGenerator(rows=15, cols=15)
    grid, start, goal = t.generate()
    t.print_grid()