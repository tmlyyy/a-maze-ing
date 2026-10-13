"""Export a maze and its shortest route to the subject format."""

from pathlib import Path

from mazegen import MazeGenerator

Point = tuple[int, int]


def directions(path: list[Point]) -> str:
    """Encode successive path steps as N, E, S, or W."""
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
            f"Could not write {path}: {error}") from error
