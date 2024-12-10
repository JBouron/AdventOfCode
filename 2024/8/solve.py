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
                chars = list(map(lambda c: value_map(c), char))
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
            res += s
        return res[:-1]

if __name__ == "__main__":
    grid = Grid.from_file(sys.argv[1], None)
    # Bitmap of antinodes
    antinode_grid = Grid.fill(grid.width, grid.height, False)
    freqs = list(filter(lambda f: f != ".", grid.values()))

    # For each frenquency, find all pairs of antennas and for each pair compute
    # the positions of the two antinodes.
    for f in freqs:
        antennas = grid.find(f)
        for a1 in antennas:
            for a2 in antennas:
                if a1 == a2:
                    continue
                d = a2 - a1
                assert a1 + (d * 2) != (a1 + d) * 2
                ant1 = a1 + d * 2
                ant2 = a1 - d

                if antinode_grid.in_bounds(ant1):
                    antinode_grid[ant1] = True
                if antinode_grid.in_bounds(ant2):
                    antinode_grid[ant2] = True
    part1 = len(antinode_grid.find(True))
    print(f"Part 1: {part1}")

    antinode_grid = Grid.fill(grid.width, grid.height, False)
    # For each frenquency, find all pairs of antennas and for each pair compute
    # the positions of all antinodes.
    for f in freqs:
        antennas = grid.find(f)
        for a1 in antennas:
            for a2 in antennas:
                if a1 == a2:
                    continue
                d = a2 - a1
                if d.x == d.y:
                    # This is a straight diagonal, use (1, 1) so we cover all
                    # the cells.
                    d.x = d.x // abs(d.x)
                    d.y = d.y // abs(d.y)
                elif d.x == 0:
                    d.y = d.y // abs(d.y)
                elif d.y == 0:
                    d.x = d.x // abs(d.x)

                # Forward.
                curr = a1
                while grid.in_bounds(curr):
                    antinode_grid[curr] = True
                    curr = curr + d

                # Backward.
                curr = a1
                while grid.in_bounds(curr):
                    antinode_grid[curr] = True
                    curr = curr - d
    part2 = len(antinode_grid.find(True))
    print(f"Part 2: {part2}")
