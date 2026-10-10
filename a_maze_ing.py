#!/usr/bin/env python3
"""Load a maze configuration, show the maze, and export its solution."""

import sys
from pathlib import Path

from mazegen import MazeGenerator

Point = tuple[int, int]
COLORS = ("\033[37m", "\033[36m", "\033[33m", "\033[35m")
RESET = "\033[0m"


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


def directions(path: list[Point]) -> str:
    """Encode successive path steps as N, E, S, W."""
    moves = {(0, -1): "N", (1, 0): "E", (0, 1): "S", (-1, 0): "W"}
    return "".join(moves[(bx - ax, by - ay)]
                   for (ax, ay), (bx, by) in zip(path, path[1:]))


def export_maze(path: str, maze: MazeGenerator,
                solution: list[Point]) -> None:
    """Write hex rows, a blank line, coordinates, and shortest moves."""
    lines = ["".join(f"{cell:X}" for cell in row) for row in maze.grid]
    lines += ["", f"{maze.entry[0]},{maze.entry[1]}",
              f"{maze.exit[0]},{maze.exit[1]}", directions(solution)]
    try:
        Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")
    except OSError as error:
        raise ValueError(
            f"Nao foi possivel escrever {path}: {error}") from error


def render(maze: MazeGenerator, solution: list[Point],
           show_path: bool, color: int) -> str:
    """Draw every wall and mark entry, exit, 42, and optional solution."""
    points = set(solution) if show_path else set()
    rows: list[str] = []
    for y in range(maze.height):
        top = ""
        middle = ""
        for x in range(maze.width):
            cell = maze.grid[y][x]
            top += "+" + ("---" if cell & 1 else "   ")
            if (x, y) == maze.entry:
                mark = " E "
            elif (x, y) == maze.exit:
                mark = " X "
            elif (x, y) in maze.pattern:
                mark = "###"
            elif (x, y) in points:
                mark = " . "
            else:
                mark = "   "
            middle += ("|" if cell & 8 else " ") + mark
        rows.append(top + "+")
        rows.append(middle + ("|" if maze.grid[y][-1] & 2 else " "))
    rows.append("+" + "---+" * maze.width)
    drawing = "\n".join(rows)
    if sys.stdout.isatty():
        for symbol in ("+", "-", "|"):
            drawing = drawing.replace(symbol, COLORS[color] + symbol + RESET)
    return drawing


def run(config_path: str) -> None:
    """Generate, export, and handle the terminal menu."""
    config = read_config(config_path)
    maze = make_generator(config)
    maze.generate()
    if not maze.pattern:
        print("Erro: tamanho/posicao insuficiente para desenhar 42; "
              "labirinto gerado sem o padrao.")
    solution = maze.solve()
    export_maze(config["OUTPUT_FILE"], maze, solution)
    show_path = True
    color = 0
    print(render(maze, solution, show_path, color))
    print(f"Arquivo salvo: {config['OUTPUT_FILE']}")
    while True:
        print("\n1 Gerar novamente | 2 Mostrar/ocultar caminho | "
              "3 Trocar cor das paredes | 4 Sair")
        try:
            choice = input("Opcao: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAte logo!")
            return
        if choice == "1":
            # A configured seed repeats; a new random seed gives a new maze.
            maze.seed = None
            maze.generate()
            solution = maze.solve()
            export_maze(config["OUTPUT_FILE"], maze, solution)
            print(render(maze, solution, show_path, color))
            print(f"Arquivo salvo: {config['OUTPUT_FILE']}")
        elif choice == "2":
            show_path = not show_path
            print(render(maze, solution, show_path, color))
        elif choice == "3":
            color = (color + 1) % len(COLORS)
            print(f"Cor das paredes: {color + 1}/{len(COLORS)}")
            print(render(maze, solution, show_path, color))
        elif choice == "4":
            print("Ate logo!")
            return
        else:
            print("Opcao invalida; escolha de 1 a 4.")


def main() -> int:
    """Report user-facing errors without a traceback."""
    if len(sys.argv) != 2:
        print("Uso: python3 a_maze_ing.py config.txt", file=sys.stderr)
        return 1
    try:
        run(sys.argv[1])
    except (ValueError, OSError) as error:
        print(f"Erro: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
