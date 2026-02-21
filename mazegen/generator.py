import random
import sys
import time
import os
from collections import deque
from Maze_grid import WALL, EMPTY


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

sys.setrecursionlimit(10000)


class MazeGenerator:
    def __init__(self, height: int, width: int, perfect: bool = True) -> None:
        self.height = height
        self.width = width
        self.perfect = perfect
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

    def _draw_frame(self, c_x: int, c_y: int):
        """Clear the terminal and draw the current generation state (Bonus)"""
        """clear if posix(System linux) else cls (Windows)"""
        os.system('clear' if os.name == 'posix' else 'cls')
        # WALL = "\033[90m██\033[0m"  # Gris foncé
        # EMP = "\033[97m██\033[0m"    # Blanc brillant
        for y in range(self.height):
            top_ligne = ""
            middle_ligne = ""
            for x in range(self.width):
                cell = self.grid[y][x]
                if (cell & 1) != 0:
                    top_ligne += WALL + WALL
                else:
                    top_ligne += WALL + EMPTY
                if x == c_x and y == c_y:
                    centre = "👀"
                elif cell == 15:
                    centre = WALL
                else:
                    centre = EMPTY
                if (cell & 8) != 0:
                    middle_ligne += WALL + centre
                else:
                    middle_ligne += EMPTY + centre
            print(top_ligne)
            print(middle_ligne)
        if c_x == self.width - 1 and c_y == self.height - 1:
            pass
        time.sleep(0.025)

    def sculpt(self, cx: int, cy: int, animate: bool = False) -> None:
        """cx, cy : Current position"""
        self.visited.add((cx, cy))
        if animate is True:
            self._draw_frame(cx, cy)
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
                    self.sculpt(nx, ny, animate)

    def _make_imperfect(self):
        """We scan the grid and randomly remove ~10% of the remaining walls."""
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if self.grid[y][x] == 15:
                    continue
                if random.random() < 0.10:
                    """10% probability of breaking a wall here"""
                    direction = []
                    if x + 1 < self.width - 1 and self.grid[y][x + 1] != 15:
                        direction.append(WALL_E)
                    if y + 1 < self.height - 1 and self.grid[y + 1][x] != 15:
                        direction.append(WALL_S)
                    if not direction:
                        continue
                    wall_to_break = random.choice(direction)
                    if (self.grid[y][x] & wall_to_break) != 0:
                        """if there is a wall, we break it"""
                        if wall_to_break == WALL_E:
                            self.grid[y][x] -= WALL_E
                            self.grid[y][x + 1] -= OPPOSITE[WALL_E]  
                        if wall_to_break == WALL_S:
                            self.grid[y][x] -= WALL_S
                            self.grid[y + 1][x] -= OPPOSITE[WALL_S]

    def generate(self, animate: bool = False) -> list:
        """Function to launch the entire process"""
        self._pattern_42()
        self.sculpt(0, 0, animate)
        if not self.perfect:
            self._make_imperfect()
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

