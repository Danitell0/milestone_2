#!/usr/bin/env python3

import curses
import random
from curses import panel
from typing import Callable
from .maze_display import (
    COLOR_CHOICES,
    CHAR_THEMES,
    DEFAULT_COLORS,
    DEFAULT_CHARS,
    convert_path_from_letters,
    render)
from maze_generator.generator import generate
from maze_generator.grid import Maze
from maze_generator.solver import maze_solver
from maze_generator.writer import write_maze_file
from configurations.check_parsing import MazeConfig


class Menu(object):
    def __init__(self, title: str,
                 items: list[tuple[str, Callable[[], None]]],
                 stdscreen: curses.window,
                 background: Callable[[curses.window],
                                      None] | None = None) -> None:
        self.title = title
        self.window = stdscreen.subwin(0, 0)
        self.window.keypad(True)
        self.panel = panel.new_panel(self.window)
        self.panel.hide()
        self.background = background
        panel.update_panels()

        self.position = 0
        self.items = list(items)
        self.items.append(("exit", lambda: None))
        #  lambda to satisfy mypy

    def navigate(self, n: int) -> None:
        self.position += n
        if self.position < 0:
            self.position = 0
        elif self.position >= len(self.items):
            self.position = len(self.items) - 1

    def display(self) -> None:
        self.panel.top()
        self.panel.show()
        self.window.clear()

        while True:
            self.window.refresh()
            self.draw_menu()
            curses.doupdate()
            key = self.window.getch()

            if key in [curses.KEY_ENTER, ord('\n')]:
                if self.position == len(self.items) - 1:
                    break
                self.items[self.position][1]()
            elif key == curses.KEY_UP:
                self.navigate(-1)
            elif key == curses.KEY_DOWN:
                self.navigate(1)
        self.window.clear()
        self.panel.hide()
        panel.update_panels()
        curses.doupdate()

    def draw_menu(self) -> None:
        self.window.clear()
        max_y, max_x = self.window.getmaxyx()

        needed_h = 4 + len(self.items)
        longest = max(len(self.title),
                      max(len(item[0]) for item in self.items))
        needed_w = longest + 10

        if max_y < needed_h or max_x < needed_w:
            try:
                self.window.addstr(0, 0,
                                   "Warning: Terminal too small, "
                                   "try to resizing it"[:max_x - 1])
            except curses.error:
                pass
            return

        self.window.addstr(1, (max_x - len(self.title)) // 2,
                           self.title, curses.A_BOLD)
        if self.background:
            self.background(self.window)
        box_width = longest + 10
        left_x = (max_x - box_width) // 2
        right_x = left_x + box_width
        self.window.addstr(0, left_x, "╔" + "═" * (box_width - 2) + "╗")
        for row in range(1, len(self.items) + 3):
            self.window.addstr(row, left_x, "║")
            self.window.addstr(row, right_x - 1, "║")
        self.window.addstr(3 + len(self.items),
                           left_x, "╚" + "═" * (box_width - 2) + "╝")

        for index, item in enumerate(self.items):
            mode = (
                curses.A_REVERSE if index == self.position
                else curses.A_NORMAL)
            msg = "%d. %s" % (index, item[0])
            self.window.addstr(3 + index, (max_x - len(msg)) // 2, msg, mode)


COLOR_MAP = {
    "white": curses.COLOR_WHITE,
    "yellow": curses.COLOR_YELLOW,
    "green": curses.COLOR_GREEN,
    "red": curses.COLOR_RED,
    "magenta": curses.COLOR_MAGENTA,
    "cyan": curses.COLOR_CYAN,
    "blue": curses.COLOR_BLUE,
}


class MazeWindow(object):
    def __init__(self, stdscreen: curses.window, settings: MazeConfig) -> None:
        self.screen = stdscreen
        self.settings = settings
        self.maze: Maze | None = None
        self.letters: list[str] | None = None
        self.seed = (
            settings.seed if settings.seed is not None
            else random.randint(0, 999999999))
        self.show_path = True
        self.colors = dict(DEFAULT_COLORS)
        self.chars = dict(DEFAULT_CHARS)
        self.color_ind = 0
        self.char_ind = 0

        if not curses.has_colors():
            raise SystemExit("This program needs a color-capable terminal. "
                             "Good try dumb terminal!")
        curses.curs_set(0)
        curses.start_color()
        curses.use_default_colors()
        self.pairs: dict[str, int] = {}
        for i, (name, code) in enumerate(COLOR_MAP.items(), start=1):
            curses.init_pair(i, code, -1)
            self.pairs[name] = curses.color_pair(i)

        self.submenu_items = [
            ("Toggle Path", self.toggle_path),
            ("Show Animation", self.animation),
            ("Change Maze Color", self.change_color),
            ("Change Maze Visual", self.change_chars),
            ("Regenerate", self.regenerate)
        ]
        submenu = Menu("A-Maze-ing", self.submenu_items,
                       self.screen, background=self.show_maze)

        def generate_and_enter() -> None:
            self.build_maze(self.settings)
            submenu.display()

        main_menu = Menu("A-Maze-ing", [("Generate Maze", generate_and_enter)],
                         self.screen)
        main_menu.display()

    def build_maze(self, settings: MazeConfig) -> None:
        assert settings.entry_point is not None
        assert settings.exit_point is not None
        assert settings.output_file is not None

        maze, warnings = generate(settings)
        self.maze = maze

        for msg in warnings:
            self.show_warning(f"Warning: {msg}")

        self.letters = maze_solver(maze,
                                   settings.entry_point, settings.exit_point)
        if self.letters is None:
            raise RuntimeError(
                "Internal Error: generated maze has no possible solution."
            )

        write_maze_file(settings.output_file, maze,
                        settings.entry_point,
                        settings.exit_point,
                        self.letters)
        self.show_warning(f"Maze output was written to "
              f"'{settings.output_file}' (seed={settings.seed})")

    def paint(self, win: curses.window,
              rows: list[list[tuple[str, str | None]]],
              top: int = 0) -> None:
        max_y, max_x = win.getmaxyx()
        maze_height = len(rows)
        maze_width = max(
            (sum(len(text) for text, _ in segments) for segments in rows),
            default=0
        )
        off_y = top + ((max_y - top) - maze_height) // 2
        off_x = max((max_x - maze_width) // 2, 0)

        for y, segments in enumerate(rows):
            draw_y = off_y + y
            if draw_y >= max_y - 1:
                break
            x = off_x
            for text, color_name in segments:
                if x >= max_x - 1:
                    break
                attr = self.pairs.get(color_name or "", curses.A_NORMAL)
                try:
                    win.addstr(draw_y, x, text[:max_x - 1 - x], attr)
                except curses.error:
                    pass
                x += len(text)

    def show_maze(self, win: curses.window) -> None:
        assert self.maze is not None
        assert self.letters is not None
        assert self.settings.entry_point is not None
        assert self.settings.exit_point is not None

        pc = convert_path_from_letters(
            self.settings.entry_point,
            self.letters
        ) if self.show_path else None

        rows = render(self.maze, self.settings.entry_point,
                      self.settings.exit_point,
                      path_cells=set(pc) if pc is not None else None,
                      colors=self.colors,
                      chars=self.chars)

        menu_h = 5 + len(self.submenu_items)
        self.paint(win, rows, top=menu_h)

    def toggle_path(self) -> None:
        self.show_path = not self.show_path

    def regenerate(self) -> None:
        self.seed = random.randint(0, 999999999)
        self.build_maze(self.settings)

    def change_color(self) -> None:
        choices = list(COLOR_CHOICES.values())
        self.color_ind = (self.color_ind + 1) % len(choices)
        _, code = choices[self.color_ind]
        self.colors["wall"] = code

    def change_chars(self) -> None:
        themes = list(CHAR_THEMES.values())
        self.char_ind = (self.char_ind + 1) % len(themes)
        self.chars = dict(themes[self.char_ind])

    def animation(self) -> None:
        assert self.maze is not None
        assert self.letters is not None
        assert self.settings.entry_point is not None
        assert self.settings.exit_point is not None

        win = self.screen.subwin(0, 0)
        win.keypad(True)
        win.timeout(80)
        pan = panel.new_panel(win)
        pan.top()
        pan.show()

        ordered = convert_path_from_letters(
            self.settings.entry_point, self.letters
        )

        reveal = 0
        while True:
            win.clear()
            pc = set(ordered[:reveal])
            rows = render(self.maze, self.settings.entry_point,
                          self.settings.exit_point,
                          path_cells=pc, colors=self.colors,
                          chars=self.chars)
            self.paint(win, rows)
            win.refresh()

            key = win.getch()
            if key != -1:
                break
            if reveal < len(ordered):
                reveal += 1

        win.clear()
        pan.hide()
        panel.update_panels()
        curses.doupdate()

    def show_warning(self, message: str) -> None:
            # Maak een pop-up venster in het midden van het scherm
            max_y, max_x = self.screen.getmaxyx()
            
            # Bepaal afmetingen op basis van de tekstlengte
            win_w = max(len(message) + 6, 40)
            win_h = 5
            start_y = (max_y - win_h) // 2
            start_x = (max_x - win_w) // 2

            # Maak een subwindow en zet deze in een panel zodat hij bovenaan ligt
            warn_win = self.screen.subwin(win_h, win_w, start_y, start_x)
            warn_win.keypad(True)
            warn_panel = panel.new_panel(warn_win)
            
            warn_win.clear()
            # Teken een rood kader (we gebruiken de 'red' pair die je al in self.pairs hebt)
            red_attr = self.pairs.get("red", curses.A_NORMAL) | curses.A_BOLD
            warn_win.attron(red_attr)
            warn_win.box()
            
            # Toon de waarschuwingstext
            warn_win.addstr(1, (win_w - 9) // 2, " MESSAGE ", red_attr)
            warn_win.addstr(2, (win_w - len(message)) // 2, message, curses.A_NORMAL)
            
            # Instructie om te sluiten
            prompt = "[ Press a button to continue ]"
            warn_win.addstr(3, (win_w - len(prompt)) // 2, prompt, curses.A_DIM)
            warn_win.attroff(red_attr)

            # Breng panel naar de voorgrond en ververs het scherm
            warn_panel.top()
            warn_panel.show()
            panel.update_panels()
            curses.doupdate()

            # Wacht tot de gebruiker op een toets drukt
            warn_win.getch()

            # Ruim het panel en window weer netjes op
            warn_win.clear()
            warn_panel.hide()
            panel.update_panels()
            curses.doupdate()