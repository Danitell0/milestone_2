*This project has been created as part of the 42 curriculum by chilam, danmorei*

# Description

A Python terminal application that generates a maze from a simple configuration file, renders it interactively in the terminal with a curses-based menu system, and solves it with a breadth-first search, writing the maze and its solution path out to a file.

## Features

* Perfect maze generation via a recursive-backtracker (randomized depth-first search)
Hidden "42" logo: the generator carves the digits "42" into the maze as blocked cells, tucked away from the entry, exit, corners, and center.

* Imperfect mazes: when PERFECT=False, extra loops are added and dead ends are reduced, creating a maze with multiple possible paths instead of exactly one

* Deterministic generation via an optional random seed, so the same seed reproduces the same maze — or regenerate with a fresh random seed on demand

* BFS solver that finds the shortest path from entry to exit (Breadth First Search)

* Interactive curses menu to generate a maze and then:

    * Toggle the solution path on/off
    * Play an animated step-by-step reveal of the solution path
    * Cycle through maze wall colors
    * Cycle through visual themes (box-drawing, ASCII, dots, rounded, shade)
    * Regenerate the maze with a new random seed

* Pop-up warning/info messages (e.g. when the maze is too small for the "42" logo, or confirming the output file was written)

* Maze export to a plain-text file, including the solution path

# mazegen

A reusable maze generator: builds a maze with a hidden "42" logo carved as
blocked cells, and solves it with a breadth-first search.

## Install

``` bash
pip install mazegen-1.0.0-py3-none-any.whl
```

for easy test run:
``` bash
python -c "from mazegen import MazeGenerator; g = MazeGenerator(width=10, height=10, entry_point=(0,0), exit_point=(9,9), seed=1); g.generate(); print(''.join(g.solution))"
```
## Basic usage

```python
from mazegen import MazeGenerator

gen = MazeGenerator(width=20, height=15, entry_point=(0, 0), exit_point=(19, 14))
gen.generate()
```

## Custom parameters

```python
gen = MazeGenerator(
    width=30,          # number of columns
    height=20,         # number of rows
    entry_point=(0, 0),
    exit_point=(29, 19),
    perfect=True,      # exactly one path between any two cells
    seed=42,           # reproducible: same seed -> same maze
)
gen.generate()
```

If `seed` is omitted a random one is chosen and stored on `gen.seed`, so any
maze can be reproduced. `gen.regenerate()` rebuilds with a fresh random seed;
`gen.regenerate(seed=7)` rebuilds with a specific one.

## Accessing the generated structure

`gen.maze` is a `Maze`: a grid where each cell is a 4-bit value and a set bit
means that wall is **closed** (N=1, E=2, S=4, W=8).

```python
maze = gen.maze

maze.width, maze.height           # dimensions
maze.is_wall(0, 0, 1)             # is the north wall of cell (0,0) closed?
maze.is_open(0, 0, 2)             # is the east wall of cell (0,0) open?
maze.open_neighbors(0, 0)         # [(x, y), ...] cells reachable in one step
maze.degree(0, 0)                 # number of open walls (1 == dead end)
maze.blocked_cells                # {(x, y), ...} cells forming the "42" logo
maze.cells[y][x]                  # raw 4-bit value for a cell
maze.to_lines()                   # ["bd15...", ...] one hex string per row
```

Direction constants are importable if you prefer names over numbers:

```python
from mazegen.grid import N, E, S, W
maze.is_wall(0, 0, N)
```

## Accessing the solution

`gen.solution` is the shortest path from entry to exit as direction letters:

```python
gen.solution          # ["E", "S", "S", "E", ...]
"".join(gen.solution) # "ESSE..."
```

## Warnings

`gen.warnings` holds non-fatal messages from the last generation — for
example, if the maze is too small to fit the "42" logo, it is omitted and a
warning is recorded.

```python
for msg in gen.warnings:
    print(msg)
```

# Instructions

Install development tools (mypy, flake8) with:

```
make install
```
### Usage

Run the program, pointing it at a configuration file:
```
python3 a_maze_ing.py config.txt
```
Or, using the provided Makefile:
```
make run
```
To run with the Python debugger attached:
```
bashmake debug
```

