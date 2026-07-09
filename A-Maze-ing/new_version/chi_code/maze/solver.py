"""Shortest-path solver."""
from collections import deque

from .grid import ALL_DIRS, DELTA

DIR_LETTER = {1: "N", 2: "E", 4: "S", 8: "W"}


def shortest_path(maze, entry, exit_):
    """Return the shortest path from entry to exit as a list of direction
    letters (N/E/S/W). Returns None if unreachable."""
    if entry == exit_:
        return []

    prev = {entry: None}
    queue = deque([entry]) # A deque stands for Double-Ended Queue. It is a type of data structure that allows to add and remove elements from both ends efficiently.
    while queue:
        x, y = queue.popleft()
        if (x, y) == exit_:
            break
        for d in ALL_DIRS:
            if not maze.is_open(x, y, d):
                continue
            dx, dy = DELTA[d]
            nx, ny = x + dx, y + dy
            if not maze.in_bounds(nx, ny):
                continue
            if (nx, ny) in prev:
                continue
            prev[(nx, ny)] = (x, y, d)
            queue.append((nx, ny))

    if exit_ not in prev:
        return None

    letters = []
    cur = exit_
    while prev[cur] is not None:
        px, py, d = prev[cur]
        letters.append(DIR_LETTER[d])
        cur = (px, py)
    letters.reverse()
    return letters
