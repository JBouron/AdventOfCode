#!/usr/bin/env python

import sys
from enum import Enum

# A position (x, y) in the 2D grid.
class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return str((self.x, self.y))

class Grid:
    # The type of a cell in the grid.
    class Type(Enum):
        Air = 1
        Rock = 2
        Sand = 3

    # Create an empty grid. If `part1` is False then this grid has a floor
    # otherwise it is floating above the abyss.
    def __init__(self):
        self.grid = [[Grid.Type.Air]]
        self.sandSourcePos = Position(500, 0)
        # When true, all positions with coordinate y == self.floorY are
        # considered to be rock.
        self.hasFloor = False
        # The y coordinate of the floor.
        self.floorY = 0

    # Get the width of the grid.
    def width(self):
        return len(self.grid[0]) if len(self.grid) > 0 else 0

    # Get the height of the grid.
    def height(self):
        return len(self.grid)

    # Set the grid value at pos to be of type t. Automatically grows the grid if
    # needed.
    def set(self, pos, t):
        # Make sure the grid is big enough to insert the point, add air cells
        # if this is not the case
        if self.width() <= pos.x:
            W = self.width()
            for row in self.grid:
                row += [Grid.Type.Air for i in range(pos.x - W + 1)]
        if self.height() <= pos.y:
            H = self.height()
            self.grid += [[Grid.Type.Air for i in range(self.width())] for j in range(pos.y - H + 1)]

        # Sanity check that the logic above is working as intended.
        assert pos.x < self.width() and pos.y < self.height()

        # Set the cell to the given type.
        self.grid[pos.y][pos.x] = t

    # Return the type of the tile at position `pos` in the grid.
    def get(self, pos):
        if pos.x < self.width() and pos.y < self.height():
            return self.grid[pos.y][pos.x]
        elif self.hasFloor and pos.y == self.floorY:
            return Grid.Type.Rock
        else:
            return Grid.Type.Air

    # Add a path of rock to the grid. vertices is a list of Positions containing
    # the coordinates of each point in the path.
    def addPath(self, vertices):
        # Add a line of rock starting at start and ending at end.
        # startPos and endPos must describe a straight line.
        def addLine(start, end):
            # Sanity check that this is indeed a straight line.
            assert start.x == end.x or start.y == end.y
            # Realistically we can trace the line with a single loop, but using
            # nested loops here means we don't have to bother checking if we
            # need to iterate on the x axis (horizontal line) or the y axis
            # (vertical line).
            # Typically such loops would draw a square, but given the assert
            # above this is an edge case where the square is of width or height
            # of 1, hence a line.
            for y in range(min(start.y, end.y), max(start.y, end.y) + 1):
                for x in range(min(start.x, end.x), max(start.x, end.x) + 1):
                    self.set(Position(x, y), Grid.Type.Rock)

        for i in range(1, len(vertices)):
            addLine(vertices[i-1], vertices[i])

        # Update the floor's y position to be 2 lower than the lowest line.
        rockPosY = [y for x in range(self.width()) \
            for y in range(self.height()) if self.grid[y][x] == Grid.Type.Rock]
        self.floorY = max(rockPosY) + 2

    # Drop a unit of sand and run the simulation until either that unit of sand
    # comes to rest of falls into the abyss.  Return True if the sand fell into
    # the abyss, False otherwise.
    def dropSand(self):
        # Check if a position is in the abyss, e.g. outside the grid
        # boundaries. Such a position will never go back to the grid.
        # In part2 this always return False.
        def inAbyss(pos):
            return not self.hasFloor and \
                   (pos.x < 0 or self.width() <= pos.x or \
                   pos.y < 0 or self.height() <= pos.y)

        # Check if a position in the grid is free, e.g. not blocked by sand or
        # Rock. A position in the abyss is always free.
        def isFree(pos):
            # The inAbyss check also acts as a bound check for the right
            # side of the condition.
            return (inAbyss(pos) or self.get(pos) == Grid.Type.Air)

        # For a given position of a unit of sand, compute the next positition at
        # the next step of the simulation.
        def nextPos(pos):
            # Apply the rules as described in the problem statement.
            down = Position(pos.x, pos.y + 1)
            leftDown = Position(pos.x - 1, pos.y + 1)
            rightDown = Position(pos.x + 1, pos.y + 1)
            if isFree(down):
                # Case #1: The tile immediately below the unit of sand is not
                # blocked. The sand falls straight down.
                return down
            elif isFree(leftDown):
                # Case #2: The tile under the sand is blocked. The tile on the
                # left diagonal is free.
                return leftDown
            elif isFree(rightDown):
                # Case #2: The tile under the sand is blocked. The tile on the
                # left diagonal is blocked but the tile on the right diagonal is
                # free.
                return rightDown
            else:
                # All positions are blocked, this unit of sand comes to rest at
                # its current position.
                return pos

        curr = self.sandSourcePos
        next = nextPos(curr)
        while not inAbyss(curr) and next != curr:
            curr = next
            next = nextPos(curr)
        if not inAbyss(curr):
            # The sand got into a resting position, update the grid.
            self.set(curr, Grid.Type.Sand)
        return inAbyss(curr)

    # Run the simulation of sand falling from the sand source. Assume that there
    # is no floor, and return the number of units of sand coming to rest before
    # the sand starts falling into the abyss.
    def runPart1(self):
        numDrops = 0
        while not self.dropSand():
            numDrops += 1
        return numDrops

    # Run the simulation of sand falling from the sand source. Assume that
    # there is a floor, and return the number of units of sand coming to rest
    # before the source gets blocked.
    def runPart2(self):
        self.hasFloor = True
        numDrops = 0
        while self.get(self.sandSourcePos) == Grid.Type.Air:
            self.dropSand()
            numDrops += 1
        self.hasFloor = False
        return numDrops

    def __str__(self):
        res = ""
        for y in range(self.height()):
            for x in range(494,self.width()):
                s = "."
                if self.grid[y][x] == Grid.Type.Rock:
                    s = "#"
                elif self.grid[y][x] == Grid.Type.Sand:
                    s = "o"

                res += s
            res += "\n"
        return res


# Parse the input file and returns a Grid.
def parseInput(inputFile):
    fd = open(inputFile, "r")
    lines = fd.readlines()

    grid = Grid()

    for l in lines:
        l = l.replace("\n", "")
        l = l.split(" -> ")
        l = list(map(lambda p: Position(int(p.split(",")[0]), int(p.split(",")[1])), l))
        grid.addPath(l)
    fd.close()
    return grid

def part1(inputFile):
    grid = parseInput(inputFile)
    return grid.runPart1()

def part2(inputFile):
    grid = parseInput(inputFile)
    return grid.runPart2()

if __name__ == "__main__":
    inputFile = sys.argv[1]
    print("Part 1: {}".format(part1(inputFile)))
    print("Part 2: {}".format(part2(inputFile)))
