#!/usr/bin/env python3

import random
from typing import Optional
from enum import Enum


class MazeGenerator():
    class Direction(Enum):
        NORTH = 1
        EAST = 2
        SOUTH = 4
        WEST = 8

    def __init__(self, width: int, height: int,
                 entry_point: tuple[int, int],
                 exit_point: tuple[int, int],
                 perfect: bool = True, # import from file please
                 output_file: str = "maze.txt", # import from file please
                 seed: Optional[int] = None) -> None:
        if seed is None:
            seed = random.randint(100_000_000, 999_999_999)
        self._width = width
        self._height = height
        self._entry = entry_point
        self._exit = exit_point
        self._perfect = perfect
        self._output_file = output_file
        self._seed = seed
        random.seed(self._seed)
        self._maze = [
            [15 for _ in range(self._width)]
            for _ in range(self._height)]
        
    _OPPOSITE = {
        Direction.NORTH: Direction.SOUTH,
        Direction.SOUTH: Direction.NORTH,
        Direction.EAST: Direction.WEST,
        Direction.WEST: Direction.EAST,
    }
 
    _DELTA = {
        Direction.NORTH: (-1, 0),
        Direction.SOUTH: (1, 0),
        Direction.EAST: (0, 1),
        Direction.WEST: (0, -1),
    }

    def generate(self) -> None:
        """Genereert het doolhof met een recursive backtracker (DFS)."""
        visited = [[False] * self._width for _ in range(self._height)]
 
        # entry_point is (x, y) => (col, row)
        start_col, start_row = self._entry
        visited[start_row][start_col] = True
        stack: list[tuple[int, int]] = [(start_row, start_col)]
 
        while stack:
            row, col = stack[-1]
 
            # Verzamel alle onbezochte buren vanuit de huidige cel
            neighbors = []
            for direction, (d_row, d_col) in self._DELTA.items():
                n_row, n_col = row + d_row, col + d_col
                if (0 <= n_row < self._height
                        and 0 <= n_col < self._width
                        and not visited[n_row][n_col]):
                    neighbors.append((direction, n_row, n_col))
 
            if not neighbors:
                # Doodlopend pad: terug in de stack (backtrack)
                stack.pop()
                continue
 
            # Kies willekeurig een buur en breek de muur ertussen
            direction, n_row, n_col = random.choice(neighbors)
            self._maze[row][col] &= ~direction.value
            self._maze[n_row][n_col] &= ~self._OPPOSITE[direction].value
 
            visited[n_row][n_col] = True
            stack.append((n_row, n_col))
 
        if not self._perfect:
            self._add_loops()
    
    def _add_loops(self, extra_ratio: float = 0.1) -> None:
        """Haalt willekeurig extra muren weg zodat er lussen ontstaan
        (voor een niet-'perfect' doolhof, PERFECT=False)."""
        extra_walls = int(self._width * self._height * extra_ratio)
        for _ in range(extra_walls):
            row = random.randint(0, self._height - 1)
            col = random.randint(0, self._width - 1)
            direction = random.choice(list(self.Direction))
            d_row, d_col = self._DELTA[direction]
            n_row, n_col = row + d_row, col + d_col
            if 0 <= n_row < self._height and 0 <= n_col < self._width:
                self._maze[row][col] &= ~direction.value
                self._maze[n_row][n_col] &= ~self._OPPOSITE[direction].value

    def has_wall(self, row: int, col: int, direction: Direction) -> bool:
        cell_value = self._maze[row][col]
        return bool(cell_value & direction.value)

    def print_maze(self) -> None:
        from .walls import walls
        with open(self._output_file, "w") as file:
            for row in self._maze:
                file.write("".join(walls(cell) for cell in row) +"\n")
