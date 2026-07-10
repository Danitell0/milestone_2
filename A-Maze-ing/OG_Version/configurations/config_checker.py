#!/usr/bin/env python3

REQUIRED_KEYS = ['WIDTH', 'HEIGHT', 'ENTRY', 'EXIT',
                 'OUTPUT_FILE', 'PERFECT']

# --------------------------------------------- Configurations


def config_parsing(config: str) -> dict[str, str]:
    """Function to get settings from config.txt and return dict"""
    try:
        settings = {}
        with open(config, 'r') as config_file:
            for line in config_file:
                if line.startswith('#'):
                    continue
                if line.strip():
                    setting = line.split('=', 1)
                    settings[setting[0]] = setting[1].strip('\n')
    except Exception as e:
        raise ValueError(f"Error opening configuration file: {e}")
    return settings


def validate_config(settings: dict[str, str]) -> None:
    """Match settings with required keys and check their values"""
    for key in REQUIRED_KEYS:
        if key not in settings:
            raise ValueError(f"Missing required key {key}")
    try:
        width = int(settings['WIDTH'])
    except ValueError:
        raise ValueError("Impossible to use type as width.")
    if width <= 0:
        raise ValueError(f"Maze with {width} width can't be generated.")
    try:
        height = int(settings['HEIGHT'])
    except ValueError:
        raise ValueError("Impossible to use type as height.")
    if height <= 0:
        raise ValueError(f"Maze with {height} height can't be generated.")
    try:
        entry = settings['ENTRY'].split(',')
        if len(entry) != 2:
            raise ValueError("Invalid syntax for entry, use: 'X,Y'")
    except ValueError:
        raise ValueError("Impossible to use value as entry point.")
    try:
        entry_x = int(entry[0])
        entry_y = int(entry[1])
    except ValueError:
        raise ValueError("Invalid syntax for positions")
    try:
        exit_p = settings['EXIT'].split(',')
        if len(exit_p) != 2:
            raise ValueError("Invalid syntax for exit, use: X,Y")
    except ValueError:
        raise ValueError("Impossible to use value as exit point.")
    try:
        exit_x = int(exit_p[0])
        exit_y = int(exit_p[1])
    except ValueError:
        raise ValueError("Invalid syntax for positions")
    if settings['PERFECT'] not in ["True", "False"]:
        raise ValueError("Perfect key must be either 'True' or 'False'.")

    # --------------------------------------------- position checker

    if not (0 <= entry_x < width) or not (0 <= entry_y < height):
        raise ValueError("Entry position out of bounds.")
    if not (0 <= exit_x < width) or not (0 <= exit_y < height):
        raise ValueError("Exit position out of bounds.")
    if entry_x == exit_x and entry_y == exit_y:
        raise ValueError("Entry position and exit position can't be equal.")

# ---------------------------------------------
