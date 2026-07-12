"""ASCII renderer for the maze"""
from maze_generator.grid import N, S, E, W, MOVE


DEFAULT_COLORS = {
    "wall": "white",
    "path": "yellow",
    "entry": "green",
    "exit": "red",
    "block": "magenta",
}

COLOR_CHOICES = {
    "1": ("wall", "white"),
    "2": ("wall", "cyan"),
    "3": ("wall", "blue"),
    "4": ("wall", "green"),
    "5": ("wall", "magenta"),
}


def render(maze, entry_point, exit_point,
           path_cells=None, colors=None) -> list[list[tuple[str, str]]]:
    """Returns a list of rows; each row is a list of (text, color_name) segments."""
    colors = colors or DEFAULT_COLORS
    path_cells = path_cells or set()
    w, h = maze.width, maze.height
    wall_color = colors.get("wall")
    lines: list[list[tuple[str, str]]] = []

    for row in range(h + 1):
        corners = [("🮮", wall_color)]
        for x in range(w):
            if row == 0:
                closed = maze.is_wall(x, 0, N)
            elif row == h:
                closed = maze.is_wall(x, h - 1, S)
            else:
                closed = maze.is_wall(x, row - 1, S)
            corners.append(("━━" if closed else "  ", wall_color))
            corners.append(("🮮", wall_color))
        lines.append(corners)

        if row < h:
            walls = []
            walls.append(("┃" if maze.is_wall(0, row, 8) else "  ", wall_color))
            for x in range(w):
                cell = (x, row)
                if cell in maze.blocked_cells:
                    content, color = "🮕🮕", colors.get("block")
                elif cell == entry_point:
                    content, color = "EN", colors.get("entry")
                elif cell == exit_point:
                    content, color = "EX", colors.get("exit")
                elif cell in path_cells:
                    content, color = "..", colors.get("path")
                else:
                    content, color = "  ", None
                walls.append((content, color))
                closed = maze.is_wall(x, row, 2)  # east
                walls.append(("┃" if closed else " ", wall_color))
            lines.append(walls)

    return lines


def convert_path_from_letters(entry_point, letters) -> set:
    cells = [entry_point]
    x, y = entry_point
    letter_to_dir = {"N": N, "S": S, "E": E, "W": W}
    for letter in letters:
        direction = letter_to_dir[letter]
        direction_x, direction_y = MOVE[direction]
        x, y = x + direction_x, y + direction_y
        cells.append((x, y))
    return set(cells)
