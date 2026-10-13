"""Reusable maze generator.

Example::

    from mazegen import MazeGenerator
    maze = MazeGenerator(20, 15, (0, 0), (19, 14), seed=42)
    grid = maze.generate()
    path = maze.solve()

Set perfect=True for a tree. Omit seed for a fresh random maze.
"""

from .generator import MazeGenerator

__all__ = ["MazeGenerator"]
