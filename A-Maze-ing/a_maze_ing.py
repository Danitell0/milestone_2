#!/usr/bin/env python3

import sys
import os
import curses
from configurations.config_checker import config_parsing, validate_config
from UI.menu import Menu


class MazeWindow(object):
    def __init__(self, stdscreen):
        self.screen = stdscreen
        curses.curs_set(0)

        submenu_items = [("ASCII Maze", curses.beep), 
                         ("Rendered Maze", curses.flash),
                         ("Special Maze", curses.flash)]
        submenu = Menu(submenu_items, self.screen)

        main_menu_items = [("Generate Maze", submenu.display)]
        main_menu = Menu(main_menu_items, self.screen)
        main_menu.display()


def main() -> None:
    if len(sys.argv) != 2:
        print(f"Missing configuration file: {sys.argv[0]} <file>")
        exit(1)
    try:
        settings = config_parsing(sys.argv[1])
        validate_config(settings)
    except ValueError as e:
        print(e, file=sys.stderr)
    


if __name__ == "__main__":
    try:
        curses.wrapper(MazeWindow)
    except Exception as e:
        print(f"Exiting program: {e}")
