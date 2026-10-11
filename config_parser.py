"""Read and validate the application configuration."""

from mazegen import MazeGenerator

Point = tuple[int, int]


def parse_point(value: str, key: str) -> Point:
    """Parse a coordinate in x,y format."""
    parts = value.split(",")
    if len(parts) != 2:
        raise ValueError(f"{key} deve ter formato x,y")
    try:
        return int(parts[0].strip()), int(parts[1].strip())
    except ValueError as error:
        raise ValueError(f"{key} deve conter dois inteiros") from error


def read_config(path: str) -> dict[str, str]:
    """Read required KEY=VALUE lines and reject malformed settings."""
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
                    raise ValueError(f"Linha {number}: esperado KEY=VALUE")
                key, value = (part.strip() for part in line.split("=", 1))
                if key not in allowed:
                    raise ValueError(
                        f"Linha {number}: chave desconhecida {key!r}")
                if key in config:
                    raise ValueError(f"Linha {number}: chave repetida {key}")
                if not value:
                    raise ValueError(f"Linha {number}: {key} esta vazio")
                config[key] = value
    except OSError as error:
        raise ValueError(f"Nao foi possivel ler {path}: {error}") from error
    missing = allowed - {"SEED"} - config.keys()
    if missing:
        raise ValueError("Faltam chaves obrigatorias: " +
                         ", ".join(sorted(missing)))
    return config


def make_generator(config: dict[str, str]) -> MazeGenerator:
    """Convert config strings to validated generator settings."""
    try:
        width = int(config["WIDTH"])
        height = int(config["HEIGHT"])
        seed = int(config["SEED"]) if "SEED" in config else None
    except ValueError as error:
        raise ValueError("WIDTH, HEIGHT e SEED devem ser inteiros") from error
    if config["PERFECT"] not in ("True", "False"):
        raise ValueError("PERFECT deve ser True ou False")
    return MazeGenerator(width, height, parse_point(config["ENTRY"], "ENTRY"),
                         parse_point(config["EXIT"], "EXIT"), seed,
                         config["PERFECT"] == "True")
