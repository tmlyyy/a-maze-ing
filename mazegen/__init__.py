"""Reusable maze generator.

Example::

    from mazegen import MazeGenerator
    maze = MazeGenerator(20, 15, (0, 0), (19, 14), seed=42)
    grid = maze.generate()  # grid[y][x], wall bits N=1 E=2 S=4 W=8
    path = maze.solve()     # list of (x, y), including both ends

Set perfect=True for a tree. Omit seed for a fresh random maze.
"""

from .generator import MazeGenerator

__all__ = ["MazeGenerator"]
