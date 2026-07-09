"""Config parsing for A-Maze-ing."""


class ConfigError(Exception):
    """Raised when the configuration file is invalid."""


REQUIRED_KEYS = ("WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT")


class Config:
    def __init__(self):
        self.width = None
        self.height = None
        self.entry = None
        self.exit = None
        self.output_file = None
        self.perfect = False
        self.seed = None
        self.extra = {}

    @staticmethod
    def _parse_bool(value, key):
        v = value.strip().lower()
        if v in ("true", "1", "yes"):
            return True
        if v in ("false", "0", "no"):
            return False
        raise ConfigError(f"Invalid boolean value for {key}: '{value}'")

    @staticmethod
    def _parse_coord(value, key):
        parts = value.split(",")
        if len(parts) != 2:
            raise ConfigError(
                f"Invalid coordinate for {key}: '{value}' (expected 'x,y')"
            )
        try:
            x, y = int(parts[0].strip()), int(parts[1].strip())
        except ValueError:
            raise ConfigError(f"Invalid coordinate for {key}: '{value}' (not integers)")
        return x, y

    @classmethod
    def from_file(cls, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except FileNotFoundError:
            raise ConfigError(f"Configuration file not found: '{path}'")
        except OSError as e:
            raise ConfigError(f"Could not read configuration file '{path}': {e}")

        raw = {}
        for lineno, raw_line in enumerate(lines, start=1):
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                raise ConfigError(
                    f"Syntax error on line {lineno}: expected 'KEY=VALUE', got '{line}'"
                )
            key, _, value = line.partition("=")
            key = key.strip().upper()
            value = value.strip()
            if not key:
                raise ConfigError(f"Syntax error on line {lineno}: missing key")
            raw[key] = value

        for key in REQUIRED_KEYS:
            if key not in raw:
                raise ConfigError(f"Missing mandatory key: {key}")

        cfg = cls()

        try:
            cfg.width = int(raw["WIDTH"])
        except ValueError:
            raise ConfigError(f"WIDTH must be an integer, got '{raw['WIDTH']}'")
        try:
            cfg.height = int(raw["HEIGHT"])
        except ValueError:
            raise ConfigError(f"HEIGHT must be an integer, got '{raw['HEIGHT']}'")

        if cfg.width < 5 or cfg.height < 5:
            raise ConfigError(
                "WIDTH and HEIGHT must be at least 5 to produce a valid maze"
            )
        if cfg.width > 500 or cfg.height > 500:
            raise ConfigError("WIDTH and HEIGHT must be at most 500")

        cfg.entry = cls._parse_coord(raw["ENTRY"], "ENTRY")
        cfg.exit = cls._parse_coord(raw["EXIT"], "EXIT")

        for name, (x, y) in (("ENTRY", cfg.entry), ("EXIT", cfg.exit)):
            if not (0 <= x < cfg.width and 0 <= y < cfg.height):
                raise ConfigError(
                    f"{name} coordinates {(x, y)} are outside the maze bounds "
                    f"(0..{cfg.width - 1}, 0..{cfg.height - 1})"
                )

        if cfg.entry == cfg.exit:
            raise ConfigError("ENTRY and EXIT must be different cells")

        cfg.output_file = raw["OUTPUT_FILE"]
        if not cfg.output_file:
            raise ConfigError("OUTPUT_FILE cannot be empty")

        cfg.perfect = cls._parse_bool(raw["PERFECT"], "PERFECT")

        if "SEED" in raw:
            try:
                cfg.seed = int(raw["SEED"])
            except ValueError:
                raise ConfigError(f"SEED must be an integer, got '{raw['SEED']}'")

        handled = set(REQUIRED_KEYS) | {"SEED"}
        cfg.extra = {k: v for k, v in raw.items() if k not in handled}

        return cfg
