from maze_generator.grid import N, S, E, W, MOVE, Maze
from typing import Iterable


DEFAULT_COLORS = {
    "wall": "white",
    "path": "yellow",
    "entry": "green",
    "exit": "red",
    "block": "magenta",
}

DEFAULT_CHARS = {
    "corner":   "🮮",
    "h_wall":   "━━",
    "h_open":   "  ",
    "v_wall":   "┃",
    "v_open":   " ",
    "block":    "🮕🮕",
    "entry":    "EN",
    "exit":     "EX",
    "path":     "..",
    "empty":    "  ",
}

COLOR_CHOICES = {
    "1": ("wall", "white"),
    "2": ("wall", "cyan"),
    "3": ("wall", "blue"),
    "4": ("wall", "green"),
    "5": ("wall", "magenta"),
}

CHAR_THEMES = {
    "box":   DEFAULT_CHARS,
    "ascii": {
        "corner": "+", "h_wall": "--", "h_open": "  ",
        "v_wall": "|", "v_open": " ",
        "block": "##", "entry": "EN", "exit": "EX",
        "path": "..", "empty": "  ",
    },
    "dots": {
        "corner": "·", "h_wall": "··", "h_open": "  ",
        "v_wall": ":", "v_open": " ",
        "block": "▓▓", "entry": "EN", "exit": "EX",
        "path": "**", "empty": "  ",
    },
    "rounded": {
        "corner": "╭", "h_wall": "──", "h_open": "  ",
        "v_wall": "│", "v_open": " ",
        "block": "░░", "entry": "▶▶", "exit": "◀◀",
        "path": "••", "empty": "  ",
    },
    "shade": {
        "corner": "▒", "h_wall": "▒▒", "h_open": "  ",
        "v_wall": "▒", "v_open": " ",
        "block": "█▉", "entry": "▶▶", "exit": "◀◀",
        "path": "░░", "empty": "  ",
    },
}


def render(maze: Maze,
           entry_point: tuple[int, int],
           exit_point: tuple[int, int],
           path_cells: set[tuple[int, int]] | None = None,
           colors: dict[str, str] | None = None,
           chars: dict[str, str] | None = None
           ) -> list[list[tuple[str, str | None]]]:
    """Render a maze into drawable rows of colored text segments.

    Converts the maze grid into a list of rows ready to be drawn cell by cell.

    Args:
        maze: The maze to render
        entry_point: (x, y) of the entry cell
        exit_point: (x, y) of the exit cell
        path_cells: Cells on the solution path
        colors: Color-name mapping per element
        chars: Characters mapping per element

    Returns:
        A list of rows. Each row is a list of ``(text, color_name)``
        segments, where ``color_name`` may be None. Drawing code writes each
        segments' text in the given color.
    """
    # fall back to module defaults when the caller doesn't override
    colors = colors or DEFAULT_COLORS
    chars = chars or DEFAULT_CHARS
    path_cells = path_cells or set()
    w, h = maze.width, maze.height
    wall_color = colors.get("wall")
    lines: list[list[tuple[str, str | None]]] = []

    # one extra row because there are horizontal borders both above and
    # below every cell row
    for row in range(h + 1):
        # horizontal wall row: corner post, then wall/gap, repeating
        corners: list[tuple[str, str | None]] = [(chars["corner"], wall_color)]
        for x in range(w):
            # decide if the horizontal wall above this column is closed.
            if row == 0:
                closed = maze.is_wall(x, 0, N)
            elif row == h:
                closed = maze.is_wall(x, h - 1, S)
            else:
                closed = maze.is_wall(x, row - 1, S)
            corners.append(
                (chars["h_wall"] if closed else chars["h_open"], wall_color))
            corners.append((chars["corner"], wall_color))
        lines.append(corners)

        # cell-content row: only for actual cells, not the bottom border
        if row < h:
            walls: list[tuple[str, str | None]] = []
            # leftmost vertical border of the row
            walls.append(
                (chars["v_wall"] if maze.is_wall(
                    0, row, 8) else chars["h_open"], wall_color))
            for x in range(w):
                cell = (x, row)
                # pick the cell's char + color by priority: blocked, then
                # entry, then exit, then path else empty
                if cell in maze.blocked_cells:
                    content, color = chars["block"], colors.get("block")
                elif cell == entry_point:
                    content, color = chars["entry"], colors.get("entry")
                elif cell == exit_point:
                    content, color = chars["exit"], colors.get("exit")
                elif cell in path_cells:
                    content, color = chars["path"], colors.get("path")
                else:
                    content, color = chars["empty"], None
                walls.append((content, color))
                # vertical wall to the east of this cell
                closed = maze.is_wall(x, row, 2)  # east
                walls.append(
                    (chars["v_wall"] if closed else chars["v_open"],
                     wall_color))
            lines.append(walls)

    return lines


def convert_path_from_letters(entry_point: tuple[int, int],
                              letters: Iterable[str]
                              ) -> list[tuple[int, int]]:
    """Convert a sequence of move letters into the cells they visit.

    Starting from the entry cell, follows each N/S/E/W move in order and
    records every cell stepped into, producing the ordered list of cells
    along the path

    Args:
        entry_point: (x,y) of the starting cell
        letters: Move directions as char in walk oredr.

    Returns:
        The ordered list of (x, y) cells visited, from entry.
    """
    # Start at the entry. Each move appends the next cell
    cells = [entry_point]
    x, y = entry_point
    letter_to_dir = {"N": N, "S": S, "E": E, "W": W}
    for letter in letters:
        # Map the letter to a direction, then to an step, and move
        direction = letter_to_dir[letter]
        direction_x, direction_y = MOVE[direction]
        x, y = x + direction_x, y + direction_y
        cells.append((x, y))
    return cells
