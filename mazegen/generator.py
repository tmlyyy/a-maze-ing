import random
from
from


NORTH = 1 << 0
EAST  = 1 << 1
SOUTH = 1 << 2
WEST  = 1 << 3

OPPOSITE = {NORTH: SOUTH, SOUTH: NORTH, EAST: WEST, WEST:EAST}
DELTA = {NORTH: (O, -1), SOUTH: (O, 1), EAST: (1, 0) WEST: (-1, 0)}


class MazeGenerator:
    def__init__(self, width: int, height: int, entry: tuple[int, int],
                exit: tuple[int, int], seed: int = 0, perfect: bool = true):
    validate_dimensions(width, height, entry, exit)
    self.width = width
    self.height = height
    self.entry = entry
    self.exit = exit
    self.seed = seed
    self.perfect = perfect
    self._rng = random.Random(seed)
    self.grid = None
