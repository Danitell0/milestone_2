"""Writes the maze to the output file"""

from .grid import Maze


def write_maze_file(output_file: str,
                    maze: Maze,
                    entry_point: tuple[int, int],
                    exit_point: tuple[int, int],
                    path_letters: list[str]) -> None:
    lines = maze.to_lines()
    try:
        with open(output_file, "w") as raw:
            for line in lines:
                raw.write(line + "\n")
            raw.write("\n")
            raw.write(f"{entry_point[0]},{entry_point[1]}\n")
            raw.write(f"{exit_point[0]},{exit_point[1]}\n")
            raw.write("".join(path_letters) + "\n")
    except OSError as e:
        raise OSError(f"Couldn't write output in '{output_file}': {e}")
