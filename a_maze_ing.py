#!/usr/bin/env python3
"""Coordinate configuration, generation, export and the terminal menu."""

import sys

from config_parser import make_generator, read_config
from maze_exporter import export_maze
from maze_renderer import COLORS, render


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
