from __future__ import annotations

NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8

COLOR_WALL = "\033[1;34m"
COLOR_PATH = "\033[1;32m"
COLOR_RESET = "\033[0m"

# Dados fictícios do contrato, usados enquanto o mazegen real não
# estiver funcional (ver plano-projeto-amazeing.md).
TEST_GRID: list[list[int]] = [
    [9, 5, 12],
    [10, 15, 10],
    [3, 5, 6],
]
TEST_PATH: set[tuple[int, int]] = {
    (0, 0), (0, 1), (0, 2), (1, 2), (2, 2),
}


def read_config(path: str) -> dict[str, str]:
    """Lê o arquivo de configuração e retorna um dicionário.

    Ignora comentários (#) e linhas em branco. Nunca quebra o
    programa: em caso de erro, avisa e retorna um dicionário vazio.
    """
    config: dict[str, str] = {}
    try:
        with open(path, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    print(f"Aviso: linha {line_number} ignorada: "
                          f"{line!r}")
                    continue
                key, _, value = line.partition("=")
                config[key.strip().upper()] = value.strip()
    except FileNotFoundError:
        print(f"Erro: arquivo '{path}' não encontrado.")
    except OSError as error:
        print(f"Erro ao ler '{path}': {error}")
    return config


def render_maze(
    grid: list[list[int]],
    path: set[tuple[int, int]] | None = None,
) -> None:
    """Desenha o labirinto no terminal com blocos e cores ANSI."""
    if path is None:
        path = set()

    width = len(grid[0])

    top = "██"
    for col in range(width):
        top += "██" if grid[0][col] & NORTH else "  "
    top += "██"
    print(f"{COLOR_WALL}{top}{COLOR_RESET}")

    for row, cells in enumerate(grid):
        body = "██" if cells[0] & WEST else "  "
        floor = "██"

        for col, cell in enumerate(cells):
            if (row, col) in path:
                body += (f"{COLOR_RESET}{COLOR_PATH}••"
                         f"{COLOR_RESET}{COLOR_WALL}")
            else:
                body += "  "
            body += "██" if cell & EAST else "  "
            floor += "██" if cell & SOUTH else "  "

        floor += "██"
        print(f"{COLOR_WALL}{body}{COLOR_RESET}")
        print(f"{COLOR_WALL}{floor}{COLOR_RESET}")


def export_hex(grid: list[list[int]], path: str) -> bool:
    """Exporta a matriz do labirinto para um arquivo hexadecimal.

    Cada célula (valor de 0 a 15) vira um único dígito hexadecimal
    (0-F). Retorna True se salvou com sucesso, False se deu erro.
    """
    try:
        with open(path, "w", encoding="utf-8") as file:
            for row in grid:
                line = "".join(f"{cell:X}" for cell in row)
                file.write(line + "\n")
        return True
    except OSError as error:
        print(f"Erro ao exportar para '{path}': {error}")
        return False


def main() -> None:
    """Lê a config e roda o menu interativo do labirinto."""
    config = read_config("config.txt")
    out_file = config.get("OUT_FILE", "maze.txt")

    grid = TEST_GRID
    path = TEST_PATH
    showing_path = False

    while True:
        render_maze(grid, path if showing_path else None)
        print("\n[R] Regenerar  [P] Mostrar caminho  "
              "[C] Config  [Q] Sair")
        choice = input("Escolha uma opção: ").strip().upper()

        if choice == "R":
            showing_path = False
        elif choice == "P":
            showing_path = True
        elif choice == "C":
            for key, value in config.items():
                print(f"{key} = {value}")
        elif choice == "Q":
            if export_hex(grid, out_file):
                print(f"Labirinto salvo em '{out_file}'.")
            print("Até logo!")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
