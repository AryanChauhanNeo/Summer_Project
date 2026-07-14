import requests
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

    def get_obstacles(self, terrain):
        """
        Extract all obstacle coordinates from the terrain.
        Obstacle cells have value 1.
        """

        obstacles = []

        rows, cols = terrain.shape

        for r in range(rows):
            for c in range(cols):

                if terrain[r][c] == 1:
                    obstacles.append([r, c])

        return obstacles
    
    def get_heading(self):
        """
        Returns the compass heading based on the
        first movement in the current path.
        """

        if self.current_path is None or len(self.current_path) < 2:
            return "N"

        r1, c1 = self.current_path[0]
        r2, c2 = self.current_path[1]

        dr = r2 - r1
        dc = c2 - c1

        directions = {
            (-1, 0): "N",
            (-1, 1): "NE",
            (0, 1): "E",
            (1, 1): "SE",
            (1, 0): "S",
            (1, -1): "SW",
            (0, -1): "W",
            (-1, -1): "NW"
        }

        return directions.get((dr, dc), "UNKNOWN")
    


    def build_payload(self, terrain):
        """
        Build the JSON payload expected by the FastAPI backend.
        """

        if self.current_path is None:
            raise ValueError("Generate a path first.")

        payload = {

            "route": [list(cell) for cell in self.current_path],

            "obstacles": self.get_obstacles(terrain),

            "distance_remaining": len(self.current_path) - 1,

            "heading": self.get_heading(),

            "estimated_time_sec": len(self.current_path) - 1
        }

        return payload
    
    
    def send_navigation(self, terrain):

        payload = self.build_payload(terrain)

        response = requests.post(
            "http://127.0.0.1:8000/navigation",
            json=payload
        )

        if response.status_code == 201:
            print("Navigation data sent successfully.")
        else:
            print("Failed to send navigation data.")
            print(response.status_code)
            print(response.text)