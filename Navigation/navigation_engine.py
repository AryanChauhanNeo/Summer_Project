from astar import astar


class NavigationEngine:
    """
    Navigation module for the Mars Rover.
    Generates an optimal path using A*.
    """

    def __init__(self):
        self.current_path = None

    def generate_path(self, terrain, start, goal):

        path = astar(terrain, start, goal)

        if path is None:
            raise ValueError("No valid path found.")

        self.current_path = path

        return path

    def get_current_path(self):
        return self.current_path

    def clear_path(self):
        self.current_path = None