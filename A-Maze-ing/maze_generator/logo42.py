
from typing import Iterable

DIGIT_4 = [
    "X.X",
    "X.X",
    "XXX",
    "..X",
    "..X",
]

DIGIT_2 = [
    "XXX",
    "..X",
    "XXX",
    "X..",
    "XXX",
]

CHI = [
    "XXX",
    "X..",
    "X..",
    "X..",
    "XXX",
]

DAN = [
    "XX.",
    "X.X",
    "X.X",
    "X.X",
    "XX.",
]

L_HEART = ["XX.", "XXX", "XXX", ".XX", "..X"]
R_HEART = [".XX", "XXX", "XXX", "XX.", "X.."]
SMILE_L = ["XXX", "XXX", "...", "X..", ".XX"]
SMILE_R = ["XXX", "XXX", "...", "..X", "XX."]
GHOST_L = [".XX", "XXX", "X.X", "XXX", "X.X"]
GHOST_R = ["XX.", "XXX", "X.X", "XXX", "X.X"]

LOGOS = {
    "42": (DIGIT_4, DIGIT_2),
    "CD": (CHI, DAN),
    "HEART": (L_HEART, R_HEART),
    "SMILE": (SMILE_L, SMILE_R),
    "GHOST": (GHOST_L, GHOST_R),
}


def build_logo_cells(width: int,
                     height: int,
                     avoid: Iterable[tuple[int, int]],
                     left: list[str] = DIGIT_4,
                     right: list[str] = DIGIT_2
                     ) -> set[tuple[int, int]]:
    """Generates the coordinate cells for a '42' logo centered in a grid.

    Args:
        width: The total width of the grid.
        height: The total height of the grid.
        avoid: An iterable of coordinates that the logo cannot overlap with.

    Returns:
        A set of (x, y) coordinate tuples representing the '42' logo,
        or an empty set if the logo doesn't fit or overlaps completely.
    """
    gap = 1  # space between 4 and 2
    pattern_width = len(left[0]) + gap + len(right[0])
    pattern_height = len(left)

    margin = 2  # margin 42 incomparing with maze
    if width < pattern_width + margin or height < pattern_height + margin:
        return set()

    avoid = set(avoid)
    # position of 42 logo
    ox = (width - pattern_width + 1) // 2
    oy = (height - pattern_height + 1) // 2

    cells = set()
    for row in range(pattern_height):
        combined = left[row] + "." * gap + right[row]
        for col, ch in enumerate(combined):
            if ch == "X":
                cells.add((ox + col, oy + row))

    if cells & avoid:
        # Try shifting slightly up/down before giving up entirely.
        for shift in (-2, 2, -3, 3, -4, 4):
            new_oy = oy + shift
            if new_oy < 1 or new_oy + pattern_height > height - 1:
                continue
            shifted = set()
            for row in range(pattern_height):
                combined = left[row] + "." * gap + right[row]
                for col, ch in enumerate(combined):
                    if ch == "X":
                        shifted.add((ox + col, new_oy + row))
            if not (shifted & avoid):
                return shifted
        return set()

    return cells
