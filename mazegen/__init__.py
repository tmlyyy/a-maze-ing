"""
mazegen - Gerador e solucionador de labirintos reutilizável.

uso basico:
    from mazegen import MazeGenerator

    maze = MazeGenerator(width=20, height=15, seed=42)
    maze.generate()
    solution = maze.solve()
"""

from .generator import MazeGenerator

__all__ = ["MazeGenerator"]
__version__ = "1.0.0"
