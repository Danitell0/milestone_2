class ConfigError(Exception):
    """Raised when the configuration file is invalid."""


REQUIRED_KEYS = ['WIDTH', 'HEIGHT', 'ENTRY', 'EXIT',
                 'OUTPUT_FILE', 'PERFECT']


class MazeConfig:
    """Holds and validates the settings for one maze generation run.

    Created empty, the populated by ``validate_parse`` from a
    ``KEY=VALUE`` config file. All fields start at None so unparsed
    state is detectable.

    Attributes:
        width: Maze width in cells
        height: Maze height in cells
        entry_point: (x,y) of the entry cell
        exit_point: (x,y) of the exit cell
        output_file: Path the generated maze is written to
        perfect: True for a perfect maze without loops
                False for a pac-man like maze
        seed: seed for reproducible mazes or None to generate a random one
    """

    def __init__(self) -> None:
        """Create an unpopulated config with all fields unset."""
        self.width: int | None = None
        self.height: int | None = None
        self.entry_point: tuple[int, int] | None = None
        self.exit_point: tuple[int, int] | None = None
        self.output_file: str | None = None
        self.perfect: bool | None = None
        self.seed: int | None = None

    def validate_parse(self, config_file: str) -> None:
        """Read, parse and validate a config file into the instance.

        Reads ``KEY=VALUE`` lines and converts each value to its proper type.

        Args:
            config_file: Path to the configuration file to read

        Raises:
            FileNotFoundError: If the config file does not exist
            PermissionError: If the config file cannot be read
            ConfigError: If a required key is missing, a value has the
                wrong type or format or the entry/exit are invalid

        Returns:
            None. Populates this instance's attributes
        """
        try:
            settings = {}
            with open(config_file, 'r') as raw:
                for line in raw:
                    if line.startswith('#'):
                        continue
                    if line.strip():
                        try:
                            setting = line.split('=', 1)
                            if len(setting) != 2:
                                raise ConfigError(
                                    "Invalid syntax use: 'KEY=VALUE'")
                            settings[setting[0]] = setting[1].strip('\n')
                        except ValueError:
                            raise ConfigError(
                                "Invalid syntax use: 'KEY=VALUE'")
        except FileNotFoundError:
            raise FileNotFoundError(f"'{config_file}' not found.")
        except PermissionError:
            raise PermissionError(f"Can't access '{config_file}'.")

        for key in REQUIRED_KEYS:
            if key not in settings:
                raise ConfigError(f"Missing required key {key}.")
        try:
            self.width = int(settings['WIDTH'])
            if self.width <= 0:
                raise ConfigError("Width must be a positive value.")
        except ValueError:
            raise ConfigError("Can't use type as width.")
        try:
            self.height = int(settings['HEIGHT'])
            if self.height <= 0:
                raise ConfigError("Height must be a positive value.")
        except ValueError:
            raise ConfigError("Can't use type as height.")
        try:
            entry = settings['ENTRY'].split(',')
            if len(entry) != 2:
                raise ConfigError("Invalid syntax for entry, use: 'X,Y'")
        except ValueError:
            raise ConfigError("Impossible to use value as entry point.")
        try:
            self.entry_point = (int(entry[0]), int(entry[1]))
        except ValueError:
            raise ConfigError("Invalid syntax for positions")
        try:
            exit_p = settings['EXIT'].split(',')
            if len(exit_p) != 2:
                raise ConfigError("Invalid syntax for exit, use: X,Y")
        except ValueError:
            raise ConfigError("Impossible to use value as exit point.")
        try:
            self.exit_point = (int(exit_p[0]), int(exit_p[1]))
        except ValueError:
            raise ConfigError("Invalid syntax for positions")
        if settings['PERFECT'] not in ["True", "False"]:
            raise ConfigError("Perfect key must be either 'True' or 'False'.")
        if settings['PERFECT'] == "True":
            self.perfect = True
        elif settings['PERFECT'] == "False":
            self.perfect = False
        if 'SEED' in settings:
            if settings['SEED']:
                try:
                    self.seed = int(settings['SEED'])
                except ValueError:
                    raise ConfigError("Seed syntax incorrect, must be an int.")
        try:
            if settings['OUTPUT_FILE']:
                self.output_file = (settings['OUTPUT_FILE'])
        except ValueError:
            raise ConfigError("Output_File syntax incorrect, must be an str.")

#   ------------------------------------ position checker

        if not (0 <= self.entry_point[0] < self.width) or not (
            0 <= self.entry_point[1] < self.height
        ):
            raise ConfigError("Entry position out of bounds.")
        if not (0 <= self.exit_point[0] < self.width) or not (
            0 <= self.exit_point[1] < self.height
        ):
            raise ConfigError("Exit position out of bounds.")
        # checking if entry == exit
        if self.entry_point[
            0] == self.exit_point[
                0] and self.entry_point[
                    1] == self.exit_point[1]:
            raise ConfigError("Entry and Exit positions can't be equal.")
