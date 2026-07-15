#!/usr/bin/env python3
import sys
import curses
from display.window import MazeWindow
from configurations.check_parsing import MazeConfig, ConfigError


def main() -> None:
    """Parse the config file and launch the maze application.

    Entry point for the program. Expects the path to a maze
    configuration file. Validates and parses it, then hands
    control to the curses UI.

    Usage errors and configuration errors are reported on stderr
    and cause an early return.

    Returns:
        None. Returns early if the arguments are wrong or the
        config file is invalid
    """
    # exactly one argument expected: the config file path
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt",
              file=sys.stderr)
        return

    # build and populate the config from the file. ConfigError
    # covers all validation failures
    try:
        settings = MazeConfig()
        settings.validate_parse(sys.argv[1])
    except ConfigError as e:
        print(f"Configuration error: {e}",
              file=sys.stderr)
        return

    # sets up the terminal and restores it afterwards
    curses.wrapper(lambda stdscr: MazeWindow(stdscr, settings))


if __name__ == "__main__":
    main()
