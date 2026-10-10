"""Find shortest routes in a wall-bit maze."""

from collections import deque

Point = tuple[int, int]
DIRECTIONS = ((1, 0, -1), (2, 1, 0), (4, 0, 1), (8, -1, 0))


def shortest_path(grid: list[list[int]], entry: Point,
                  exit: Point) -> list[Point]:
    """Return a shortest valid path, including entry and exit."""
    parents: dict[Point, Point | None] = {entry: None}
    queue = deque([entry])
    height = len(grid)
    width = len(grid[0])
    while queue:
        point = queue.popleft()
        if point == exit:
            break
        x, y = point
        for wall, dx, dy in DIRECTIONS:
            other = (x + dx, y + dy)
            if (not grid[y][x] & wall and
                    0 <= other[0] < width and 0 <= other[1] < height and
                    other not in parents):
                parents[other] = point
                queue.append(other)
    if exit not in parents:
        raise ValueError("Nao existe caminho entre ENTRY e EXIT")
    path = []
    current: Point | None = exit
    while current is not None:
        path.append(current)
        current = parents[current]
    path.reverse()
    return path
