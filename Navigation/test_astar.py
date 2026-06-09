import numpy as np

from astar import astar


def visualize_grid(terrain, path, start, destination):

    rows, cols = terrain.shape

    display = []

    for r in range(rows):

        current_row = []

        for c in range(cols):

            if terrain[r][c] == 1:
                current_row.append("X")
            else:
                current_row.append(".")

        display.append(current_row)

    if path:

        for r, c in path:

            if (r, c) != start and (r, c) != destination:
                display[r][c] = "*"

    sr, sc = start
    dr, dc = destination

    display[sr][sc] = "S"
    display[dr][dc] = "D"

    print("\nTerrain Visualization:\n")

    for row in display:
        print(" ".join(row))


# ==========================
# TEST GRID
# ==========================

terrain = np.array([
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 1, 0],
    [1, 1, 0, 0, 0],
    [0, 0, 0, 1, 0]
])

start = (0, 0)

destination = (4, 4)

# ==========================
# RUN A*
# ==========================

path = astar(
    terrain,
    start,
    destination
)

print("Path Found:\n")

print(path)

visualize_grid(
    terrain,
    path,
    start,
    destination
)