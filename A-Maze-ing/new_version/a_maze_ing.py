#!/usr/bin/env python3
import sys
import random
from configurations.check_parsing import MazeConfig, ConfigError
from maze_generator.generator import generate

def build_maze(settings: MazeConfig, seed: int) -> Maze, str:
    maze, warnings = generate(settings)

    for msg in warnings:
        print(f"Warning: {msg}")

def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt",
              file=sys.stderr)
        return

    try:
        settings = MazeConfig()
        settings.validate_parse(sys.argv[1])
    except ConfigError as e:
        print(f"Configuration error: {e}",
              file=sys.stderr)
        return
    
    seed = settings.seed if settings.seed is not None else random.randint(0, 999999999)


if __name__ == "__main__":
    main()
