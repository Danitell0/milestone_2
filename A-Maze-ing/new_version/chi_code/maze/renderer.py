"""ASCII terminal renderer for the maze."""
from .grid import N, S, DELTA

RESET = "\033[0m"

DEFAULT_COLORS = {
    "wall": "\033[97m",    # bright white
    "path": "\033[93m",    # yellow
    "entry": "\033[92m",   # green
    "exit": "\033[91m",    # red
    "block": "\033[35m",   # magenta (the '42' pattern)
}

COLOR_CHOICES = {
    "1": ("wall", "\033[97m", "white"),
    "2": ("wall", "\033[96m", "cyan"),
    "3": ("wall", "\033[94m", "blue"),
    "4": ("wall", "\033[92m", "green"),
    "5": ("wall", "\033[95m", "magenta"),
}


def _colorize(text, color, enabled):
    if not enabled or not color:
        return text
    return f"{color}{text}{RESET}"


def render(maze, entry, exit_, path_cells=None, colors=None, use_color=True):
    """Return the maze as a printable ASCII string."""
    colors = colors or DEFAULT_COLORS
    path_cells = path_cells or set()
    w, h = maze.width, maze.height
    wall_char = _colorize("━━", colors.get("wall"), use_color)
    vwall_char = _colorize("┃", colors.get("wall"), use_color)
    lines = []

    for row in range(h + 1):
        segs = [_colorize("🮮", colors.get("wall"), use_color)]
        for x in range(w):
            if row == 0:
                closed = maze.is_wall(x, 0, N)
            elif row == h:
                closed = maze.is_wall(x, h - 1, S)
            else:
                closed = maze.is_wall(x, row - 1, S)
            segs.append(wall_char if closed else "  ")
            segs.append(_colorize("🮮", colors.get("wall"), use_color))
        lines.append("".join(segs))

        if row < h:
            segs = []
            # West border of the row
            segs.append(vwall_char if maze.is_wall(0, row, 8) else " ")
            for x in range(w):
                cell = (x, row)
                if cell in maze.blocked:
                    content = _colorize("🮕🮕", colors.get("block"), use_color)
                elif cell == entry:
                    content = _colorize("EN", colors.get("entry"), use_color)
                elif cell == exit_:
                    content = _colorize("EX", colors.get("exit"), use_color)
                elif cell in path_cells:
                    content = _colorize("..", colors.get("path"), use_color)
                else:
                    content = "  "
                segs.append(content)
                closed = maze.is_wall(x, row, 2)  # East
                segs.append(vwall_char if closed else " ")
            lines.append("".join(segs))

    return "\n".join(lines)


def path_cells_from_letters(entry, letters):
    """Reconstruct the list of (x, y) cells visited along the solution path."""
    cells = [entry]
    x, y = entry
    letter_to_dir = {"N": N, "S": S, "E": 2, "W": 8}
    for letter in letters:
        d = letter_to_dir[letter]
        dx, dy = DELTA[d]
        x, y = x + dx, y + dy
        cells.append((x, y))
    return set(cells)
