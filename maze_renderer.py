"""Render the terminal interface without changing maze data."""

import os
import sys

from mazegen import MazeGenerator

Point = tuple[int, int]
COLORS = ("\033[38;2;230;234;241m", "\033[38;2;245;115;125m",
          "\033[38;2;120;175;255m", "\033[38;2;240;145;210m")
RESET = "\033[0m"
# Junctions use the same N/E/S/W bits as the maze walls.
GLYPHS = " ╹╺┗╻┃┏┣╸┛━┻┓┫┳╋"
HIGHLIGHTS = ("\033[38;2;250;252;255m", "\033[38;2;255;205;210m",
              "\033[38;2;203;224;255m", "\033[38;2;255;211;243m")
ENTRY_COLOR = "\033[38;2;74;222;128m"
EXIT_COLOR = "\033[38;2;255;90;90m"


def render(maze: MazeGenerator, solution: list[Point],
           show_path: bool, color: int) -> str:
    """Draw firm walls and light circles for the route and 42 cells."""
    terminal = (sys.stdout.isatty()
                and os.environ.get("TERM") not in ("dumb", "unknown")
                and "NO_COLOR" not in os.environ)
    unicode = terminal and "utf" in (sys.stdout.encoding or "").lower()
    width, height = maze.width * 4 + 1, maze.height * 2 + 1
    walls = [[0] * width for _ in range(height)]
    route = [[0] * width for _ in range(height)]

    def connect(layer: list[list[int]], ax: int, ay: int,
                bx: int, by: int) -> None:
        """Join screen positions horizontally or vertically."""
        dx = (bx > ax) - (bx < ax)
        dy = (by > ay) - (by < ay)
        forward, backward = {(1, 0): (2, 8), (-1, 0): (8, 2),
                             (0, 1): (4, 1), (0, -1): (1, 4)}[(dx, dy)]
        while (ax, ay) != (bx, by):
            layer[ay][ax] |= forward
            ax, ay = ax + dx, ay + dy
            layer[ay][ax] |= backward

    for y in range(maze.height):
        for x in range(maze.width):
            # Reserved cells use three circles instead of a wall box.
            if (x, y) in maze.pattern:
                continue
            cell = maze.grid[y][x]
            left, top = x * 4, y * 2
            for bit, ax, ay, bx, by in (
                    (1, left, top, left + 4, top),
                    (2, left + 4, top, left + 4, top + 2),
                    (4, left, top + 2, left + 4, top + 2),
                    (8, left, top, left, top + 2)):
                if cell & bit:
                    connect(walls, ax, ay, bx, by)

    if show_path:
        steps = {(0, -1): 1, (1, 0): 2, (0, 1): 4, (-1, 0): 8}
        for (ax, ay), (bx, by) in zip(solution, solution[1:]):
            step_bit = steps.get((bx - ax, by - ay))
            if (step_bit is not None and not maze.grid[ay][ax] & step_bit
                    and (ax, ay) not in maze.pattern
                    and (bx, by) not in maze.pattern):
                connect(route, ax * 4 + 2, ay * 2 + 1,
                        bx * 4 + 2, by * 2 + 1)

    lines = []
    for row in range(height):
        line = ""
        previous = ""
        for column in range(width):
            wall_bits, path_bits = walls[row][column], route[row][column]
            mask = path_bits or wall_bits
            char = GLYPHS[mask] if unicode else (
                "+" if mask & 5 and mask & 10 else
                "|" if mask & 5 else "-" if mask else " ")
            if path_bits:
                # Terminal characters are taller than they are wide:
                # one dot every two columns keeps both directions balanced.
                char = ("●" if unicode else ".") if column % 2 == 0 else " "
            style = HIGHLIGHTS[color] if path_bits else COLORS[color]
            if row % 2 == 1 and column % 4 in (1, 2, 3):
                point = (column // 4, row // 2)
                if point in maze.pattern:
                    char, style = ("●" if unicode else "o"), HIGHLIGHTS[color]
                if column % 4 == 2 and point == maze.entry:
                    char, style = ("●" if unicode else "E"), ENTRY_COLOR
                elif column % 4 == 2 and point == maze.exit:
                    char, style = ("●" if unicode else "X"), EXIT_COLOR
            if terminal and style != previous:
                line += RESET + style
                previous = style
            line += char
        lines.append(line + RESET if terminal else line)
    legend = (ENTRY_COLOR + "●" + RESET + " verde = entrada | " +
              EXIT_COLOR + "●" + RESET + " vermelho = saída" if unicode else
              "E = entrada | X = saida")
    return "\n".join(lines + [legend])
