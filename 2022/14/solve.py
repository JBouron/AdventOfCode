#!/usr/bin/env python

# Smarter solution that uses DFS instead of running the simulation for each unit
# of sand.

import sys
from enum import Enum
import copy

# A position (x, y) in the 2D grid.
class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return str((self.x, self.y))

class Grid:
    # Create an empty grid. If `part1` is False then this grid has a floor
    # otherwise it is floating above the abyss.
    def __init__(self):
        # Keep track of the coordinates of all rock tiles.
        self.rocks = set()
        # The position where the sand is dropped from.
        self.sandSourcePos = Position(500, 0)
        # When true, all positions with coordinate y == self.floorY are
        # considered to be rock.
        self.hasFloor = False
        # The y coordinate of the floor.
        self.floorY = 0
        # Keep track of the minimum and the maximum x and y coordinates. This
        # essentially store the two corner of the smallest square that can hold
        # all the rocks. This is used to compute the positions that are
        # considered out of bounds and by extension which positions are
        # considered in the abyss.
        self.min = copy.copy(self.sandSourcePos)
        self.max = copy.copy(self.sandSourcePos)

    # Check if a given position is rock or not.
    def isRock(self, pos):
        return (self.hasFloor and pos.y == self.floorY) or pos in self.rocks

    # Return true if the position `pos` is outside the boundaries, such tiles
    # will always fall into the abyss.
    # If the grid has a floor then no tile can be out of bounds.
    def outOfBounds(self, pos):
        return not self.hasFloor and \
               not (self.min.x <= pos.x <= self.max.x and \
                    self.min.y <= pos.y <= self.max.y)

    # Add a path of rock to the grid. vertices is a list of Positions containing
    # the coordinates of each point in the path.
    def addPath(self, vertices):
        # Add a rock at position `pos`.
        def addRock(pos):
            # Make sure the grid is big enough to insert the point, add air cells
            # if this is not the case
            self.rocks.add(pos)
            self.min.x = min(self.min.x, pos.x)
            self.min.y = min(self.min.y, pos.y)
            self.max.x = max(self.max.x, pos.x)
            self.max.y = max(self.max.y, pos.y)
            self.floorY = self.max.y + 2

        # Add a line of rock starting at start and ending at end. startPos and
        # endPos must describe a straight line.
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
                    addRock(Position(x, y))

        for i in range(1, len(vertices)):
            addLine(vertices[i-1], vertices[i])

    # Run DFS until a termination condition is reached. Return the number of
    # units of sand that reached a resting state before hitting the termination
    # condition. terminationFunc is a function taking a position as its sole
    # argument and returns True if the position satisfies the termination
    # condition, False otherwise.
    def dfs(self, terminationFunc):
        # Visited set and stack to implement DFS. Start with the position of the
        # source of sand.
        visited = set()
        visited.add(self.sandSourcePos)
        stack = [self.sandSourcePos]
        # Keep track of how we reached a particular tile using DFS, e.g. which
        # tile was being processed when the current tile had been pushed onto
        # the stack. With this dict we can trace back the path from the
        # termination tile to the sand source.
        parent = {}
        # The result of the function to be returned. This holds the number of
        # tiles that where processed by the loop below, counting the tile that
        # triggered the termination condition.
        res = 0
        while len(stack) > 0:
            res += 1
            tile = stack.pop(0)
            assert tile in visited
            if terminationFunc(tile):
                # We reached the termination, this can only happen in part 1.
                # The problem at this point is that `res` is also counting the
                # tiles we iterated over to find the first tile falling into the
                # abyss. By definition, those tiles are not indicating resting
                # sand and should not be counted. Therefore we need to subtract
                # the lenght of the path from the source of sand to the current
                # tile.
                curr = tile
                pathLen = 0
                while curr != self.sandSourcePos:
                    pathLen += 1
                    curr = parent[curr]
                return res - pathLen - 1
            # Insert the next tile to visit in the stack, the order matters
            # here, we want to visit `down`, `leftDown` and `rightDown` in that
            # order and therefore those must be pushed into the opposite order
            # onto the stack.
            down = Position(tile.x, tile.y + 1)
            leftDown = Position(tile.x - 1, tile.y + 1)
            rightDown = Position(tile.x + 1, tile.y + 1)
            for p in [rightDown, leftDown, down]:
                if not self.isRock(p) and p not in visited:
                    # Record from which tile `p` was reached.
                    parent[p] = tile
                    visited.add(p)
                    stack.insert(0, p)
        # No tile hit the termination condition. This is the case when running
        # part 2.
        return res

    # Run the simulation of sand falling from the sand source. Assume that there
    # is no floor, and return the number of units of sand coming to rest before
    # the sand starts falling into the abyss.
    def runPart1(self):
        numDrops = self.dfs(self.outOfBounds)
        return numDrops

    # Run the simulation of sand falling from the sand source. Assume that
    # there is a floor, and return the number of units of sand coming to rest
    # before the source gets blocked.
    def runPart2(self):
        self.hasFloor = True
        numDrops = self.dfs(lambda _: False)
        self.hasFloor = False
        return numDrops

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
