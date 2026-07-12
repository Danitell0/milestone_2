"""ASCII renderer for the maze"""
from maze_generator.grid import N, S, E, W, MOVE


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


def render(maze, entry_point, exit_point,
           path_cells=None, colors=None,
           chars=None) -> list[list[tuple[str, str]]]:
    """Returns a list of rows; each row is a list of (text, color_name) segments."""
    colors = colors or DEFAULT_COLORS
    chars = chars or DEFAULT_CHARS
    path_cells = path_cells or set()
    w, h = maze.width, maze.height
    wall_color = colors.get("wall")
    lines: list[list[tuple[str, str]]] = []

    for row in range(h + 1):
        corners = [(chars["corner"], wall_color)]
        for x in range(w):
            if row == 0:
                closed = maze.is_wall(x, 0, N)
            elif row == h:
                closed = maze.is_wall(x, h - 1, S)
            else:
                closed = maze.is_wall(x, row - 1, S)
            corners.append((chars["h_wall"] if closed else chars["h_open"], wall_color))
            corners.append((chars["corner"], wall_color))
        lines.append(corners)

        if row < h:
            walls = []
            walls.append((chars["v_wall"] if maze.is_wall(0, row, 8) else chars["h_open"],
                          wall_color))
            for x in range(w):
                cell = (x, row)
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
                closed = maze.is_wall(x, row, 2)  # east
                walls.append((chars["v_wall"] if closed else chars["v_open"], wall_color))
            lines.append(walls)

    return lines


def convert_path_from_letters(entry_point, letters) -> list:
    cells = [entry_point]
    x, y = entry_point
    letter_to_dir = {"N": N, "S": S, "E": E, "W": W}
    for letter in letters:
        direction = letter_to_dir[letter]
        direction_x, direction_y = MOVE[direction]
        x, y = x + direction_x, y + direction_y
        cells.append((x, y))
    return cells
