#!/usr/bin/env python3

import random
from typing import Optional


class MazeGenerator():
    def __init__(self, width: int, height: int,
                 entry_point: tuple[int, int],
                 exit_point: tuple[int, int],
                 seed: Optional[int] = None) -> None:
        if seed is None:
            seed = random.randint(100_000_000, 999_999_999)
        self._width = width
        self._height = height
        self._entry = entry_point
        self._exit = exit_point
        self._seed = seed
        random.seed(self._seed)
        self._maze = [
            [15 for _ in range(self._width)]
            for _ in range(self._height)]


# ------------testing

def main() -> None:
    ...


if __name__ == "__main__":
    main()
