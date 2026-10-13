"""Read and validate the application configuration."""

from mazegen import MazeGenerator

Point = tuple[int, int]


def parse_point(value: str, key: str) -> Point:
    """Parse a coordinate in x,y format."""
    parts = value.split(",")
    if len(parts) != 2:
        raise ValueError(f"{key} must use x,y format")
    try:
        return int(parts[0].strip()), int(parts[1].strip())
    except ValueError as error:
        raise ValueError(f"{key} must contain two integers") from error


def read_config(path: str) -> dict[str, str]:
    """Read KEY=VALUE lines and reject invalid settings."""
    allowed = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE",
               "PERFECT", "SEED"}
    config: dict[str, str] = {}
    try:
        with open(path, encoding="utf-8") as source:
            for number, raw in enumerate(source, 1):
                line = raw.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    raise ValueError(f"Line {number}: expected KEY=VALUE")
                key, value = (part.strip() for part in line.split("=", 1))
                if key not in allowed:
                    raise ValueError(
                        f"Line {number}: unknown key {key!r}")
                if key in config:
                    raise ValueError(f"Line {number}: duplicate key {key}")
                if not value:
                    raise ValueError(f"Line {number}: {key} cannot be empty")
                config[key] = value
    except OSError as error:
        raise ValueError(f"Could not read {path}: {error}") from error
    missing = allowed - {"SEED"} - config.keys()
    if missing:
        raise ValueError("Missing required keys: " +
                         ", ".join(sorted(missing)))
    return config


def make_generator(config: dict[str, str]) -> MazeGenerator:
    """Convert config text to validated generator settings."""
    try:
        width = int(config["WIDTH"])
        height = int(config["HEIGHT"])
        seed = int(config["SEED"]) if "SEED" in config else None
    except ValueError as error:
        raise ValueError("WIDTH, HEIGHT and SEED must be integers") from error
    if config["PERFECT"] not in ("True", "False"):
        raise ValueError("PERFECT must be True or False")
    return MazeGenerator(width, height, parse_point(config["ENTRY"], "ENTRY"),
                         parse_point(config["EXIT"], "EXIT"), seed,
                         config["PERFECT"] == "True")
