#!/usr/bin/env python3

import curses
from curses import panel
from typing import Callable

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
		_, max_x = self.window.getmaxyx()
		self.panel.top()
		self.panel.show()
		self.window.clear()

		while True:
			self.window.refresh()
			self.draw_menu()
			curses.doupdate()
			for index, item in enumerate(self.items):
				if index == self.position:
					mode = curses.A_REVERSE
				else:
					mode = curses.A_NORMAL

				msg = "%d. %s" % (index, item[0])
				self.window.addstr(
					3 + index, (max_x - len(msg)) // 2, msg, mode
				)
				key = self.window.getch()

				if key in [curses.KEY_ENTER, ord('\n')]:
					if self.position == len(self.items) - 1:
						break
					else:
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

class MazeWindow(object):
    def __init__(self, stdscreen: curses.window) -> None:
        self.screen = stdscreen
        self.maze = maze
        curses.curs_set(0)

        def menu_to_submenu() -> None:
            self.maze.generate_perfect()
            submenu.display()

        submenu_items = [("ASCII Maze", curses.flash),
                         ("Animated Maze", curses.flash),
                         ("Change Color", curses.flash)]
        submenu = Menu("A-Maze-ing", submenu_items, self.screen)

        main_menu_items = [("Generate Maze", menu_to_submenu)]
        main_menu = Menu("A-Maze-ing", main_menu_items, self.screen)
        main_menu.display()
