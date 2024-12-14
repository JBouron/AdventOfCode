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

    # Get the list of neighbors of a particular position.
    # @param pos: The position to get the neighbors of.
    # @return: A list of positions indicating the position of all the neighbor
    # of `pos`. This list is filtered to only contain positions that falls
    # within the bounds of the grid.
    def neighbors_of(self, pos: Pos2d):
        res = []
        voff = [Pos2d(-1, 0), Pos2d(1, 0), Pos2d(0, -1), Pos2d(0, 1)]
        for off in voff:
            npos = pos + off
            if self.in_bounds(npos):
                res.append(npos)
        return res

    # Same as neighbors_of but only return diagonal neighbors.
    def diagonal_neighbors_of(self, pos):
        res = []
        voff = [Pos2d(-1, -1), Pos2d(-1, 1), Pos2d(1, -1), Pos2d(1, 1)]
        for off in voff:
            npos = pos + off
            if self.in_bounds(npos):
                res.append(npos)
        return res

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

plots = Grid.from_file(sys.argv[1], None)
# Bit mask to indicates which plots have been visited and binned into a region
# already.
visited = Grid.fill(plots.width, plots.height, False)

def compute_region_stat(start_pos):
    Q = [start_pos]
    assert not visited[start_pos]
    visited[start_pos] = True

    area = 0
    perimeter = 0
    sides = 0

    while len(Q):
        pos = Q.pop(0)
        neighbors = plots.neighbors_of(pos)

        area += 1
        p = 4-sum(map(lambda n: 1 if plots[n] == plots[pos] else 0, neighbors))
        assert 0 <= p <= 4
        perimeter += p

        # Using the perimeters and the neighbors, we can count the number of
        # corners/angles added by this plot, which gives us the number of sides
        # added by this plot.
        is_outside_corner = False
        if p == 4:
            # This region only contains a single plot hence 4 sides.
            sides += 4
            is_outside_corner = True
        elif p == 3:
            # This is a small bump coming out of the region, 2 corner/sides.
            sides += 2
            is_outside_corner = True
        elif p == 2:
            # This plot may not be a corner, for example:
            #   X P X
            #   X P X
            #   X P X
            # The middle plot P has a perimeter of 2 but is not a corner plot
            # hence does not contribute to the number of corners/sides.
            same = list(filter(lambda n: plots[n] == plots[pos], neighbors))
            assert len(same) == 2
            if same[0].x != same[1].x and same[0].y != same[1].y:
                # True only if the current plot and its two neighbors of the
                # same type are not aligned, i.e. form a corner.
                sides += 1
                is_outside_corner = True

        # Check for "insider corners" of the region, i.e.:
        #   X X P
        #   P P P <- This is a corner with perimeter = 0!
        # We need to check for any diagonal neighbor that is not of the same
        # type as the current plot. The number of such neighbors gives use
        # the number of corners / sides created by the current plot.
        for n in plots.diagonal_neighbors_of(pos):
            nn = plots.neighbors_of(n)
            inter = set(nn)
            inter &= set(neighbors)
            inter = list(inter)
            is_corner = plots[n] != plots[pos] and plots[inter[0]] == plots[pos] and plots[inter[1]] == plots[pos]
            assert(len(inter) == 2)
            # If the plots in inter are of the same type of the current plot
            # then the current plot is an inside corner.
            if is_corner:
                sides += 1

        for neigh in neighbors:
            if plots[neigh] == plots[pos] and not visited[neigh]:
                    visited[neigh] = True
                    Q.append(neigh)
    return area, perimeter, sides


part1 = 0
part2 = 0
for y in range(plots.height):
    for x in range(plots.width):
        pos = Pos2d(x, y)
        if not visited[pos]:
            # New undiscovered region
            a, p, s = compute_region_stat(pos)
            part1 += a * p
            part2 += a * s
print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
