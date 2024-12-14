#!/bin/python3

import sys
from typing import Callable
from typing import Any

# Representation of a 2D position.
class Pos2d:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        return (self.x, self.y) == (other.x, other.y)

    def __sub__(self, other):
        return Pos2d(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Pos2d(self.x + other.x, self.y + other.y)

    def __neg__(self):
        return Pos2d(-self.x, -self.y)

    def __mul__(self, scalar):
        return Pos2d(self.x * scalar, self.y * scalar)

    def __hash__(self):
        return hash((self.x, self.y))

# Representation of a 2D grid with convenience functions.
class Grid:
    # Create a 2D grid from a 2D list
    # @param rows: The 2D list to create the grid from. This list is NOT copied.
    def __init__(self, rows: list[list[Any]]):
        prev_row_len = len(rows[0])
        for i in range(1, len(rows)):
            if len(rows[i]) != prev_row_len:
                raise Exception("Not all rows have the same length")
        self.rows = rows
        self.width = prev_row_len
        self.height = len(rows)

    # Create a 2D grid with the given dimension in which all cells have the same
    # value.
    # @param width: Width of the Grid.
    # @param height: Height of the Grid.
    # @param value: Value to initialize all cells to.
    @staticmethod
    def fill(width: int, height: int, value: Any):
        rows = []
        for i in range(height):
            rows.append([value] * width)
        return Grid(rows)

    # Parse a grid from a text file.
    # @param filename: Path to the text file to parse the grid from.
    # @param value_map: (Optional) Function to map the characters of the file
    # into a value. Called for each cell/position of the grid. If omitted, the
    # resulting grid is a grid of characters/strings.
    # @return: The Grid corresponding to the contents of the file.
    @staticmethod
    def from_file(filename: str, value_map: Callable[str, Any]):
        fd = open(filename, "r")
        rows = []
        for line in fd:
            chars = list(line.replace("\n", ""))
            if value_map is not None:
                chars = list(map(lambda c: value_map(c), chars))
            rows.append(chars)
        return Grid(rows)

    # Find a value in the Grid.
    # @param value: The value to find.
    # @return: A list of the position of all the cells matching the value. Empty
    # list if no such cell matches the value. The order of the list is
    # undefined.
    def find(self, value: Any) -> list[Pos2d]:
        return [Pos2d(x, y) \
                for y in range(len(self.rows)) \
                for x in range(len(self.rows[y])) \
                if self.rows[y][x] == value]

    # Get a set of all the values contained in the grid.
    def values(self):
        res = set()
        for y in range(len(self.rows)):
            for x in range(len(self.rows[y])):
                res.add(self.rows[y][x])
        return res

    # Get the value of the cell at the given coordinate.
    def __getitem__(self, index: Pos2d | tuple[int, int]) -> Any:
        if type(index) is Pos2d:
            x, y = index.x, index.y
        else:
            x, y = index
        if self.in_bounds((x, y)):
            return self.rows[y][x]
        else:
            raise Exception("Error: Grid indices out of range")

    # Set the value of the cell at the given coordinate.
    def __setitem__(self, index: Pos2d | tuple[int, int], value: Any):
        if type(index) is Pos2d:
            x, y = index.x, index.y
        else:
            x, y = index
        if self.in_bounds((x, y)):
            self.rows[y][x] = value
        else:
            raise Exception("Error: Grid indices out of range")

    # Check if coordinates are within the grid's bounds.
    def in_bounds(self, index: Pos2d | tuple[int, int]) -> bool:
        if type(index) is Pos2d:
            x, y = index.x, index.y
        else:
            x, y = index
        return 0 <= y < len(self.rows) and 0 <= x < len(self.rows[y])

    def __str__(self):
        res = ""
        for r in self.rows:
            if type(r[0]) == bool:
                # Special case for bools, use 0s and 1s.
                s = "".join(list(map(lambda e: "1" if e else "0", r)))
            else:
                s = "".join(list(map(lambda e: str(e), r)))
            res += s + "\n"
        return res[:-1]

grid = Grid.from_file(sys.argv[1], lambda c: int(c))
trailheads = grid.find(0)

# Compute the score and rating of a trailhead.
# @param trailhead: Pos2d of the start of the trail.
# @return: A tuple (score, rating) associated with this trailhead.
def compute_score_and_rating(trailhead):
    # Use a variation of BFS in which we do not maintain the set of visited
    # nodes. This set is not needed because we cannot end-up stuck in a loop
    # since each step must increase the height by 1.
    # Not using a visited set means that we might visit the same node twice if
    # two paths from the trailhead to this node exist. This is on purpose as
    # this allows us to count the number of distinct paths from the trailhead to
    # the peak(s).
    score = 0
    Q = [trailhead]
    peaks = set()
    rating = 0
    while len(Q):
        pos = Q.pop(0)
        assert grid.in_bounds(pos)
        if grid[pos] == 9:
            rating += 1
            if pos not in peaks:
                peaks.add(pos)
                score += 1
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if abs(dx) + abs(dy) != 1:
                    # Don't do diagonals and don't do the current pos.
                    continue
                nei = pos + Pos2d(dx, dy)
                if grid.in_bounds(nei) and grid[pos] == grid[nei] - 1:
                    Q.append(nei)
    return score, rating

part1 = 0
part2 = 0
for t in trailheads:
    score, rating = compute_score_and_rating(t)
    part1 += score
    part2 += rating
print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
