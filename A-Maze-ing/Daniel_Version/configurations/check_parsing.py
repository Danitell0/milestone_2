import random

class ConfigError(Exception):
    """Raised when the configuration file is invalid."""

REQUIRED_KEYS = ['WIDTH', 'HEIGHT', 'ENTRY', 'EXIT',
				 'OUTPUT_FILE', 'PERFECT']

class MazeConfig:
    def __init__(self, width: int, height: int,
                 entry_point: tuple[int, int],
                 exit_point: tuple[int, int],
                 output_file: str,
                 perfect: bool = True,
                 seed: int | None = None) -> None:
        self.width = width
        self.height = height
        self.entry_point = entry_point
        self.exit_point = exit_point
        self.output_file = output_file
        self.perfect = perfect
        self.seed = seed


    @classmethod
    def from_file(cls, config_file: str) -> "MazeConfig":
        try:
            settings = {}
            with open(config_file, 'r') as raw:
                for line in raw:
                    if line.startswith('#'):
                        continue
                    if line.strip():
                        key, value = line.split('=', 1)
                        settings[key.strip()] = value.strip()
        except FileNotFoundError:
            raise FileNotFoundError(f"'{config_file}' not found.")
        except PermissionError:
            raise PermissionError(f"Can't access '{config_file}'.")

        for key in REQUIRED_KEYS:
            if key not in settings:
                raise ConfigError(f"Missing required key {key}.")
        try:
            width = int(settings['WIDTH'])
        except ValueError:
            raise ConfigError("Can't use type as width.")
        if width <= 0:
            raise ConfigError("Width must be a positive value.")
        try:
            height = int(settings['HEIGHT'])
        except ValueError:
            raise ConfigError("Can't use type as height.")
        if height <= 0:
            raise ConfigError("Height must be a positive value.")
        entry = settings['ENTRY'].split(',')
        if len(entry) != 2:
            raise ConfigError("Invalid syntax for entry, use: 'X,Y'")
        try:
            entry_point = (int(entry[0]), int(entry[1]))
        except ValueError:
            raise ConfigError("Invalid syntax for positions")
        exit_p = settings['EXIT'].split(',')
        if len(exit_p) != 2:
            raise ConfigError("Invalid syntax for exit, use: X,Y")
        try:
            exit_point = (int(exit_p[0]), int(exit_p[1]))
        except ValueError:
            raise ConfigError("Invalid syntax for positions")
        if settings['PERFECT'] not in ["True", "False"]:
            raise ConfigError("Perfect key must be either 'True' or 'False'.")
        if settings['PERFECT'] == "True":
            perfect = True
        elif settings['PERFECT'] == "False":
            perfect = False
        seed_str = settings.get('SEED')
        seed = None
        if seed_str:
            try:
                seed = int(seed_str)
            except ValueError:
                raise ConfigError("SEED must be an integer.")
        output_file = "maze.txt"
        if settings['OUTPUT_FILE']:
            output_file = settings['OUTPUT_FILE']

        #------------------------------------ position checker

        if not (0 <= entry_point[0] < width) or not (
            0 <= entry_point[1] < height
        ):
            raise ConfigError("Entry position out of bounds.")
        if not (0 <= exit_point[0] < width) or not (
            0 <= exit_point[1] < height
        ):
            raise ConfigError("Exit position out of bounds.")
        if entry_point[0] == exit_point[0] and entry_point[1] == exit_point[1]:
            raise ConfigError("Entry and Exit positions can't be equal.")
        
        return cls(width, height, entry_point, exit_point,
            output_file, perfect, seed)