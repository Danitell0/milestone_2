"""mazegen - a reusable maze generator with a '42' logo."""

from .grid import Maze
from . maze_generator import MazeGenerator

__all__ = ["MazeGenerator", "Maze"]
__version__ = "1.0.0"