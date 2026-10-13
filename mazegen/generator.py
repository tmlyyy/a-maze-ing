"""Generate connected mazes with an iterative depth-first search."""

import random
from typing import Optional

from .solver import shortest_path

Point = tuple[int, int]
N, E, S, W = 1, 2, 4, 8
DIRECTIONS = ((N, 0, -1, S), (E, 1, 0, W),
              (S, 0, 1, N), (W, -1, 0, E))
DIGITS = ("#..#.###", "#..#...#", "####.###", "...#.#..",
          "...#.###")


class MazeGenerator:
    """Build a maze; cells use wall bits N=1, E=2, S=4, W=8.

    Coordinates are always (x, y), with cells accessed through grid[y][x].
    Call generate(), then read grid or call solve().
    A seed makes output repeatable.
    """

    def __init__(self, width: int, height: int, entry: Point,
                 exit: Point, seed: Optional[int] = None,
                 perfect: bool = False) -> None:
        """Validate dimensions and save generation options."""
        if not isinstance(width, int) or isinstance(width, bool) or width < 2:
            raise ValueError("WIDTH must be an integer of at least 2")
        if (not isinstance(height, int) or isinstance(height, bool) or
                height < 2):
            raise ValueError("HEIGHT must be an integer of at least 2")
        for name, point in (("ENTRY", entry), ("EXIT", exit)):
            if (not isinstance(point, tuple) or len(point) != 2 or
                    any(not isinstance(v, int) or isinstance(v, bool)
                        for v in point) or
                    not (0 <= point[0] < width and 0 <= point[1] < height)):
                raise ValueError(f"{name} must be inside the maze")
        if entry == exit:
            raise ValueError("ENTRY and EXIT must be different")
        if seed is not None and (not isinstance(seed, int) or
                                 isinstance(seed, bool)):
            raise ValueError("SEED must be an integer")
        if not isinstance(perfect, bool):
            raise ValueError("PERFECT must be True or False")
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.seed = seed
        self.perfect = perfect
        self.grid: list[list[int]] = []
        self.pattern: set[Point] = set()
        self._rng = random.Random(seed)

    def _inside(self, x: int, y: int) -> bool:
        """Return whether coordinates are inside the board."""
        return 0 <= x < self.width and 0 <= y < self.height

    def _neighbors(self, x: int, y: int) -> list[tuple[int, Point, int]]:
        """Return adjacent available cells and both wall bits."""
        return [(wall, (x + dx, y + dy), opposite)
                for wall, dx, dy, opposite in DIRECTIONS
                if self._inside(x + dx, y + dy)
                and (x + dx, y + dy) not in self.pattern]

    def _connected_shape(self, blocked: set[Point]) -> bool:
        """Check connectivity before placing the closed 42 cells."""
        start = self.entry
        seen = {start}
        pending = [start]
        while pending:
            x, y = pending.pop()
            for _, dx, dy, _ in DIRECTIONS:
                other = (x + dx, y + dy)
                if (self._inside(*other) and other not in blocked and
                        other not in seen):
                    seen.add(other)
                    pending.append(other)
        return len(seen) == self.width * self.height - len(blocked)

    def _choose_pattern(self) -> set[Point]:
        """Place a centered 42 when it fits without cutting corridors."""
        pattern_width = len(DIGITS[0])
        pattern_height = len(DIGITS)
        if (self.width < pattern_width + 2 or
                self.height < pattern_height + 2):
            return set()
        center = (self.width // 2, self.height // 2)
        required = {self.entry, self.exit}
        if not self.perfect:
            required |= {(0, 0), (self.width - 1, 0),
                         (0, self.height - 1),
                         (self.width - 1, self.height - 1), center}
        positions = [(x, y)
                     for y in range(1, self.height - pattern_height)
                     for x in range(1, self.width - pattern_width)]
        positions.sort(key=lambda p: (
            abs(p[0] + pattern_width // 2 - center[0]) +
            abs(p[1] + pattern_height // 2 - center[1]),
            p[1], p[0]))
        for ox, oy in positions:
            blocked = {(ox + x, oy + y)
                       for y, row in enumerate(DIGITS)
                       for x, char in enumerate(row) if char == "#"}
            if not (blocked & required) and self._connected_shape(blocked):
                return blocked
        return set()

    def _open(self, point: Point, other: Point, wall: int,
              opposite: int) -> None:
        """Remove one shared wall from both cells."""
        x, y = point
        nx, ny = other
        self.grid[y][x] &= ~wall
        self.grid[ny][nx] &= ~opposite

    def _carve_tree(self) -> None:
        """Visit each corridor once using an explicit DFS stack."""
        seen = {self.entry}
        stack = [self.entry]
        while stack:
            point = stack[-1]
            choices = [(wall, other, opposite)
                       for wall, other, opposite in self._neighbors(*point)
                       if other not in seen]
            if not choices:
                stack.pop()
                continue
            wall, other, opposite = self._rng.choice(choices)
            self._open(point, other, wall, opposite)
            seen.add(other)
            stack.append(other)
        if len(seen) != self.width * self.height - len(self.pattern):
            raise ValueError("Could not connect all corridors")

    def _degree(self, point: Point) -> int:
        """Count open passages around a corridor."""
        x, y = point
        return sum(not (self.grid[y][x] & wall)
                   for wall, _, _ in self._neighbors(x, y))

    def _large_open_area(self) -> bool:
        """Detect a completely open three by three square."""
        for y in range(self.height - 2):
            for x in range(self.width - 2):
                if any((x + dx, y + dy) in self.pattern
                       for dy in range(3) for dx in range(3)):
                    continue
                if all(not (self.grid[y + dy][x + dx] & E)
                       for dy in range(3) for dx in range(2)) and all(
                        not (self.grid[y + dy][x + dx] & S)
                        for dy in range(2) for dx in range(3)):
                    return True
        return False

    def _try_open(self, point: Point, wall: int, other: Point,
                  opposite: int) -> bool:
        """Open a wall only if it does not create a wide open square."""
        x, y = point
        nx, ny = other
        if not self.grid[y][x] & wall:
            return False
        self._open(point, other, wall, opposite)
        if self._large_open_area():
            self.grid[y][x] |= wall
            self.grid[ny][nx] |= opposite
            return False
        return True

    def _add_routes(self) -> None:
        """Reduce dead ends and add independent routes for Pac-Man mode."""
        corridors = [(x, y) for y in range(self.height)
                     for x in range(self.width)
                     if (x, y) not in self.pattern]
        self._rng.shuffle(corridors)
        extra = 0
        for point in corridors:
            if self._degree(point) != 1:
                continue
            choices = self._neighbors(*point)
            self._rng.shuffle(choices)
            for wall, other, opposite in choices:
                if self._try_open(point, wall, other, opposite):
                    extra += 1
                    break
        edges = [(point, wall, other, opposite)
                 for point in corridors
                 for wall, other, opposite in self._neighbors(*point)
                 if wall in (E, S)]
        self._rng.shuffle(edges)
        target = max(2, len(corridors) // 8)
        for point, wall, other, opposite in edges:
            if extra >= target:
                break
            if self._try_open(point, wall, other, opposite):
                extra += 1
        if extra < 2:
            raise ValueError(
                "Maze dimensions are too small for two loops in default mode")

    def generate(self) -> list[list[int]]:
        """Generate and return the wall matrix."""
        self._rng = random.Random(self.seed)
        self.grid = [[15 for _ in range(self.width)]
                     for _ in range(self.height)]
        self.pattern = self._choose_pattern()
        self._carve_tree()
        if not self.perfect:
            self._add_routes()
        return self.grid

    def solve(self) -> list[Point]:
        """Return the shortest entry-to-exit path using BFS."""
        if not self.grid:
            raise ValueError("Call generate() before solve()")
        return shortest_path(self.grid, self.entry, self.exit)

    def get_structure(self) -> list[list[int]]:
        """Return the generated wall matrix."""
        if not self.grid:
            raise ValueError("Call generate() before get_structure()")
        return self.grid
