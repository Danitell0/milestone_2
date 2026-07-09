"""Writes the maze to the output file in the required format."""


def write_maze_file(path, maze, entry, exit_, path_letters):
    lines = maze.to_lines()
    try:
        with open(path, "w", encoding="utf-8") as f:
            for line in lines:
                f.write(line + "\n")
            f.write("\n")
            f.write(f"{entry[0]},{entry[1]}\n")
            f.write(f"{exit_[0]},{exit_[1]}\n")
            f.write("".join(path_letters) + "\n")
    except OSError as e:
        raise OSError(f"Could not write output file '{path}': {e}")
