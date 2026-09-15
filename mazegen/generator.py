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
    
    def _carve_perfect_maze(self)
	    visited = set()

        def carve(x, y):
            visited.add((x, y))
            directions = [NORTH, EAST, SOUTH, WEST]
            self._rng.shuffle(directions)

            for wall in directions:
                    dx, dy = DELTA[wall]
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height and (nx, ny) not in visited:
                        self.grid[y][x] &= ~wall
                        self.grid[ny][nx] &= ~OPPOSITE[wall]
                        carve(nx, ny)
	
	carve(*self.entry)

    def _insert_42_pattern(self):
		pattern_w = 7
		pattern_h = 5

		if self.width < pattern_w + 2 or self.height < pattern_h + 2:
			print("Erro: Labirinto pequeno demais para o padrão '42'.")
			return

		origin_x = (self.width - pattern_w) // 2
		origin_y = (self.height - pattern_h) // 2
	    

		closed_cells = self._get_42_shape(origin_x, origin_y)

		for (x, y) in closed_cells:
			self.grid[y][x] = NORTH | EAST | SOUTH | WEST
			
			for wall in (NORTH, EAST, SOUTH, WEST):
				dx = DELTA[wall]
				dy = DELTA[wall]
				nx = x + dx
				ny = y + dy
				if 0 <= nx < self.width and 0 < ny < self.height:
					self.grid[ny][nx] |= OPPOSITE[wall]

	def _add_loops(self):
		corners = [(0, 0), (self.width - 1, 0), (0, self.height - 1), (self.width - 1, self.height - 1)]
		center = (self.width // 2, self.height // 2)
		for (x, y) in corners + [center]:
			self._force_open(x, y)