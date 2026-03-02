import random

class SpawnManager:

    def __init__(self, width, height, size):
        self.width = width
        self.height = height
        self.size = size

    def spawn_food(self, snake_body, obstacles, count=1):
        positions = []
        cols = self.width // self.size
        rows = self.height // self.size

        while len(positions) < count:
            x = random.randint(1, cols - 2) * self.size
            y = random.randint(1, rows - 2) * self.size
            pos = (x, y)

            if pos not in snake_body and pos not in obstacles and pos not in positions:
                positions.append(pos)

        return positions

    def spawn_obstacles(self, count=10):
        obstacles = []
        cols = self.width // self.size
        rows = self.height // self.size

        while len(obstacles) < count:
            x = random.randint(1, cols - 2) * self.size
            y = random.randint(1, rows - 2) * self.size
            pos = (x, y)

            if pos not in obstacles:
                obstacles.append(pos)

        return obstacles