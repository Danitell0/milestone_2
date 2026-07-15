import random

from.grid import Maze
from.generator import generate
from .solver import maze_solver


class MazeGenerator:
    """Generates a maze and solves it.

    Create an instance with the maze parameters, call ``generate()``, then
    read the results from ``maze`` and ``solution``.

    Attributes:
        width: Number of columns in the grid.
        height: Number of rows in the grid.
        entry: (x, y) of the entry cell.
        exit: (x, y) of the exit cell.
        perfect: If True, exactly one path exists between any two cells. If
            False, extra loops are added and dead ends reduced.
        seed: The seed used for the current maze. Always an int after
            construction, so a generated maze is always reproducible.
        maze: The generated Maze, or None before `generate()` is called.
        solution: The shortest path from entry to exit as a list of "N"/"E"/
            "S"/"W" letters, or None before `generate()` is called.
        warnings: Non-fatal messages from the last generation (e.g. the maze
            was too small to fit the '42' logo).
    """

    def __init__(self,
                 width: int,
                 height: int,
                 entry_point: tuple[int, int],
                 exit_point: tuple[int, int],
                 perfect: bool = False,
                 seed: int | None = None) -> None:
        """Set up a generator. Call ``generate()``.

        Args:
            width: Number of columns. Must be positive.
            height: Number of rows. Must be positive.
            entry: (x, y) of the entry cell, inside the grid.
            exit: (x, y) of the exit cell, inside the grid and different
                from `entry`.
            perfect: If True, generate a perfect maze (exactly one path
                between any two cells). If False (default), add loops and
                reduce dead ends.
            seed: Seed for reproducible generation. If None, a random seed is
                chosen and stored, so the result is still reproducible via
                the `seed` attribute.

        Raises:
            ValueError: If the dimensions are not positive, a point is out of
                bounds, or entry and exit are the same cell.
        """
        if width <= 0 or height <= 0:
            raise ValueError("width and height must be positive")
        for name, point in (("entry", entry_point), ("exit", exit_point)):
            if not (0 <= point[0] < width and 0 <= point[1] < height):
                raise ValueError(f"{name} {point} is outside the maze")
        if entry_point == exit_point:
            raise ValueError("entry and exit must be different cells")
        
        self.width = width
        self.height = height
        self.entry_point = entry_point
        self.exit_point = exit_point
        self.perfect = perfect
        self.seed = seed if seed is not None else random.randint(0, 999999999)

        self.maze: Maze | None = None
        self.solution: list[str] | None = None
        self.warnings: list[str] = []

    def generate(self) -> None:
        """Generate the maze and solve it, storing both on the instance.

        Populates ``maze``, ``solution`` and ``warnings``.

        Raises:
            RuntimeError: If the generated maze has no solution
        """
        maze, warnings = generate(
            width=self.width,
            height=self.height,
            entry_point=self.entry_point,
            exit_point=self.exit_point,
            perfect=self.perfect,
            seed=self.seed
        )
        self.maze = maze
        self.warnings = warnings

        solution = maze_solver(maze, self.entry_point, self.exit_point)
        if solution is None:
            raise RuntimeError(
                "generated maze has no solution (internal error)"
            )
        self.solution = solution
    
    def regenerate(self, seed: int | None = None) -> None:
        """Rebuild the maze, optionally with a new seed.

        Args:
            seed: Seed to use. If None generated a random seed
        """
        self.seed = seed if seed is not None else random.randint(0, 999999999)
        self.generate()
