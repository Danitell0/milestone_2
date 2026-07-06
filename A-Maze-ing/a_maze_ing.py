#!/usr/bin/env python3

import sys
import curses
from configurations.config_checker import config_parsing, validate_config
from MazeGen.maze_generator import MazeGenerator
from UI.menu import MazeWindow


def main() -> None:
    if len(sys.argv) != 2:
        print(f"Missing configuration file: {sys.argv[0]} <file>")
        exit(1)
    try:
        settings = config_parsing(sys.argv[1])
        validate_config(settings)

        entry = settings['ENTRY'].split(',')
        exit_p = settings['EXIT'].split(',')
        maze = MazeGenerator(int(settings['WIDTH']),
                             int(settings['HEIGHT']),
                             (int(entry[0]), int(entry[1])),
                             (int(exit_p[0]), int(exit_p[1])),
                             perfect=(settings['PERFECT'] == 'True'),
                             output_file=settings['OUTPUT_FILE']
                             )
        # from UI.menu import Menu

    except ValueError as e:
        print("Error:", e, file=sys.stderr)
    
    curses.wrapper(MazeWindow, maze)


if __name__ == "__main__":
    main()
