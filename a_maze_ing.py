#!/usr/bin/env python3
"""Main module for the A-Maze-ing project.

Lida com a configuracao, interacao do utilizador e exportacao do labirinto.
"""

import sys
from typing import Dict, List, Tuple, Any


def parse_coordinates(coordinate_str: str) -> Tuple[int, int]:
    """Converte uma string 'x,y' numa tupla (x, y) de inteiros.

    Args:
        coordinate_str: String com as coordenadas separadas por virgula.

    Returns:
        Uma tupla de inteiros representando (x, y).
    """
    try:
        x_str, y_str = coordinate_str.split(",")
        return int(x_str.strip()), int(y_str.strip())
    except (ValueError, AttributeError):
        print(f"Aviso: coordenada invalida ({coordinate_str!r}), a usar (0,0).")
        return (0, 0)


def read_config(config_path: str) -> Dict[str, Any]:
    """Le o ficheiro de configuracao com tratamento de erros.

    Args:
        config_path: Caminho para o ficheiro de configuracao.

    Returns:
        Dicionario com as configuracoes carregadas e validadas.
    """
    config: Dict[str, Any] = {
        "WIDTH": 20,
        "HEIGHT": 15,
        "ENTRY": (0, 0),
        "EXIT": (19, 14),
        "OUTPUT_FILE": "maze.txt",
        "PERFECT": True,
    }

    try:
        with open(config_path, "r", encoding="utf-8") as file_handle:
            for line in file_handle:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip()
                    if key in ("WIDTH", "HEIGHT"):
                        config[key] = int(value)
                    elif key in ("ENTRY", "EXIT"):
                        config[key] = parse_coordinates(value)
                    elif key == "PERFECT":
                        config[key] = value.lower() in ("true", "1", "yes")
                    elif key == "OUTPUT_FILE":
                        config[key] = value
    except FileNotFoundError:
        print(f"Erro: Ficheiro de configuracao '{config_path}' ausente.")
        sys.exit(1)
    except Exception as error:
        print(f"Erro inesperado ao ler a configuracao: {error}")
        sys.exit(1)

    return config


def convert_path_to_directions(path: List[Tuple[int, int]]) -> str:
    """Converte lista de coordenadas numa string de direcoes N/E/S/W.

    Args:
        path: Lista de tuplas (linha, coluna) do caminho.

    Returns:
        String com N, E, S, W representando o caminho mais curto.
    """
    if not path or len(path) < 2:
        return ""

    directions: str = ""
    for (row1, col1), (row2, col2) in zip(path, path[1:]):
        if row2 < row1:
            directions += "N"
        elif row2 > row1:
            directions += "S"
        elif col2 > col1:
            directions += "E"
        elif col2 < col1:
            directions += "W"
    return directions


def export_maze(filepath: str, hex_grid: List[str], entry: Tuple[int, int],
                exit_coord: Tuple[int, int], path: List[Tuple[int, int]]
                ) -> None:
    """Exporta os dados do labirinto para ficheiro no formato exigido.

    Grava a grelha hexadecimal, uma linha em branco, entrada, saida
    e o caminho percorrido em letras direcionais.

    Args:
        filepath: Caminho do ficheiro de saida.
        hex_grid: Lista de strings (matriz em hexadecimal).
        entry: Coordenadas da entrada.
        exit_coord: Coordenadas da saida.
        path: Lista de coordenadas do caminho mais curto.
    """
    try:
        with open(filepath, "w", encoding="utf-8") as out_file:
            for row in hex_grid:
                out_file.write(row + "\n")
            
            out_file.write("\n")
            out_file.write(f"{entry[0]},{entry[1]}\n")
            out_file.write(f"{exit_coord[0]},{exit_coord[1]}\n")
            
            directions: str = convert_path_to_directions(path)
            out_file.write(directions + "\n")
            
        print(f"[Info] Labirinto exportado para '{filepath}'.")
    except Exception as error:
        print(f"Erro ao exportar o labirinto para '{filepath}': {error}")


def main() -> None:
    """Funcao principal que inicializa e corre o programa."""
    config_path: str = sys.argv[1] if len(sys.argv) > 1 else "config.txt"
    config: Dict[str, Any] = read_config(config_path)

    print(f"Configuracao carregada de '{config_path}'.")

    # Placeholder para testar a sua parte de exportacao sem o mazegen final
    mock_hex_grid: List[str] = ["9a3", "c56", "3a6"]
    mock_path: List[Tuple[int, int]] = [
        config["ENTRY"], (0, 1), (1, 1), config["EXIT"]
    ]

    # Substitua isto quando integrar com o codigo do Guilherme
    export_maze(
        filepath=config["OUTPUT_FILE"],
        hex_grid=mock_hex_grid,
        entry=config["ENTRY"],
        exit_coord=config["EXIT"],
        path=mock_path
    )

    while True:
        print("\n=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show / Hide the shortest path")
        print("3. Rotate the wall colours")
        print("4. Quit")
        
        try:
            choice: str = input("Choice? (1-4): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nA sair...")
            break

        if choice == "1":
            print("[Info] A regenerar o labirinto...")
        elif choice == "2":
            print("[Info] A alternar exibicao do caminho...")
        elif choice == "3":
            print("[Info] A alterar cores das paredes...")
        elif choice == "4":
            print("Adeus!")
            break
        else:
            print("Opcao invalida. Escolha entre 1 e 4.")


if __name__ == "__main__":
    main()
