from .grid import ALL_DIRS, MOVE
from collections import deque

DIR_LETTER = {1: "N", 2: "E", 4: "S", 8: "W"}

def maze_solver(maze, entry_point, exit_point) -> list[str] | None:
    """Return the shortest path from entry to exit as a list of direction
    letters (N/E/S/W). Returns None if unreachable."""
    if entry_point == exit_point:
        return []

    previous = {entry_point: None}
    queue = deque([entry_point])
    while queue:
        x, y = queue.popleft()
        if (x, y) == exit_point:
            break
        for direction in ALL_DIRS:
            if not maze.is_open