Once running, use the arrow keys to navigate the menu and Enter to select. From the main menu, choose Generate Maze to build and display it, then use the submenu to toggle the path, play the animation, change colors/visuals, or regenerate.

### Makefile commands

| **Command**            | **Description**                                         |
| -------------          | :------------------------------------------------------ |
| **make install**       | Installs mypy and flake8                                |
| **make run**           | Runs a_maze_ing.py with config.txt                      |
| **make debug**         | Runs the program under pdb                              |
| **make clean**         | Removes __pycache__ and .mypy_cache directories         | 
| **make lint**          | Runs flake8 and mypy (with several strictness flags)    |
| **make lint-strict**   | Runs flake8 and mypy --strict                           |

### Configuration

The program is driven by a config file (see `config.txt`):

**Example**
```
WIDTH=20
HEIGHT=20
ENTRY=0,0
EXIT=19,19
OUTPUT_FILE=maze.txt
PERFECT=True
```

| Key             | Description                                                            |
|-----------------|------------------------------------------------------------------------|
| `WIDTH`         | Number of columns in the maze grid                                     |
| `HEIGHT`        | Number of rows in the maze grid                                        |
| `ENTRY`         | Starting cell, as `col,row`                                            |
| `EXIT`          | Target/exit cell, as `col,row`                                         |
| `OUTPUT_FILE`   | File the generated maze and solution are written to                    |
| `PERFECT`       | `True` for exactly one path between any two cells, `False` to add loops and trim dead ends |
| `SEED`          | *(optional)* Random seed for reproducible generation; a random seed is used if omitted, and each "Regenerate" picks a new one |

Configuration parsing and validation is handled by `configurations/check_parsing.py` (`MazeConfig`), which raises a `ConfigError` (or `FileNotFoundError`/`PermissionError` for file access issues) if the file is malformed. Validation rules include:

- All keys except `SEED` are required: `WIDTH`, `HEIGHT`, `ENTRY`, `EXIT`, `OUTPUT_FILE`, `PERFECT`
- `WIDTH` and `HEIGHT` must be positive integers
- `ENTRY` and `EXIT` must be in `X,Y` format with integer coordinates
- `PERFECT` must be exactly `True` or `False`
- `SEED`, if present, must be an integer
- Entry and exit points must fall within the grid bounds (`0 <= X < WIDTH`, `0 <= Y < HEIGHT`)
- Entry and exit points must not be the same cell
- Lines starting with `#` are treated as comments and ignored

### How It Works

1. **Generation** (`maze_generator/generator.py`) carves a perfect maze from the entry point using a randomized recursive-backtracker (`carve_perfect`): it walks to a random unvisited neighbor, opening the wall between the two cells, and backtracks when it hits a dead end.

2. **Hidden logo**: before carving, `logo42.py` computes a set of "blocked" cells shaped like "42", avoiding the entry, exit, grid corners, and center. If the maze is too small, the logo is skipped and a warning is shown instead.

3. **Reconnection**: if the logo (or anything else) splits the grid into disconnected regions, any unreached cells are stitched back in by opening a wall toward an already-visited neighbor.

4. **Imperfect mazes**: if `PERFECT=False`, `add_loops` removes a handful of extra internal walls to introduce loops, and `reduce_dead_ends` opens an extra wall from dead-end cells to cut down on dead ends.

5. **Solving** (`solver.py`) runs a breadth-first search from entry to exit over the open walls, returning the shortest path as a string of direction letters (`N`/`E`/`S`/`W`).

6. **Writing** (`writer.py`) serializes the maze grid, entry/exit coordinates, and solution path to `OUTPUT_FILE`.

7. **Display** (`display/window.py`, `display/maze_display.py`) drives a `curses` menu system, renders the maze and (optionally) its solution path with selectable color/character themes, and can animate the path being revealed cell by cell.

### Maze Encoding

Each cell is stored as a 4-bit value where a set bit means that wall is **closed**:

| Bit | Value | Direction |
|-----|-------|-----------|
| 0   | 1     | North     |
| 1   | 2     | East      |
| 2   | 4     | South     |
| 3   | 8     | West      |

A cell's value is the sum of its closed walls, printed as a single hex digit (e.g. `d` = `1101` = North, South, and West walls closed, East open).

### Output Format

