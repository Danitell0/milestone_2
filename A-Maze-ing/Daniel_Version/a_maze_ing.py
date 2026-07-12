#!/usr/bin/env python3
import sys
import curses
from display.window import MazeWindow
from configurations.check_parsing import MazeConfig, ConfigError

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

    curses.wrapper(lambda stdscr: MazeWindow(stdscr, settings))

if __name__ == "__main__":
    main()
