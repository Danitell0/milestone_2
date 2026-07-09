#!/usr/bin/env python3
"""A-Maze-ing: maze generator.

Usage:
    python3 a_maze_ing.py config.txt
"""
import sys
import random

from maze.config import Config, ConfigError
from maze.generator import generate
from maze.solver import shortest_path
from maze.writer import write_maze_file
from maze.renderer import render, path_cells_from_letters, DEFAULT_COLORS, COLOR_CHOICES


def build_and_save(cfg, seed):
    maze, warnings = generate(
        cfg.width, cfg.height, cfg.entry, cfg.exit, cfg.perfect, seed=seed
    )
    for w in warnings:
        print(f"Warning: {w}")

    letters = shortest_path(maze, cfg.entry, cfg.exit)
    if letters is None:
        raise RuntimeError(
            "Internal error: generated maze has no path between entry and exit."
        )

    write_maze_file(cfg.output_file, maze, cfg.entry, cfg.exit, letters)
    print(f"Maze written to '{cfg.output_file}' (seed={seed}).")
    return maze, letters


def print_menu():
    print(
        "\nCommands: [r] regenerate  [p] toggle path  [c] change wall color  "
        "[q] quit\n> ",
        end="",
    )


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt", file=sys.stderr)
        return 1

    try:
        cfg = Config.from_file(sys.argv[1])
    except ConfigError as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        return 1

    seed = cfg.seed if cfg.seed is not None else random.randint(0, 999999999)

    try:
        maze, letters = build_and_save(cfg, seed)
    except Exception as e:
        print(f"Error while generating the maze: {e}", file=sys.stderr)
        return 1

    show_path = True
    colors = dict(DEFAULT_COLORS)

    def draw():
        pc = path_cells_from_letters(cfg.entry, letters) if show_path else None
        print()
        print(render(maze, cfg.entry, cfg.exit, path_cells=pc, colors=colors))
        print(
            f"\nEntry: {cfg.entry}  Exit: {cfg.exit}  "
            f"Path length: {len(letters)} steps  Perfect: {cfg.perfect}"
        )

    draw()

    while True:
        print_menu()
        try:
            choice = input().strip().lower()
        except EOFError:
            break

        if choice == "q":
            break
        elif choice == "p":
            show_path = not show_path
            draw()
        elif choice == "r":
            seed = random.randint(0, 999999999)
            try:
                maze, letters = build_and_save(cfg, seed)
            except Exception as e:
                print(f"Error while generating the maze: {e}", file=sys.stderr)
                continue
            draw()
        elif choice == "c":
            # print("Choose a wall color: 1) white 2) cyan 3) blue 4) green 5) magenta") # better change to random choice (rest can be deleted)
            # pick = input("> ").strip()
            pick = random.choice(list(COLOR_CHOICES))
            if pick in COLOR_CHOICES:
                _, code, name = COLOR_CHOICES[pick]
                colors["wall"] = code
                print(f"Wall color set to {name}.")
                draw()
            # else:
            #     print("Unknown option.")
        else:
            print("Unknown command.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
