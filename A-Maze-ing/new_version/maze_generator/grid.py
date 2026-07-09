from typing import Any

"""Core grid / wall representation for A-Maze-ing.

Each cell is stored as a 4-bit value:
    bit 0 (1) = North wall closed
    bit 1 (2) = East  wall closed
    bit 2 (4) = South wall closed
    bit 3 (8) = West  wall closed

1 = wall closed, 0 = wall open.
"""

N, E, S, W = 1, 2, 4, 8

OPPOSITE = {N: S, S: N, E: W, W: E}
MOVE = {N: (0, -1), S: (0, 1), E: (1, 0), W: (-1, 0)}
ALL_DIRS = (N, E, S, W)


class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Start fully walled (bit = 15)
        self.cells = [[15 for _ in range(width)]
                for _ in range(height)]
        self.blocked_cells = set() # 42 pattern

	# Alreay checked in parsing
    # def in_bounds(self, x, y):
    #     return 0 <= x < self.width and 0 <= y < self.height

    def is_wall(self, x, y, direction):
        return bool(self.cells[y][x] & direction)

    def is_open(self, x, y, direction):
        return not self.is_wall(x, y, direction)

    def open_wall(self, x, y, direction) -> None:
        self.cells[y][x] &= ~direction # flips all bit in direction and keeps the unchanged
        nx, ny = x + MOVE[direction][0], y + MOVE[direction][1]
        if self.in_bounds(nx, ny):
            self.cells[ny][nx] &= ~OPPOSITE[direction]

    def close_wall(self, x, y, direction) -> None:
        self.cells[y][x] |= direction # flips the only different bit
        nx, ny = x + MOVE[direction][0], y + MOVE[direction][1]
        if self.in_bounds(nx, ny):
            self.cells[ny][nx] |= OPPOSITE[direction]

    def neighbor(self, x, y, direction) -> Any | None:
        nx, ny = x + MOVE[direction][0], y + MOVE[direction][1]
        if self.in_bounds(nx, ny):
            return nx, ny
        return None

    def open_neighbors(self, x, y) -> list[Any]:
        """Cells reachable directly from (x, y) through an open wall."""
        result = []
        for direction in ALL_DIRS:
            if self.is_open(x, y, direction):
                n = self.neighbor(x, y, direction)
                if n is not None:
                    result.append(n)
        return result

    def degree(self, x, y) -> int:
        return sum(1 for direction in ALL_DIRS if self.is_open(x, y, direction))

    def to_lines(self) -> list[str]:
        """Return the hexadecimal representation, one string per row."""
        lines = []
        for y in range(self.height):
            lines.append("".join(format(self.cells[y][x], "x") for x in range(self.width)))
        return lines
