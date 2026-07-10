"""Maze generation algorithms."""
import random

from .grid import Maze, N, E, S, W, ALL_DIRS, DELTA, OPPOSITE
from .pattern42 import build_pattern_cells


class GenerationError(Exception):
    pass


def _carve_perfect(maze, start, rng):
    """Randomized DFS (recursive backtracker) restricted to non-blocked cells."""
    visited = {start}
    stack = [start]
    while stack:
        x, y = stack[-1]
        candidates = []
        for d in ALL_DIRS:
            dx, dy = DELTA[d]
            nx, ny = x + dx, y + dy
            if not maze.in_bounds(nx, ny):
                continue
            if (nx, ny) in maze.blocked or (nx, ny) in visited:
                continue
            candidates.append((nx, ny, d))
        if not candidates:
            stack.pop()
            continue
        nx, ny, d = rng.choice(candidates)
        maze.open_wall(x, y, d)
        visited.add((nx, ny))
        stack.append((nx, ny))
    return visited


def _would_create_open_block(maze, x, y, d):
    """Check whether opening wall d at (x, y) would create a >=3x3 fully
    open block (no internal walls at all), which is forbidden."""
    dx, dy = DELTA[d]
    nx, ny = x + dx, y + dy

    def open_between(ax, ay, bx, by):
        if (ax, ay) == (x, y) and (bx, by) == (nx, ny):
            return True
        if (ax, ay) == (nx, ny) and (bx, by) == (x, y):
            return True
        if not (maze.in_bounds(ax, ay) and maze.in_bounds(bx, by)):
            return False
        ddx, ddy = bx - ax, by - ay
        for dd, (vx, vy) in DELTA.items():
            if (vx, vy) == (ddx, ddy):
                return maze.is_open(ax, ay, dd)
        return False

    w, h = maze.width, maze.height
    # Check every 3x3 window that could contain this edge.
    for ox in range(min(x, nx) - 2, min(x, nx) + 1):
        for oy in range(min(y, ny) - 2, min(y, ny) + 1):
            if ox < 0 or oy < 0 or ox + 2 >= w or oy + 2 >= h:
                continue
            block = [(ox + i, oy + j) for j in range(3) for i in range(3)]
            if any(c in maze.blocked for c in block):
                continue
            fully_open = True
            for j in range(3):
                for i in range(2):
                    a = (ox + i, oy + j)
                    b = (ox + i + 1, oy + j)
                    if not open_between(*a, *b):
                        fully_open = False
                        break
                if not fully_open:
                    break
            if fully_open:
                for i in range(3):
                    for j in range(2):
                        a = (ox + i, oy + j)
                        b = (ox + i, oy + j + 1)
                        if not open_between(*a, *b):
                            fully_open = False
                            break
                    if not fully_open:
                        break
            if fully_open:
                return True
    return False


def _add_loops(maze, visited, rng, target_loops):
    """Remove extra internal walls to create loops for the Pac-Man mode."""
    candidates = []
    for (x, y) in visited:
        for d in (E, S):  # only check each internal wall once
            dx, dy = DELTA[d]
            nx, ny = x + dx, y + dy
            if (nx, ny) in visited and maze.is_wall(x, y, d):
                candidates.append((x, y, d))
    rng.shuffle(candidates)

    added = 0
    for x, y, d in candidates:
        if added >= target_loops:
            break
        if not maze.is_wall(x, y, d):
            continue
        if _would_create_open_block(maze, x, y, d):
            continue
        maze.open_wall(x, y, d)
        added += 1
    return added


def _reduce_dead_ends(maze, visited, rng, tolerance):
    dead_ends = [(x, y) for (x, y) in visited if maze.degree(x, y) == 1]
    rng.shuffle(dead_ends)
    excess = max(0, len(dead_ends) - tolerance)
    fixed = 0
    for (x, y) in dead_ends:
        if fixed >= excess:
            break
        dirs = list(ALL_DIRS)
        rng.shuffle(dirs)
        for d in dirs:
            dx, dy = DELTA[d]
            nx, ny = x + dx, y + dy
            if not maze.in_bounds(nx, ny):
                continue
            if (nx, ny) not in visited:
                continue
            if not maze.is_wall(x, y, d):
                continue
            if _would_create_open_block(maze, x, y, d):
                continue
            maze.open_wall(x, y, d)
            fixed += 1
            break
    return fixed


def generate(width, height, entry, exit_, perfect, seed=None):
    """Generate a maze. Returns (Maze, warnings: list[str])."""
    warnings = []
    rng = random.Random(seed)

    maze = Maze(width, height)

    corners = [(0, 0), (width - 1, 0), (0, height - 1), (width - 1, height - 1)]
    center = (width // 2, height // 2)
    avoid = set(corners) | {center, entry, exit_}

    pattern_cells = build_pattern_cells(width, height, avoid)
    if not pattern_cells:
        warnings.append(
            "Maze size too small to draw the '42' pattern: it has been omitted."
        )
    else:
        maze.blocked = pattern_cells

    # start = entry
    # if start in maze.blocked:
    #     # Should not happen since entry is in `avoid`, but stay safe.
    #     start = next(iter(set((x, y) for y in range(height) for x in range(width)) - maze.blocked))

    visited = _carve_perfect(maze, entry, rng)

    all_cells = {(x, y) for y in range(height) for x in range(width)} - maze.blocked
    unreached = all_cells - visited
    if unreached:
        # Connect any leftover pockets (can happen if the '42' pattern splits
        # the grid into more than one region) by carving a path from each
        # unreached cell towards an already visited neighbour.
        for (x, y) in unreached:
            for d in ALL_DIRS:
                dx, dy = DELTA[d]
                nx, ny = x + dx, y + dy
                if (nx, ny) in visited:
                    maze.open_wall(x, y, d)
                    visited.add((x, y))
                    break

    if not perfect:
        target_loops = max(2, (width * height) // 15)
        _add_loops(maze, visited, rng, target_loops)
        tolerance = max(2, (width * height) // 50)
        _reduce_dead_ends(maze, visited, rng, tolerance)

    return maze, warnings
