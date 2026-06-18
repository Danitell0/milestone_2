#!/usr/bin/env python3

import sys
import typing

REQUIRED_KEYS = ['WIDTH', 'HEIGHT', 'ENTRY', 'EXIT',
                 'OUTPUT_FILE', 'PERFECT']

def config_parsing(config: str) -> dict[str, str]:
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

def validate_config(settings: dict) -> bool:
    ...


def main() -> None:
    if len(sys.argv) != 2:
        print(f"Missing configuration file: {sys.argv[0]} <file>")
        exit(1)
    print("========== A-Maze-ing ==========")
    try:
        settings = config_parsing(sys.argv[1])
    except ValueError as e:
        print(e, file=sys.stderr)
        exit(1)

if __name__ == "__main__":
    main()
