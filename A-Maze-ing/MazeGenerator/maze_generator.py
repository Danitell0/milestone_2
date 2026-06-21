#!/usr/bin/env python3

import random
from typing import Optional


class MazeGenerator():
    def __init__(self, width: int, height: int,
                 entry_point: tuple[int, int],
                 exit_point: tuple[int, int],
                 seed: Optional[int] = None) -> None:
        if seed is None:
            seed = random.randint()
        self._width = width
        self._height = height
        self._entry = entry_point
        self._exit = exit_point
        self._seed = seed
        random.seed(self._seed)

# ------------testing

def main() -> None:
    random.seed(42)
    print(random.randint(1, 100))
    random.seed(43)
    print(random.randint(1, 100))


if __name__ == "__main__":
    main()
