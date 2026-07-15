
import random
from .grid import Maze, ALL_DIRS, MOVE, E, S
from .logo42 import build_logo_cells


class GenerationError(Exception):
    """Raised when maze generation fails."""
    pass


def add_loops(maze: Maze,
              visited: set[tuple[int, int]],
              rand_seed: random.Random,
              target_loops: int) -> int:
    """Open extra internal walls to create loops.

    Args:
        maze: Maze to modify.
        visited: Reachable cells.
        rand_seed: Seeded RNG for reproducibility.
        target_loops: Max number of walls to open.

    Returns:
        Number of walls actually opened.
    """
    candidates = []
    for (x, y) in visited:
        for direction in (E, S):  # only check each internal wall once
            dx, dy = MOVE[direction]
            nx, ny = x + dx, y + dy
            if (nx, ny) in visited and maze.is_wall(x, y, direction):
                candidates.append((x, y, direction))
    rand_seed.shuffle(candidates)

    added = 0
    for x, y, direction in candidates:
        if added >= target_loops:
            break
        if not maze.is_wall(x, y, direction):
            continue
        # if _would_create_open_block(maze, x, y, direction):
        #     continue
        maze.open_wall(x, y, direction)
        added += 1
    return added


def reduce_dead_ends(maze: Maze,
                     visited: set[tuple[int, int]],
                     rand_seed: random.Random,
                     ) -> int:
    """Give each dead-end cell a second opening where possible.

    Args:
        maze: Maze to modify.
        visited: Reachable cells.
        rand_seed: Seeded RNG for reproducibility.

    Returns:
        Number of dead ends that received an extra opening.
    """
    dead_ends = [(x, y) for (x, y) in visited if maze.degree(x, y) == 1]
    rand_seed.shuffle(dead_ends)
    excess = max(0, len(dead_ends))
    fixed = 0
    for (x, y) in dead_ends:
        if fixed >= excess:
            break
        dirs = list(ALL_DIRS)
        rand_seed.shuffle(dirs)
        for direction in dirs:
            dx, dy = MOVE[direction]
            nx, ny = x + dx, y + dy
            if not maze.in_bounds(nx, ny):
                continue
            if (nx, ny) not in visited:
                continue
            if not maze.is_wall(x, y, direction):
                continue
            # if _would_create_open_block(maze, x, y, d):
            #     continue
            maze.open_wall(x, y, direction)
            fixed += 1
            break
    return fixed


def carve_perfect(maze: Maze,
                  start: tuple[int, int],
                  rand_seed: random.Random
                  ) -> set[tuple[int, int]]:
    """Carve a perfect maze using randomized DFS.

    Args:
        maze: Maze to carve into.
        start: Starting cell coordinates.
        rand_seed: Seeded RNG for reproducibility.

    Returns:
        Set of all cells reachable from start.
    """
    visited = {start}
    stack = [start]
    while stack:
        x, y = stack[-1]
        candidates = []  # not blocked, not visited and in bounds
        for direction in ALL_DIRS:
            dx, dy = MOVE[direction]
            nx, ny = x + dx, y + dy
            if not maze.in_bounds(nx, ny):
                continue
            if (nx, ny) in maze.blocked_cells or (nx, ny) in visited:
                continue
            candidates.append((nx, ny, direction))
        if not candidates:
            stack.pop()
            continue
        nx, ny, direction = rand_seed.choice(candidates)
        maze.open_wall(x, y, direction)
        visited.add((nx, ny))
        stack.append((nx, ny))
    return visited  # returns every reachable cell


def generate(width: int,
             height: int,
             entry_point: tuple[int, int],
             exit_point: tuple[int, int],
             perfect: bool = False,
             seed: int | None = None) -> tuple[Maze, list[str]]:
    """Generate a maze from the given settings.

    Args:
        width: Number of columns.
        height: Number of rows.
        entry_point: (x, y) of the entry cell.
        exit_point: (x, y) of the exit cell.
        perfect: If True, leave the maze perfect. If False, add loops and
            reduce dead ends.
        seed: Seed for reproducible generation.

    Returns:
        Tuple of the generated Maze and a list of warning messages.
    """
    warnings: list[str] = []
    rand_seed = random.Random(seed)
    maze = Maze(width, height)

    corners = [(0, 0), (width - 1, 0),
               (0, height - 1),
               (width - 1, height - 1)]
    center = (width // 2, height // 2)
    avoid = set(corners) | {center, entry_point, exit_point}

    pattern_cells = build_logo_cells(width, height, avoid)
    if not pattern_cells:
        warnings.append(
            "Maze size too small to draw the '42' logo: it has been hidden."
        )
    else:
        maze.blocked_cells = pattern_cells

    visited = carve_perfect(maze, entry_point, rand_seed)

    all_cells = {
        (x, y) for y in range(height)
        for x in range(width)} - maze.blocked_cells
    unreached = all_cells - visited
    if unreached:
        # Connect any leftover pockets (can happen if the '42' logo splits
        # the grid into more than one region) by carving a path from each
        # unreached cell towards an already visited neighbour.
        for (x, y) in unreached:
            for direction in ALL_DIRS:
                dx, dy = MOVE[direction]
                nx, ny = x + dx, y + dy
                if (nx, ny) in visited:
                    maze.open_wall(x, y, direction)
                    visited.add((x, y))
                    break

    if not perfect:
        target_loops = max(2, (width * height) // 15)
        add_loops(maze, visited, rand_seed, target_loops)
        reduce_dead_ends(maze, visited, rand_seed)

    return maze, warnings
