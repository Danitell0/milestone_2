#!/usr/bin/env python3

import curses
import random
from curses import panel
from typing import Callable
from maze_generator.logo42 import LOGOS
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
from configurations import MazeConfig


class Menu(object):
    """A reusable curses menu with an optional backgroung painter.

    Renders a centered, box-framed list of labeled items that the user
    navigates with arrow keys and selects with Enter.
    The class knows nothing about the maze.

    Attibutes:
        title: Text shown at the top of the menu box
        window: The curses window this menu draws into
        panel: The panel wrapping the window
        background: Optional callback drawn behind the menu each frame
        position: Index of the current item
        items: The (label, callback) pairs, with an "exit" entry appended.
    """
    def __init__(self, title: str,
                 items: list[tuple[str, Callable[[], None]]],
                 stdscreen: curses.window,
                 background: Callable[[curses.window],
                                      None] | None = None) -> None:
        """Build a menu (initially hidden) over the given screen.

        Args:
            title: Text shown at the top of the menu box
            items: The (label, callback) pairs, with an "exit" entry appended.
            stdscreen: The parent window where menu is created on
            background: Optional callback drawn behind the menu each frame
        """
        self.title = title
        # full screen sub-window + panel for this menu
        self.window = stdscreen.subwin(0, 0)
        self.window.keypad(True)
        self.panel = panel.new_panel(self.window)
        self.panel.hide()
        self.background = background
        panel.update_panels()

        self.position = 0
        self.items = list(items)
        # Every menu gets an exit entry. The lambda exists
        # to satisfy the (label, callable) type, keeping mypy happy :)
        self.items.append(("exit", lambda: None))

    def navigate(self, n: int) -> None:
        """Move the selection by ``n``.

        Args:
            n: Offset to add to the current position (negative moves up,
            positive moves down).

        Returns:
            None.
        """
        self.position += n
        # Clamp to [0, last index] so the selection can't run off either end
        if self.position < 0:
            self.position = 0
        elif self.position >= len(self.items):
            self.position = len(self.items) - 1

    def display(self) -> None:
        """Show the menu and run its input loop until the user exists.

        Raises th emenu to the top, then loops: redraw, wait for a key,
        and handle it. Up/Down move the selection. Enter runs the selected
        items' callback or exits he loop with "exit".

        Returns:
            None. Blocks until the user selects "exit".
        """
        self.panel.top()
        self.panel.show()
        self.window.clear()

        while True:
            self.window.refresh()
            self.draw_menu()
            curses.doupdate()
            key = self.window.getch()

            if key in [curses.KEY_ENTER, ord('\n')]:
                # the last item is always "exit"
                if self.position == len(self.items) - 1:
                    break
                # otherwise run the selected item's callback
                self.items[self.position][1]()
            elif key == curses.KEY_UP:
                self.navigate(-1)
            elif key == curses.KEY_DOWN:
                self.navigate(1)
        # hide this menu and repaint whatever was underneath
        self.window.clear()
        self.panel.hide()
        panel.update_panels()
        curses.doupdate()

    def draw_menu(self) -> None:
        """Render the menu box, title, items and any background.

        Clears the window, and if the terminal is too small to fit,
        shows a warning and returns without drawing. Otherwise draws
        the tile, the optional background behind the menu, the box
        border and each item.

        Returns:
            None.
        """
        self.window.clear()
        max_y, max_x = self.window.getmaxyx()

        # space the menu needs
        needed_h = 4 + len(self.items)
        longest = max(len(self.title),
                      max(len(item[0]) for item in self.items))
        needed_w = longest + 10

        # if it won't fit, warn and exit before any positioned draw call
        if max_y < needed_h or max_x < needed_w:
            try:
                self.window.addstr(0, 0,
                                   "Warning: Terminal too small, "
                                   "try to resizing it"[:max_x - 1])
            except curses.error:
                pass
            return

        # centered bold title on the second row
        self.window.addstr(1, (max_x - len(self.title)) // 2,
                           self.title, curses.A_BOLD)
        # draw the background behind the box if provided
        if self.background:
            self.background(self.window)

        box_width = longest + 10
        left_x = (max_x - box_width) // 2
        right_x = left_x + box_width
        # Top border, then the two side walls down each row, then the
        # bottom border, framing the item list
        self.window.addstr(0, left_x, "╔" + "═" * (box_width - 2) + "╗")
        for row in range(1, len(self.items) + 3):
            self.window.addstr(row, left_x, "║")
            self.window.addstr(row, right_x - 1, "║")
        self.window.addstr(3 + len(self.items),
                           left_x, "╚" + "═" * (box_width - 2) + "╝")

        # each item, centered. The selected one is drawn reversed(highlighted)
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
    """Top-level curses application: maze generation with menu.

    Owns the whole terminal UI. Sets up colors, builds the menu and runs
    the main menu loop. The maze is drawn as a background beneath the menu,
    and menu actions let the user toggle the path, animate the solution,
    recolor, re-theme and regenerate the maze.

    Attributes:
        screen: The root curses window
        settings: Parsed run configuration
        maze: The current maze, or None until generated
        letters: The solution as N/S/E/W moves, or None until solved
        seed: Active random seed or from config file
        show_path: Active toggle the path to be drawn over the maze
        colors: Active color-name mapping per maze element
        chars: Active characters mapping per maze element
        color_ind: Index into the color presets for cycling
        char_ind: Index into the character-theme presets for cycling
        pairs: Maps color names to initialized curses color-pair attributes
        submenu_itms: The in_maze menu actions pairs
    """
    def __init__(self, stdscreen: curses.window, settings: MazeConfig) -> None:
        """Set up the UI and run the application.

        Initialize instane stats, verifies the terminal supports color,
        sets up curses color pairs, builds the main and sub menus, and
        enters the main menu loop.

        Args:
            stdscreen: The root curses window
            settings: Parsed configuration for this run

        Raises:
            SystemExit: If the terminal has no color support, so the program
            exits cleanly with a message
        """
        self.screen = stdscreen
        self.settings = settings
        self.maze: Maze | None = None
        self.letters: list[str] | None = None
        # Use the config seed if given, otherwise pick a random one
        self.seed = (
            settings.seed if settings.seed is not None
            else random.randint(0, 999999999))
        self.show_path = True
        # copy the default colors
        self.colors = dict(DEFAULT_COLORS)
        self.chars = dict(DEFAULT_CHARS)
        self.logo_name = "42"
        self.logo_ind = 0
        self.color_ind = 0
        self.char_ind = 0

        # exit the program if the terminal can't support colors
        # (e.g. TERM=dumb)
        if not curses.has_colors():
            raise SystemExit("This program needs a color-capable terminal. "
                             "Good try dumb terminal!")
        # hide the cursor and enable color
        curses.curs_set(0)
        curses.start_color()
        curses.use_default_colors()
        # build one curses color per named color, keyed by name so the
        # renderer can look up an attribute from a color name
        self.pairs: dict[str, int] = {}
        for i, (name, code) in enumerate(COLOR_MAP.items(), start=1):
            curses.init_pair(i, code, -1)
            self.pairs[name] = curses.color_pair(i)

        # the actions available once a maze exists
        self.submenu_items = [
            ("Toggle Path", self.toggle_path),
            ("Show Animation", self.animation),
            ("Change Maze Color", self.change_color),
            ("Change Maze Visual", self.change_chars),
            ("Regenerate", self.regenerate),
            ("Regenerate w/ new logo", self.change_logo)
        ]
        # the submenu draws the maze as its background via show_maze, so the
        # maze and the menu are visible together
        submenu = Menu("A-Maze-ing", self.submenu_items,
                       self.screen, background=self.show_maze)

        # wraps "generate then show the submenu" as tge sugke main menu action
        def generate_and_enter() -> None:
            self.build_maze(self.settings)
            submenu.display()

        # the entry screen: one action that generates and enters the maze
        main_menu = Menu("A-Maze-ing", [("Generate Maze", generate_and_enter)],
                         self.screen)
        main_menu.display()

    def build_maze(self, settings: MazeConfig) -> None:
        """Generate a maze, solve it and write it to the output file.

        Syncs the current seed into the settings, generate the maze,
        surfaces any generation warnings to the user, solves it,
        and writes the result. Stores the maze and it's solution so the
        menu and drawing code can use them.

        Args:
            settings: Parsed configuration for this run. May be updated
                in place if the seed differs.

        Raises:
            RuntimeError: If the generated maze has no solution.

        Return:
            None. Side effects: sets ``self.maze`` and ``self.letters``,
            writes the output file, and may show warning pop-ups.
        """
        # guarantees expected config variables
        assert settings.entry_point is not None
        assert settings.exit_point is not None
        assert settings.output_file is not None

        # changes the seed after the regenerating option in the menu
        if self.seed != settings.seed:
            settings.seed = self.seed
        settings.logo_name = self.logo_name
        maze, warnings = generate(settings)
        self.maze = maze

        # show each generation warning as a pop-up
        for msg in warnings:
            self.show_warning(f"Warning: {msg}")

        # solve the maze with the ordered list of N/S/E/W moves, later used
        # to draw and animate the path
        self.letters = maze_solver(maze,
                                   settings.entry_point, settings.exit_point)
        # a generated maze should always be solvable
        if self.letters is None:
            raise RuntimeError(
                "Internal Error: generated maze has no possible solution."
            )

        # persist the maze to the configured file, then confirm the user
        # with a pop-up
        write_maze_file(settings.output_file, maze,
                        settings.entry_point,
                        settings.exit_point,
                        self.letters)
        self.show_warning(f"Maze output was written to "
                          f"'{settings.output_file}' (seed={settings.seed})")

    def paint(self, win: curses.window,
              rows: list[list[tuple[str, str | None]]],
              top: int = 0) -> None:
        """Draw rendered maze rows into a window.

        Shared drawing helper used by both the menu background ``show_maze``
        and the animation. It centers the maze in the drawable area.

        Args:
            win: The window to draw into.
            rows: The redered maze produced by a list of rows, each a list
                of ``(text, color_name)`` where ``color_name`` may be ``None``
                for no color.
            top: Number of rows reserved at the top before drawing begins.
                Pass the menu height to center the maze
                below it (background use), leave it as 0 to center in
                full window (animation use).

        Returns:
            None. Side effects only: draws into ``win``.
        """
        max_y, max_x = win.getmaxyx()
        maze_height = len(rows)
        # widest row in display columns: sum the length of every segment's
        # text. Used to center horizontally, default=0 guards an empty maze
        maze_width = max(
            (sum(len(text) for text, _ in segments) for segments in rows),
            default=0
        )
        off_y = top + ((max_y - top) - maze_height) // 2
        off_x = max((max_x - maze_width) // 2, 0)

        for y, segments in enumerate(rows):
            draw_y = off_y + y
            # stop if we've run past the bottom edge
            if draw_y >= max_y - 1:
                break
            x = off_x
            for text, color_name in segments:
                # stop this row if we've reached the right edge
                if x >= max_x - 1:
                    break
                # look up the curses color for this segment. segments with
                # no color fall back to normal attributes
                attr = self.pairs.get(color_name or "", curses.A_NORMAL)
                # clip the text so it can't spill past the right edge, then
                # draw. The try block catches the error when writting to the
                # very last cell of a line.
                try:
                    win.addstr(draw_y, x, text[:max_x - 1 - x], attr)
                except curses.error:
                    pass
                x += len(text)

    def show_maze(self, win: curses.window) -> None:
        """Draw the maze as the menu's background.

        This is the background callback passed to the submenu.
        It renders the current maze and draws it into the space below
        the menu. The menu owns the loop and the window.

        Args:
            win: The menu's window to draw the maze into. Passed by
                the menu on each redraw.

        Return:
            None. Side effects only: draws the maze into ``win``.
        """
        # These hold because build_maze() runs before the submenu
        # can ever be reached
        assert self.maze is not None
        assert self.letters is not None
        assert self.settings.entry_point is not None
        assert self.settings.exit_point is not None

        # build the ordered solution path only if the the path display is on
        pc = convert_path_from_letters(
            self.settings.entry_point,
            self.letters
        ) if self.show_path else None

        # turn the ordered path list into a set for render()
        # order doesn't matter so set() is fine
        rows = render(self.maze, self.settings.entry_point,
                      self.settings.exit_point,
                      path_cells=set(pc) if pc is not None else None,
                      colors=self.colors,
                      chars=self.chars)

        # centers the maze in the space below
        menu_h = 5 + len(self.submenu_items)
        self.paint(win, rows, top=menu_h)

    def toggle_path(self) -> None:
        """Toggle whether the solution path is drawn over the maze.

        Flips the ``show_path`` flag.

        Returns:
            None.
        """
        self.show_path = not self.show_path

    def regenerate(self) -> None:
        """Generate a fresh maze using a new random seed.

        Picks a new random seed and rebuilds the maze in place.

        Returns:
            None.
        """
        self.seed = random.randint(0, 999999999)
        self.build_maze(self.settings)

    def change_color(self) -> None:
        """Cycle the wall color to the next preset.

        Advances through the presets in ``COLOR_CHOICES`` and applies
        the new color to the walls.

        Return:
            None.
        """
        # step to the next color, wrapping around with modulo so it never
        # runs off the end of the list
        choices = list(COLOR_CHOICES.values())
        self.color_ind = (self.color_ind + 1) % len(choices)
        # each preset is a (role, color) pair, we only use the color and
        # apply it to the "wall" role
        _, code = choices[self.color_ind]
        self.colors["wall"] = code

    def change_logo(self) -> None:
        """Cycle to the next logo and rebuild the maze around it.

        The logo is stamped into the maze's blocked cells.

        Returns:
            None.
        """
        names = list(LOGOS.keys())
        self.logo_ind = (self.logo_ind + 1) % len(names)
        self.logo_name = names[self.logo_ind]
        self.build_maze(self.settings)

    def change_chars(self) -> None:
        """Cycle the maze character theme to the next preset.

        Advances through the themes in ``CHAR_THEMES`` and swaps in that
        theme's full character set.

        Returns:
            None.
        """
        # step to the next theme, wrapping around with modulo
        themes = list(CHAR_THEMES.values())
        self.char_ind = (self.char_ind + 1) % len(themes)
        # copy the theme dict
        self.chars = dict(themes[self.char_ind])

    def animation(self) -> None:
        """Play an animated reveal of the shortest path over the maze.

        Draws the maze in full screen on a temporary panel and animates
        the soulution path one cell at a time. The animation runs until
        the path is fully revealed or the user presses any key. On exit
        the temporary panel is hidden and control returns to the menu.

        Returns:
            None. Side effects only: draws the screen and, on return,
            restores the previous panel stack.
        """
        # the maze and solution ,ust already exist
        assert self.maze is not None
        assert self.letters is not None
        assert self.settings.entry_point is not None
        assert self.settings.exit_point is not None

        # create a temporary full screen window on top of the menu
        win = self.screen.subwin(0, 0)
        win.keypad(True)
        # create a frame loop so the animation can advance on a timer
        win.timeout(80)
        pan = panel.new_panel(win)
        pan.top()
        pan.show()

        # ordered list of path cells from entry to exit
        # needs to be a list to be in order since we are slicing it
        # below to reveal the path step by step. set() loses order
        ordered = convert_path_from_letters(
            self.settings.entry_point, self.letters
        )

        # number of path cells revealed, grows by one each time.
        reveal = 0
        while True:
            win.clear()
            # only the first reveal cells are shown as path this frame
            pc = set(ordered[:reveal])
            rows = render(self.maze, self.settings.entry_point,
                          self.settings.exit_point,
                          path_cells=pc, colors=self.colors,
                          chars=self.chars)
            self.paint(win, rows)
            win.refresh()

            key = win.getch()
            # getch() returns -1 when the 80ms elapsed with no input
            # any keypress aborts the animation early.
            if key != -1:
                break
            # advance one cell per frame until the whole path is shown
            # once fully revealed the path freezes and waits for input
            if reveal < len(ordered):
                reveal += 1

        # removing this temporary window and repaint the menu.
        win.clear()
        pan.hide()
        panel.update_panels()
        curses.doupdate()

    def show_warning(self, message: str) -> None:
        """Display a centered pop-up warning box and wait for keypress.

        Draws a small red-bordered pop-up window showing ``message``,
        then blocks unstil the user presses any key. After skipping it
        the pop-up is removed and whatever was beneath it is restored.

        Args:
            message: The text to show inside the warning box

        Returns:
            None. Side effects only: draws a panel and consumes one
            keypress.
        """
        max_y, max_x = self.screen.getmaxyx()

        # Box is wide enough for the message plus padding
        win_w = max(len(message) + 6, 40)
        win_h = 5
        start_y = (max_y - win_h) // 2
        start_x = (max_x - win_w) // 2

        # Temporary sub.window + panel for the pop-up,
        # it overlays the current view
        warn_win = self.screen.subwin(win_h, win_w, start_y, start_x)
        warn_win.keypad(True)
        warn_panel = panel.new_panel(warn_win)

        warn_win.clear()

        # turn on red + bold, draw the border and title in that style.
        # attron/attroff must be paired: everything drawns between them
        # inherits the attribute
        red_attr = self.pairs.get("red", curses.A_NORMAL) | curses.A_BOLD
        warn_win.attron(red_attr)
        warn_win.box()

        # centered " MESSAGE " title
        warn_win.addstr(1, (win_w - 9) // 2, " MESSAGE ", red_attr)
        # the message itself, centered, drawn in normal style.
        warn_win.addstr(2,
                        (win_w - len(message)) // 2, message, curses.A_NORMAL)

        # prompting the user to skip the pop-up
        prompt = "[ Press a button to continue ]"
        warn_win.addstr(3, (win_w - len(prompt)) // 2, prompt, curses.A_DIM)
        warn_win.attroff(red_attr)

        # raise the pop-up above everything and render it.
        warn_panel.top()
        warn_panel.show()
        panel.update_panels()
        curses.doupdate()

        # waiting for the keypress
        warn_win.getch()

        # hide the pop-up and repaint what was underneath
        warn_win.clear()
        warn_panel.hide()
        panel.update_panels()
        curses.doupdate()
