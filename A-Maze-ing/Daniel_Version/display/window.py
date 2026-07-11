#!/usr/bin/env python3

import curses
import random
from curses import panel
from typing import Callable
from .maze_display import COLOR_CHOICES, DEFAULT_COLORS, convert_path_from_letters, render
from maze_generator.generator import generate
from maze_generator.solver import maze_solver
from maze_generator.writer import write_maze_file
from configurations.check_parsing import MazeConfig


class Menu(object):
	def __init__(self, title: str,
			  items: list[tuple[str, Callable[[], None]]],
			  stdscreen: curses.window):
		self.title = title
		self.window = stdscreen.subwin(0, 0)
		self.window.keypad(True)
		self.panel = panel.new_panel(self.window)
		self.panel.hide()
		panel.update_panels()

		self.position = 0
		self.items = items
		self.items.append(("exit", lambda: None)) #lambda to satisfy mypy

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
	
	def draw_menu(self):
		_, max_x = self.window.getmaxyx()
		self.window.addstr(1,
					 (max_x - len(self.title)) // 2,
					 self.title, curses.A_BOLD)

		longest = max(len(self.title),
					max(len(item[0]) for item in self.items))
		box_width = longest + 10 # 10 for padding
		left_x = (max_x - box_width) // 2
		right_x = left_x + box_width
		self.window.addstr(0, left_x, "╔" + "═" * (box_width - 2) + "╗")
		for row in range(1, len(self.items) + 3):
			self.window.addstr(row, left_x, "║")
			self.window.addstr(row, right_x - 1, "║")
		self.window.addstr(3 + len(self.items),
                           left_x, "╚" + "═" * (box_width - 2) + "╝")

		for index, item in enumerate(self.items):
			mode = curses.A_REVERSE if index == self.position else curses.A_NORMAL
			msg = "%d. %s" % (index, item[0])
			self.window.addstr(3 + index, (max_x - len(msg)) // 2, msg, mode)


class MazeWindow(object):
    def __init__(self, stdscreen: curses.window, settings) -> None:
        self.screen = stdscreen
        self.settings = settings
        self.maze = None
        self.letters: list[str] | None = None
        self.seed = settings.seed if settings.seed is not None else random.randint(0, 999999999)
        self.show_path = True
        self.colors = dict(DEFAULT_COLORS)
        curses.curs_set(0)
		
        submenu_items = [
			("Show Maze", self.show_maze),
			("Toggle Path", self.toggle_path),
			("Change Wall Color", self.change_color),
			("Regenerate", self.regenerate)
        ]
        submenu = Menu("A-Maze-ing", submenu_items, self.screen)

        def generate_and_enter() -> None:
            self.build_maze(self.settings)
            submenu.display()

        main_menu = Menu("A-Maze-ing",
                        [("Generate Maze", generate_and_enter)],
                        self.screen)
        main_menu.display()

    def build_maze(self, settings: MazeConfig):
        self.maze, warnings = generate(settings)

        for msg in warnings:
            print(f"Warning: {msg}")

        self.letters = maze_solver(self.maze, settings.entry_point, settings.exit_point)
        if self.letters is None:
            raise RuntimeError(
                "Internal Error: generated maze has no possible solution."
            )

        write_maze_file(settings.output_file, self.maze,
                        settings.entry_point,
                        settings.exit_point,
                        self.letters)
        print(f"Maze output was written to '{settings.output_file}' (seed={settings.seed})")

    def show_maze(self) -> None:
        pc = convert_path_from_letters(
			self.settings.entry_point,
			self.letters
        ) if self.show_path else None
        text = render(self.maze, self.settings.entry_point,
					  self.settings.exit_point,
					  path_cells=pc, colors=self.colors)

        win = self.screen.subwin(0, 0)
        win.keypad(True)
        pan = panel.new_panel(win)
        pan.top()
        pan.show()
        win.clear()

        for y, line in enumerate(text.splitlines()):
            win.addstr(y, 0, line)
        win.refresh()
        win.getch()

        win.clear()
        pan.hide()
        panel.update_panels()
        curses.doupdate()

    def toggle_path(self) -> None:
        self.show_path = not self.show_path
        self.show_maze()

    def regenerate(self) -> None:
        self.seed = random.randint(0, 999999999)
        self.build_maze(self.settings)
        self.show_maze()

    def change_color(self) -> None:
        pick = random.choice(list(COLOR_CHOICES))
        _, code = COLOR_CHOICES[pick]
        self.colors["wall"] = code
        self.show_maze()
