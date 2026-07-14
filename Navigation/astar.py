import heapq
import numpy as np

EMPTY = 0
OBSTACLE = 1
START = 2
GOAL = 3

def heuristic(a, b):
    """
    Manhattan Distance
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def get_neighbors(position, terrain):
    """
    Returns all valid neighboring cells.
    0 = free cell
    1 = obstacle
    """

    rows, cols = terrain.shape

    row, col = position

    directions = [
        (-1, 0),  # up
        (1, 0),   # down
        (0, -1),  # left
        (0, 1)    # right
    ]

    neighbors = []

    for dr, dc in directions:

        nr = row + dr
        nc = col + dc

        if (
            0 <= nr < rows
            and 0 <= nc < cols
            and terrain[nr][nc] !=1
        ):
            neighbors.append((nr, nc))

    return neighbors


def reconstruct_path(came_from, current):
    """
    Reconstruct final path.
    """

    path = [current]

    while current in came_from:
        current = came_from[current]
        path.append(current)

    path.reverse()

    return path


def astar(terrain, start, goal):
    """
    A* Pathfinding

    Input:
        terrain -> NumPy grid
        start   -> (row,col)
        goal    -> (row,col)

    Output:
        [
            (row,col),
            (row,col),
            ...
        ]
    """

    open_set = []

    heapq.heappush(
        open_set,
        (0, start)
    )

    came_from = {}

    g_score = {
        start: 0
    }

    f_score = {
        start: heuristic(start, goal)
    }

    visited = set()

    while open_set:

        _, current = heapq.heappop(open_set)

        if current == goal:
            return reconstruct_path(
                came_from,
                current
            )

        if current in visited:
            continue

        visited.add(current)

        for neighbor in get_neighbors(
            current,
            terrain
        ):

            tentative_g = (
                g_score[current] + 1
            )

            if (
                neighbor not in g_score
                or tentative_g < g_score[neighbor]
            ):

                came_from[neighbor] = current

                g_score[neighbor] = tentative_g

                f_score[neighbor] = (
                    tentative_g
                    + heuristic(neighbor, goal)
                )

                heapq.heappush(
                    open_set,
                    (
                        f_score[neighbor],
                        neighbor
                    )
                )

    return None