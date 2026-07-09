class ConfigError(Exception):
    """Raised when the configuration file is invalid."""

REQUIRED_KEYS = ['WIDTH', 'HEIGHT', 'ENTRY', 'EXIT',
				 'OUTPUT_FILE', 'PERFECT']

class MazeConfig:
    def __init__(self) -> None:
        self.width: int | None = None
        self.height: int | None = None
        self.entry_point: tuple[int, int] | None = None
        self.exit_point: tuple[int, int] | None = None
        self.output_file: str | None = None
        self.perfect: bool | None = None
        self.seed: int | None = None

    def validate_parse(self, config_file: str) -> None:
        try:
            settings = {}
            with open(config_file, 'r') as raw:
                for line in raw:
                    if line.startswith('#'):
                        continue
                    if line.strip():
                        setting = line.split('=', 1)
                        settings[setting[0]] = setting[1].strip('\n')
        except FileNotFoundError:
            raise FileNotFoundError(f"'{config_file}' not found.")
        except PermissionError:
            raise PermissionError(f"Can't access '{config_file}'.")

        for key in REQUIRED_KEYS:
            if key not in settings:
                raise ValueError(f"Missing required key {key}.")
        try:
            self.width = int(settings['WIDTH'])
            if self.width <= 0:
                raise ValueError("Width must be a positive value.")
        except ValueError:
            raise ValueError("Can't use type as width.")
        try:
            self.height = int(settings['HEIGHT'])
            if self.height <= 0:
                raise ValueError("Height must be a positive value.")
        except ValueError:
            raise ValueError("Can't use type as height.")
        try:
            entry = settings['ENTRY'].split(',')
            if len(entry) != 2:
                raise ValueError("Invalid syntax for entry, use: 'X,Y'")
        except ValueError:
            raise ValueError("Impossible to use value as entry point.")
        try:
            self.entry_point = (int(entry[0]), int(entry[1]))
        except ValueError:
            raise ValueError("Invalid syntax for positions")
        try:
            exit_p = settings['EXIT'].split(',')
            if len(exit_p) != 2:
                raise ValueError("Invalid syntax for exit, use: X,Y")
        except ValueError:
            raise ValueError("Impossible to use value as exit point.")
        try:
            self.exit_point = (int(exit_p[0]), int(exit_p[1]))
        except ValueError:
            raise ValueError("Invalid syntax for positions")
        if settings['PERFECT'] not in ["True", "False"]:
            raise ValueError("Perfect key must be either 'True' or 'False'.")
        if settings['PERFECT'] == "True":
            self.perfect = True
        elif settings['PERFECT'] == "False":
            self.perfect = False
        try:
            if settings['SEED']:
                self.seed = int(settings['SEED'])
        except ValueError:
            raise ValueError("Seed syntax incorrect, must be an int.")

        #------------------------------------ position checker

        if not (0 <= self.entry_point[0] < self.width) or not (
            0 <= self.entry_point[1] < self.height
        ):
            raise ValueError("Entry position out of bounds.")
        if not (0 <= self.exit_point[0] < self.width) or not (
            0 <= self.exit_point[1] < self.height
        ):
            raise ValueError("Exit position out of bounds.")
        if self.entry_point[0] == self.exit_point[0] and self.entry_point[1] == self.exit_point[1]:
            raise ValueError("Entry and Exit positions can't be equal.")