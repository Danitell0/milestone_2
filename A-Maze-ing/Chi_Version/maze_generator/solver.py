from .grid import ALL_DIRS, MOVE
from collections import deque

DIR_LETTER = {1: "N", 2: "E", 4: "S", 8: "W"}

# Algorithm Breadth First Search
def maze_solver(maze, entry_point, exit_point) -> list[str] | None:
    """Return the shortest path from entry to exit as a list of direction
    letters (N/E/S/W). Returns None if unreachable."""
    if entry_point == exit_point:
        return []

    previous: dict[tuple[int, int], tuple[int, int, int] | None] = {entry_point: None}

    # deque works as a line, the first in is the first out
    queue = deque([entry_point])
    while queue:
        # take the oldest cell
        x, y = queue.popleft()
    
        # if found the exit break
        if (x, y) == exit_point:
            break

        for direction in ALL_DIRS:
            # skip a direction if a wall is blocking the way
            if not maze.is_open(x, y, direction):
                continue

            # translation of bit into a coordinate
            direction_x, direction_y = MOVE[direction]
            nx, ny = x + direction_x, y + direction_y

            # guard to stay inside the grid
            if not maze.in_bounds(nx, ny):
                continue

            # continue if path already discovered is shorter
            if (nx, ny) in previous:
                continue

            # save the path
            previous[(nx, ny)] = (x, y, direction)
            queue.append((nx, ny))
    
    # if all explored withou fnding the exit
    if exit_point not in previous:
        return None
    
    # Walk the path from exit to entry collecting the directions
    letters = []
    current = exit_point
    while True:
        unzip = previous[current]
        if unzip is None:
            break
        px, py, direction = unzip
        letters.append(DIR_LETTER[direction])
        current = (px, py)

    # flip the directions so it becames entry to exit
    letters.reverse()
    return letters