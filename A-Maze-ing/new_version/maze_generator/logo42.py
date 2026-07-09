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

def build_logo_cells(width, height, avoid) -> set:
    gap = 1 # space between 4 and 2
    pattern_width = len(DIGIT_4[0]) + gap + len(DIGIT_2[0])
    pattern_height = len(DIGIT_4)

    margin = 2 #  margin 42 incomparing with maze
    if width < pattern_width + margin or height < pattern_height + margin:
        return set()

    avoid = set(avoid)
    # position of 42 logo
    ox = (width - pattern_width + 1) // 2
    oy = (height - pattern_height + 1) // 2

    cells = set()
    for row in range(pattern_height):
        combined = DIGIT_4[row] + "." * gap + DIGIT_2[row]
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
                combined = DIGIT_4[row] + "." * gap + DIGIT_2[row]
                for col, ch in enumerate(combined):
                    if ch == "X":
                        shifted.add((ox + col, new_oy + row))
            if not (shifted & avoid):
                return shifted
        return set()

    return cells