After running, the maze is written to the file named in `OUTPUT_FILE` (e.g. `maze.txt`):

**Example**

```
bd15513b95153b951397
c3ab96ac43c3ac696a83
9686abc3d47ac53abaaa
ad696c3a953a97aac2aa
c53c5386a96a856c3aaa
956956c56c3ac5556aaa
a93a955393c693953aea
c6aaad142c156c6bac52
93aa83afafafff968796
aac6aaefef857f85696b
ac396c3fffafffe95692
ad2a97a93fafd516956a
83aaa96aefafffad43d2
eaa86a9453c539693c3e
92ea96c3bc556c56c383
aa96a93c0793955556ea
aeabaaad696c6d155396
a946aac53ad153c3ba83
86956c3bac3c3a96aaea
c7c55546c5456c6d4456

0,0
19,19
SESWSSEESWWSSENESSSENNNNEENWWNENNENESSESSWSEENNEESWSESENNNNNWNEESSEESSWWSEEEENWNNNENESSSSSSSEESWSWSWWSWSSWSEENESESWWWWWSWNWSWSSESEENWNEESSENENWNEEESSSEE

```

### Project Structure

```
a-maze-ing/
├── a_maze_ing.py                  # Entry point
├── configurations/
│   └── check_parsing.py           # MazeConfig / ConfigError — config file parsing & validation
├── maze_generator/
│   ├── __init__.py
│   ├── grid.py                    # Maze class — wall bitmask grid representation
│   ├── generator.py               # Perfect-maze carving, loops, dead-end reduction
│   ├── logo42.py                  # Builds the hidden "42" logo cell pattern
│   ├── solver.py                  # BFS shortest-path solver
│   └── writer.py                  # Serializes the maze + solution to a file
├── display/
│   ├── __init__.py
│   ├── window.py                  # MazeWindow / Menu — curses menu & interaction loop
│   └── maze_display.py            # ASCII/box-drawing renderer, color & character themes
├── config.txt                     # Example configuration
├── maze.txt                       # Example generated output
├── Makefile
└── README.md
```

## Technical Choices & Algorithm

### Why We Chose the Recursive-Backtracker Algorithm
We chose the randomized depth-first search (recursive backtracker) because it is highly efficient for generating "perfect" mazes and naturally creates long, winding corridors with a lower density of intersections. This characteristics makes the maze visually engaging in the terminal and provides a solid foundation for the BFS solver to demonstrate a clear pathfinding trajectory.

### Code Reusability
Our codebase was designed with modularity in mind so components can be easily reused in future 42 projects:
* **`maze_generator/grid.py`:** The 4-bit wall-encoding scheme and data structures are fully independent of the rendering and generation logic, allowing this module to be reused for any grid-based game or pathfinding simulation.
* **`configurations/check_parsing.py`:** This strict configuration parser can be adapted to any project requiring key-value parsing from raw configuration text files with minimal adjustments.


## Team & Project Management

### Roles of Team Members
* **chilam:** [Implemented the recursive-backtracker algorithm and loop creation logic]
* **danmorei:** [Developed the interactive `curses` interface and configuration validation engine]
* **together:** [BFS solver engine, file exporters and cleaning files]

### Anticipated Planning vs. Evolution
* **Anticipated Planning:** We originally estimated 7 days for core generation and algorithms, 5 days for the interface, and 3 days for final integration and linting.
* **Evolution:** Integrating the hidden "42" logo while maintaining a fully valid, connectable maze pattern regardless of dimension required significant debugging time, forcing us to adjust our rendering timelines but resulting in a much cleaner edge-case solution.

### Retrospective
* **What Worked Well:** Our clean separation of data structures (`grid.py`) from rendering (`maze_display.py`) allowed us to work concurrently without merge conflicts.
* **What Could Be Improved:** We should have written automation tests for the config edge cases earlier in the lifecycle to minimize troubleshooting during integration.


## Resources

* [Maze Generation Algorithms - Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
* [Python Curses Documentation & How-To](https://docs.python.org/3/howto/curses.html)

### AI Usage Disclosure
* **Tasks Assisted:** AI was utilized to generate test scripts verifying configuration edge cases and to debug screen-flickering anomalies tied to specific terminal resizing triggers within the `curses` refresh loop.
