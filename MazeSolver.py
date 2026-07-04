import random
from collections import deque
import heapq


def generate_maze(rows, cols, wall_chance=0.25, seed=None):
    if seed is not None:
        random.seed(seed)

    start = (0, 0)
    end = (rows - 1, cols - 1)

    while True:
        grid = []
        for r in range(rows):
            row = []
            for c in range(cols):
                if (r, c) == start or (r, c) == end:
                    row.append(0)
                elif random.random() < wall_chance:
                    row.append(1)
                else:
                    row.append(0)
            grid.append(row)

        if path_exists(grid, start, end):
            return grid, start, end


def path_exists(grid, start, end):
    visited = set()
    visited.add(start)
    queue = deque([start])

    while queue:
        current = queue.popleft()
        if current == end:
            return True
        for n in get_neighbors(grid, current):
            if n not in visited:
                visited.add(n)
                queue.append(n)
    return False


def get_neighbors(grid, pos):
    rows = len(grid)
    cols = len(grid[0])
    r, c = pos
    moves = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]

    neighbors = []
    for m in moves:
        mr, mc = m
        if 0 <= mr < rows and 0 <= mc < cols:
            if grid[mr][mc] == 0:
                neighbors.append(m)
    return neighbors


def rebuild_path(came_from, end):
    path = [end]
    while path[-1] in came_from:
        path.append(came_from[path[-1]])
    path.reverse()
    return path


def bfs(grid, start, end):
    queue = deque([start])
    came_from = {}
    visited = {start}

    while queue:
        current = queue.popleft()

        if current == end:
            return rebuild_path(came_from, end)

        for n in get_neighbors(grid, current):
            if n not in visited:
                visited.add(n)
                came_from[n] = current
                queue.append(n)

    return None


def dfs(grid, start, end):
    stack = [start]
    came_from = {}
    visited = {start}

    while stack:
        current = stack.pop()

        if current == end:
            return rebuild_path(came_from, end)

        for n in get_neighbors(grid, current):
            if n not in visited:
                visited.add(n)
                came_from[n] = current
                stack.append(n)

    return None


def heuristic(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])


def astar(grid, start, end):
    frontier = [(0, start)]
    came_from = {}
    cost_so_far = {start: 0}

    while frontier:
        current_priority, current = heapq.heappop(frontier)

        if current == end:
            return rebuild_path(came_from, end)

        for n in get_neighbors(grid, current):
            new_cost = cost_so_far[current] + 1
            if n not in cost_so_far or new_cost < cost_so_far[n]:
                cost_so_far[n] = new_cost
                priority = new_cost + heuristic(n, end)
                heapq.heappush(frontier, (priority, n))
                came_from[n] = current

    return None


def print_maze(grid, start, end, path=None):
    if path is None:
        path = []
    path = set(path)

    for r in range(len(grid)):
        line = ""
        for c in range(len(grid[0])):
            pos = (r, c)
            if pos == start:
                line += "S"
            elif pos == end:
                line += "E"
            elif pos in path:
                line += "*"
            elif grid[r][c] == 1:
                line += "#"
            else:
                line += "."
        print(line)


def main():
    rows = 10
    cols = 15
    grid, start, end = generate_maze(rows, cols, wall_chance=0.25, seed=42)

    print("Here's the maze:")
    print_maze(grid, start, end)
    print()

    algorithms = {
        "BFS": bfs,
        "DFS": dfs,
        "A*": astar
    }

    for name in algorithms:
        func = algorithms[name]
        path = func(grid, start, end)
        print(f"--- {name} ---")
        if path:
            print("path length:", len(path))
            print_maze(grid, start, end, path)
        else:
            print("couldn't find a path")
        print()


if __name__ == "__main__":
    main()

    test_grid = [
        [0, 0, 1],
        [1, 0, 1],
        [1, 0, 0]
    ]
    test_start = (0, 0)
    test_end = (2, 2)

    for name, func in [("bfs", bfs), ("dfs", dfs), ("astar", astar)]:
        p = func(test_grid, test_start, test_end)
        assert p is not None
        assert p[0] == test_start
        assert p[-1] == test_end

    print("tests passed i think")
