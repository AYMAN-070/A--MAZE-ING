import random
import sys
from collections import deque

WALL_N, WALL_S, WALL_E, WALL_W = 1, 4, 2, 8
OPPOSITE = {WALL_N: WALL_S, WALL_E: WALL_W, WALL_S: WALL_N, WALL_W: WALL_E}
MOVES = {
    WALL_N: (0, -1),
    WALL_E: (1, 0),
    WALL_S: (0, 1),
    WALL_W: (-1, 0)
}
DIR_TO_CHAR = {
    WALL_N: 'N',
    WALL_E: 'E',
    WALL_S: 'S',
    WALL_W: 'W'
}

sys.setrecursionlimit(5000)


class MazeGenerator:
    def __init__(self, height: int, width: int) -> None:
        self.height = height
        self.width = width
        """We create a row of 'width' cells containing 15 /
We repeat this row of 'height' cells once"""
        self.grid = [[15 for _ in range(width)] for _ in range(height)]
        self.visited = set()

    def _pattern_42(self):
        if self.height < 10 or self.width < 10:
            return
        center_x = self.width // 2
        center_y = self.height // 2
        pattern = [
            (-3, -2), (-3, -1), (-3, 0),
            (-2, 0),
            (-1, 0), (-1, 1), (-1, 2),
            (1, -2), (2, -2), (3, -2),
            (3, -1), (3, 0),
            (2, 0), (1, 0),
            (1, 1), (1, 2),
            (2, 2), (3, 2)
        ]
        for dx, dy in pattern:
            nx = center_x + dx
            ny = center_y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                self.visited.add((nx, ny))

    def sculpt(self, cx: int, cy: int) -> None:
        """cx, cy : Current position"""
        self.visited.add((cx, cy))
        direction = [WALL_N, WALL_S, WALL_E, WALL_W]
        random.shuffle(direction)
        for dir_key in direction:
            dx, dy = MOVES[dir_key]
            """Neighbor x, Neighbor y"""
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if (nx, ny) not in self.visited:
                    self.grid[cy][cx] -= dir_key
                    self.grid[ny][nx] -= OPPOSITE[dir_key]
                    self.sculpt(nx, ny)

    def generate(self):
        """Function to launch the entire process"""
        self._pattern_42()
        self.sculpt(0, 0)
        return self.grid

    def solve(self, x_start: int, y_start: int, x_end: int, y_end: int) -> str:
        """Find the shortest path and return a string like "NNEESW.."""
        queue = deque([(x_start, y_start)])
        came_from = {}
        came_from[(x_start, y_start)] = None
        while queue:
            cx, cy = queue.popleft()
            if cx == x_end and cy == y_end:
                break
            for direction, (dx, dy) in MOVES.items():
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if (nx, ny) not in came_from:
                        if (self.grid[cy][cx] & direction) == 0:
                            queue.append((nx, ny))
                            char_dir = DIR_TO_CHAR[direction]
                            came_from[(nx, ny)] = (cx, cy, char_dir)
        path = []
        end = (x_end, y_end)
        if end not in came_from:
            return ""
        while end != (x_start, y_start):
            prev_x, prev_y, direction = came_from[end]
            path.append(direction)
            end = (prev_x, prev_y)
        return "".join(reversed(path))


if __name__ == "__main__":
    gen = MazeGenerator(10, 10)
    maze = gen.generate()
    for row in maze:
        print([f"{cell:02d}" for cell in row])
