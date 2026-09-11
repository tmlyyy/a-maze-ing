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
    def __init__(self, width: int, height: int, entry: tuple[int, int],
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

    def generate(self) -> None:
        self.grid = self._init_grid()
        self._carve_perfect_maze()
        self._insert_42_pattern()
        if not self.perfect:
            sel._add_loops()
	
    def solve(self) -> list[str]:
        if self.grid is None:
            raise RuntimeError("Chame generate() antes de solve().")
        return bfs_shortest_path(self.grid, self.entry, self.exit)

    def get_structure(self) -> list[list[int]]:
        return self.grid

    def _init_grid(self):
        grid = [[NORTH | EAST | SOUTH | WEST for _ in range(self.width)]
                for _ in range(self.height)]
		
		for (x, y) in (self.entry, self.exit):
			if x == 0:
				grid[y][x] &= ~WEST
			elif x == self.width - 1:
				grid[y][x] &= ~EAST
			if y == 0:
				grid[y][x] &= ~NORTH
			elif y == self.height -1:
				grid[y][x] &= ~SOUTH

		return grid
        