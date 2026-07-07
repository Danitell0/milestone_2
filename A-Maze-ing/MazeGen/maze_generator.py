#!/usr/bin/env python3

import random
import curses
from typing import Optional
from enum import Enum

N, E, S, W = 0, 1, 2, 3
DIRECTIONS = {
    N: (0, -1),
    E: (1, 0),
    S: (0, 1),
    W: (-1, 0),
}
OPPOSITE = {N: S, S: N, E: W, W: E}

class MazeGenerator():

    def __init__(self, width: int, height: int,
                 entry_point: tuple[int, int],
                 exit_point: tuple[int, int],
                 perfect: bool = True, # import from file please
                 output_file: str = "maze.txt", # import from file please
                 seed: Optional[int] = None) -> None:
        if seed is None:
            seed = random.randint(100_000_000, 999_999_999)
        self._width = width
        self._height = height
        self._entry = entry_point
        self._exit = exit_point
        self._perfect = perfect
        self._output_file = output_file
        self._seed = seed
        random.seed(self._seed)
        self.grid: list[list[int]] = [
            [0 for _ in range(self._width)] for _ in range(self._height)
        ]
        self.pattern_cells_set: set[tuple[int, int]] = set()

    @property
    def width(self) -> int:
        return self._width
    
    @property
    def height(self) -> int:
        return self._height
    
    @property
    def exit(self) -> tuple[int, int]:
        return self._exit

    @property
    def entry(self) -> tuple[int, int]:
        return self._entry

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self._width and 0 <= y < self._height

    def neighbors(self, x: int, y: int) -> list[tuple[int, int, int]]:
        res = []
        for d, (dx, dy) in DIRECTIONS.items():
            nx, ny = x + dx, y + dy
            if self.in_bounds(nx, ny):
                res.append((nx, ny, d))
        return res

    def close_border_walls(self) -> None:
        for x in range(self._width):
            self.set_wall(x, 0, N, True)
            self.set_wall(x, self._height - 1, S, True)
        for y in range(self._height):
            self.set_wall(0, y, W, True)
            self.set_wall(self._width - 1, y, E, True)

    def generate_perfect(self) -> None:
        stack: list[tuple[int, int]] = [self._entry]
        visited = [[False for _ in range(self._width)] for _ in range(self._height)]
        visited[self._entry[1]][self._entry[0]] = True

        for y in range(self._height):
            for x in range(self._width):
                self.grid[y][x] = 0
                for d in (N, E, S, W):
                    self.set_wall(x, y, d, True)

        while stack:
            x, y = stack[-1]
            unvisited_neighbors = []
            for nx, ny, d in self.neighbors(x, y):
                if not visited[ny][nx]:
                    unvisited_neighbors.append((nx, ny, d))
            if not unvisited_neighbors:
                stack.pop()
                continue
            nx, ny, d = random.choice(unvisited_neighbors)
            self.set_wall(x, y, d, False)
            self.set_wall(nx, ny, OPPOSITE[d], False)
            visited[ny][nx] = True
            stack.append((nx, ny))

        self.close_border_walls()
    
    def add_loops(self, count: int) -> None:
        for _ in range(count):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            dirs = [d for d in (N, E, S, W)]
            random.shuffle(dirs)
            for d in dirs:
                nx, ny = x + DIRECTIONS[d][0], y + DIRECTIONS[d][1]
                if not self.in_bounds(nx, ny):
                    continue
                if (x == 0 and d == W) or (x == self.width - 1 and d == E):
                    continue
                if (y == 0 and d == N) or (y == self.height - 1 and d == S):
                    continue
                if self.has_wall(x, y, d):
                    self.set_wall(x, y, d, False)
                    self.set_wall(nx, ny, OPPOSITE[d], False)
                    break

    def set_wall(self, x: int, y: int, direction: int, closed: bool) -> None:
        bit = 1 << direction
        if closed:
            self.grid[y][x] |= bit
        else:
            self.grid[y][x] &= ~bit

    def has_wall(self, col: int, row: int, direction: int) -> bool:
        bit = 1 << direction
        return (self.grid[row][col] & bit) != 0

    def _reachable(self, start: tuple[int, int], end: tuple[int, int]) -> bool:
        from collections import deque
        sx, sy = start
        ex, ey = end
        visited = [[False for _ in range(self.width)] for _ in range(self.height)]
        visited[sy][sx] = True
        queue = deque([(sx, sy)])

        while queue:
            x, y = queue.popleft()
            if (x, y) == (ex, ey):
                return True
            for d, (dx, dy) in DIRECTIONS.items():
                nx, ny = x + dx, y + dy
                if not self.in_bounds(nx, ny) or self.has_wall(x, y, d) or visited[ny][nx]:
                    continue
                visited[ny][nx] = True
                queue.append((nx, ny))
        return False

    def _pattern_cells(self, start_x: int, start_y: int) -> Optional[list[tuple[int, int]]]:
        four_coords = [(start_x, start_y), (start_x, start_y + 1), (start_x, start_y + 2), (start_x + 1, start_y + 1)]
        two_coords = [(start_x + 2, start_y), (start_x + 3, start_y), (start_x + 3, start_y + 1), (start_x + 2, start_y + 2), (start_x + 3, start_y + 2)]
        coords = four_coords + two_coords
        for (cx, cy) in coords:
            if not self.in_bounds(cx, cy):
                return None
        return coords

    def embed_42_pattern(self, entry: tuple[int, int], exit_: tuple[int, int]) -> bool:
        pattern_w, pattern_h = 4, 3
        self.pattern_cells_set.clear()
        if self._width < pattern_w + 2 or self._height < pattern_h + 2:
            return False

        def close_cell(cx: int, cy: int):
            for d in (N, E, S, W):
                self.set_wall(cx, cy, d, True)

        center_x = (self._width - pattern_w) // 2
        center_y = (self._height - pattern_h) // 2
        
        for offset in range(max(self._width, self._height)):
            for dx in range(-offset, offset + 1):
                for dy in range(-offset, offset + 1):
                    if max(abs(dx), abs(dy)) != offset:
                        continue
                    sx, sy = center_x + dx, center_y + dy
                    coords = self._pattern_cells(sx, sy)
                    if coords is None:
                        continue
                    
                    saved = {(cx, cy): self.grid[cy][cx] for (cx, cy) in coords}
                    for (cx, cy) in coords:
                        close_cell(cx, cy)

                    if self._reachable(entry, exit_):
                        self.pattern_cells_set = set(coords)
                        return True
                    
                    for (cx, cy), val in saved.items():
                        self.grid[cy][cx] = val
        return False

    def to_hex_lines(self) -> list[str]:
        return ["".join(f"{(self.grid[y][x] & 0xF):X}" for x in range(self._width)) for y in range(self._height)]

    def shortest_path(self, start: tuple[int, int], end: tuple[int, int]) -> Optional[list[tuple[int, int]]]:
        from collections import deque
        sx, sy = start
        queue = deque([(sx, sy)])
        visited = [[False for _ in range(self._width)] for _ in range(self._height)]
        visited[sy][sx] = True
        parent: dict[tuple[int, int], tuple[int, int]] = {}

        while queue:
            x, y = queue.popleft()
            if (x, y) == end:
                break
            for d, (dx, dy) in DIRECTIONS.items():
                nx, ny = x + dx, y + dy
                if self.in_bounds(nx, ny) and not self.has_wall(x, y, d) and not visited[ny][nx]:
                    visited[ny][nx] = True
                    parent[(nx, ny)] = (x, y)
                    queue.append((nx, ny))

        if end not in parent and start != end:
            return None

        path = []
        cur = end
        while cur != start:
            path.append(cur)
            cur = parent[cur]
        path.append(start)
        path.reverse()
        return path


    def check_corridor_width(self) -> bool:
        for y in range(self.height - 2):
            for x in range(self._width - 2):
                if all(self.grid[by][bx] == 0 for by in range(y, y + 3) for bx in range(x, x + 3)):
                    return False
        return True

    def run_visualizer(self):
        def main_loop(stdscr):
            curses.curs_set(0)
            stdscr.nodelay(False)
            
            # Color palette setup
            curses.start_color()
            wall_colors = [curses.COLOR_BLUE, curses.COLOR_CYAN, curses.COLOR_MAGENTA, curses.COLOR_GREEN, curses.COLOR_YELLOW]
            color_idx = 0
            
            # Init base tracking settings
            show_path = True
            highlight_42 = True


            while True:
                # Color pairs re-assignment
                curses.init_pair(1, wall_colors[color_idx], curses.COLOR_BLACK) # Walls
                curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Entry
                curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)    # Exit
                curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK) # Solution path
                curses.init_pair(5, curses.COLOR_RED, curses.COLOR_RED)      # 42 Pattern blocks

                self.generate_perfect(self._entry)
                if not self._perfect:
                    self.add_loops(max(1, (self._width * self._height) // 10))
                self.embed_42_pattern(self._entry, self._exit)
                path_coords = self.shortest_path(self._entry, self._exit) or []

                while True:
                    stdscr.clear()
                    
                    # Check terminal boundaries
                    scr_h, scr_w = stdscr.getmaxyx()
                    needed_h = (self._height * 2 + 1) + 6
                    needed_w = max(self._width * 2 + 2, 50)
                    if scr_h < needed_h or scr_w < needed_w:
                        stdscr.addstr(0, 0, f"Terminal window too small! Minimal size required: {needed_w}x{needed_h}")
                        stdscr.addstr(1, 0, "Resize your terminal to continue...")
                        ch = stdscr.getch()
                        if ch in (ord('q'), ord('Q'), 27):
                            return
                        continue

                    # Build ASCII canvas string buffer
                    canvas = [[" " for _ in range(self._width * 2 + 1)] for _ in range(self._height * 2 + 1)]
                    
                    # Fill structure walls
                    for y in range(self._height):
                        for x in range(self._width):
                            cy, cx = y * 2 + 1, x * 2 + 1
                            if self.has_wall(x, y, N): canvas[cy - 1][cx] = "─"
                            if self.has_wall(x, y, S): canvas[cy + 1][cx] = "─"
                            if self.has_wall(x, y, W): canvas[cy][cx - 1] = "│"
                            if self.has_wall(x, y, E): canvas[cy][cx + 1] = "│"
                            # Intersections corners
                            canvas[cy - 1][cx - 1] = "┼"
                            canvas[cy - 1][cx + 1] = "┼"
                            canvas[cy + 1][cx - 1] = "┼"
                            canvas[cy + 1][cx + 1] = "┼"

                    # Render Canvas to Screen Buffer
                    for y in range(len(canvas)):
                        for x in range(len(canvas[y])):
                            char = canvas[y][x]
                            if char in ("─", "│", "┼"):
                                stdscr.addch(y, x, char, curses.color_pair(1))
                            else:
                                stdscr.addch(y, x, " ")

                    # Overlay Path Visual Elements
                    if show_path:
                        for px, py in path_coords:
                            if (px, py) != self._entry and (px, py) != self._exit:
                                stdscr.addch(py * 2 + 1, px * 2 + 1, "·", curses.color_pair(4) | curses.A_BOLD)

                    # Overlay 42 Pattern Highlight
                    if highlight_42:
                        for px, py in self.pattern_cells_set:
                            stdscr.addch(py * 2 + 1, px * 2 + 1, "█", curses.color_pair(5))

                    # Overlay Entry and Exit Indicators
                    stdscr.addch(self._entry[1] * 2 + 1, self._entry[0] * 2 + 1, "S", curses.color_pair(2) | curses.A_BOLD)
                    stdscr.addch(self._exit[1] * 2 + 1, self._exit[0] * 2 + 1, "E", curses.color_pair(3) | curses.A_BOLD)

                    # Control HUD Render Panel
                    offset_y = self._height * 2 + 2
                    stdscr.addstr(offset_y, 0, "═" * (self._width * 2 + 1), curses.A_DIM)
                    stdscr.addstr(offset_y + 1, 0, "[R] Re-generate Maze   [P] Toggle Path Visibility", curses.A_BOLD)
                    stdscr.addstr(offset_y + 2, 0, "[C] Change Wall Color  [4] Toggle '42' Highlight", curses.A_BOLD)
                    stdscr.addstr(offset_y + 3, 0, "[Q/ESC] Exit Visualizer", curses.A_BOLD)

                    # Capture event actions
                    key = stdscr.getch()
                    if key in (ord('r'), ord('R')):
                        break  # Break interior loop to re-generate structural values
                    elif key in (ord('p'), ord('P')):
                        show_path = not show_path
                    elif key in (ord('c'), ord('C')):
                        color_idx = (color_idx + 1) % len(wall_colors)
                    elif key == ord('4'):
                        highlight_42 = not highlight_42
                    elif key in (ord('q'), ord('Q'), 27):
                        return
