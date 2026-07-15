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
    """A grid-based maze where walls are represented by 4-bit cell values.

    Attributes:
        width (int): The total number of columns in the maze grid.
        height (int): The total number of rows in the maze grid.
        cells (list[list[int]]): A 2D grid storing the 4-bit integer state
            of each cell's walls.
        blocked_cells (set[tuple[int, int]]): A set of (x, y) coordinates
            reserved for custom structural patterns (e.g., a '42' logo).
    """
    def __init__(self, width: int, height: int) -> None:
        """Initializes a Maze instance with all walls closed.

        Args:
            width (int): The width of the maze in cells.
            height (int): The height of the maze in cells.

        Returns:
            None.
        """
        self.width = width
        self.height = height
        # Start fully walled (bit = 15)
        self.cells = [[15 for _ in range(width)]
                      for _ in range(height)]
        self.blocked_cells: set[tuple[int, int]] = set()  # 42 pattern

    def in_bounds(self, x: int, y: int) -> bool:
        """Checks if the given coordinates are within the maze grid boundaries.

        Args:
            x (int): The horizontal column index.
            y (int): The vertical row index.

        Returns:
            bool: True if the coordinates are in bounds, False otherwise.
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def is_wall(self, x: int, y: int, direction: int) -> bool:
        """Determines if a wall exists in a specific direction
        at the given cell.

        Args:
            x (int): The horizontal column index.
            y (int): The vertical row index.
            direction (int): The directional bit mask (N, E, S, or W).

        Returns:
            bool: True if the wall is closed, False if it is open.
        """
        return bool(self.cells[y][x] & direction)

    def is_open(self, x: int, y: int, direction: int) -> bool:
        """Determines if a passage is open in a specific
        direction at the given cell.

        Args:
            x (int): The horizontal column index.
            y (int): The vertical row index.
            direction (int): The directional bit mask (N, E, S, or W).

        Returns:
            bool: True if the wall is open, False if it is closed.
        """
        return not self.is_wall(x, y, direction)

    def open_wall(self, x: int, y: int, direction: int) -> None:
        """Opens a wall at a specific cell and syncs the
        neighboring cell's wall.

        Args:
            x (int): The horizontal column index.
            y (int): The vertical row index.
            direction (int): The directional bit mask to open.
        """
        # flips all bit in direction and keeps the unchanged
        self.cells[y][x] &= ~direction
        nx, ny = x + MOVE[direction][0], y + MOVE[direction][1]
        if self.in_bounds(nx, ny):
            self.cells[ny][nx] &= ~OPPOSITE[direction]

    def close_wall(self, x: int, y: int, direction: int) -> None:
        """Closes a wall at a specific cell and syncs the
        neighboring cell's wall.

        Args:
            x (int): The horizontal column index.
            y (int): The vertical row index.
            direction (int): The directional bit mask to close.
        """
        self.cells[y][x] |= direction  # flips the only different bit
        nx, ny = x + MOVE[direction][0], y + MOVE[direction][1]
        if self.in_bounds(nx, ny):
            self.cells[ny][nx] |= OPPOSITE[direction]

    def neighbor(self, x: int, y: int, direction: int) -> Any | None:
        """Calculates the adjacent coordinates in a given direction
        if in bounds.

        Args:
            x (int): The horizontal column index.
            y (int): The vertical row index.
            direction (int): The directional bit mask to look toward.

        Returns:
            tuple[int, int] | None: A tuple of (x, y) coordinates of
            the neighbor, if it exists within bounds, otherwise None.
        """
        nx, ny = x + MOVE[direction][0], y + MOVE[direction][1]
        if self.in_bounds(nx, ny):
            return nx, ny
        return None

    def open_neighbors(self, x: int, y: int) -> list[Any]:
        """Finds all adjacent cells directly accessible via open walls.

        Args:
            x (int): The horizontal column index.
            y (int): The vertical row index.

        Returns:
            list[tuple[int, int]]: A list of (x, y) coordinate
            tuples representing reachable neighboring cells.
        """
        result = []
        for direction in ALL_DIRS:
            if self.is_open(x, y, direction):
                n = self.neighbor(x, y, direction)
                if n is not None:
                    result.append(n)
        return result

    # number of open walls. degree == 1 means a dead end
    def degree(self, x: int, y: int) -> int:
        """Calculates the total number of open directions
        surrounding a single cell.

        Args:
            x (int): The horizontal column index.
            y (int): The vertical row index.

        Returns:
            int: The total count of open paths out of the cell
            (1 indicates a dead end).
        """
        return sum(1 for direction in ALL_DIRS
                   if self.is_open(x, y, direction))

    def to_lines(self) -> list[str]:
        """Converts each row of the maze cells into a hexadecimal string.

        Returns:
            list[str]: A list of hex string rows representing
            the complete maze structure.
        """
        lines = []
        for y in range(self.height):
            lines.append("".join(format(self.cells[y][x],
                                        "x") for x in range(self.width)))
        return lines
