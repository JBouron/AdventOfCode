#!/usr/bin/env python

import sys
import copy
import math

class JetPattern:
    # `pattern` is a string containing the entire pattern.
    def __init__(self, pattern):
        self.pattern = pattern
        self.currIdx = 0

    # Get the next jet. Repeats the pattern infinitely.
    def next(self):
        res = self.pattern[self.currIdx % len(self.pattern)]
        self.currIdx += 1
        return res

class Shape:
    def __init__(self, mask):
        self.mask = mask
        self.width = len(mask[0])
        self.height = len(mask)

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
    def __init__(self, jetPattern):
        self.width = 7
        # Start with just the floor
        self.height = 1
        # Indicates, for each row i, which cells are free and which are not.
        # True == there is a rock there. Assume floor is made of rock.
        self.hitbox = [[True] * self.width]
        self.jetPattern = jetPattern

    # Add n new rows to the hitbox
    def newRows(self, n):
        for i in range(n):
            self.hitbox.append([False] * self.width)

    def maxHeight(self):
        r = list(filter(lambda r: True in r[1], enumerate(self.hitbox)))
        return r[-1][0] + 1

    def dropShape(self, shape):
        # Compute initial position of shape. Coordinates of a shape is the coord
        # of its bottom left corner.
        startPos = Position(2, self.maxHeight() + 3) 
        # The current position of the shape.
        currPos = copy.copy(startPos)
        # Add enough row to avoid out of bounds issues.
        if self.height <= currPos.y + shape.height:
            self.newRows(currPos.y + shape.height - self.height);
            self.height = len(self.hitbox)

        # Check if for a position `p` the shape will collide with another shape
        # or the floor.
        def collision(p):
            res = False
            for y in range(p.y, p.y + shape.height):
                for x in range(p.x, p.x + shape.width):
                    res |= (self.hitbox[y][x] and shape.mask[y-p.y][x-p.x])
            return res

        # For a position `p` get the next position when applying jet `jet`.
        def push(p, jet):
            d = -1 if jet == "<" else 1
            n = Position(min(max(0, p.x + d), self.width - shape.width), p.y)
            # Make sure the push is not going to collide with another shape.
            return p if collision(n) else n

        # Stop the shape at position `p` and update the hitbox accordingly.
        def stop(p):
            for y in range(p.y, p.y + shape.height):
                for x in range(p.x, p.x + shape.width):
                    self.hitbox[y][x] |= shape.mask[y-p.y][x-p.x]
        # Do the sim.
        while True:
            # First push.
            jet = self.jetPattern.next()
            currPos = push(currPos, jet)

            # Then fall down.
            down = Position(currPos.x, currPos.y - 1)
            if not collision(down):
                currPos = down
            else:
                # We collided with something, stop here. Update the hitbox with
                # the current position of the shape.
                stop(currPos)
                return

    def __repr__(self):
        res = ""
        for i in range(len(self.hitbox)-1):
            rowIndex = len(self.hitbox)-1-i
            row = self.hitbox[rowIndex]
            res += str(rowIndex) + ":\t|" + "".join(["#" if t else "." for t in row]) + "|\n"
        res += "0:\t+-------+"
        return res


# Parse the file and returns a JetPattern.
def parseInput(inputFile):
    fd = open(inputFile, "r")
    lines = list(map(lambda l: l.replace("\n",""), fd.readlines()))
    fd.close()
    s = "".join(lines)
    return JetPattern(s)

SHAPES = [
    Shape([[True] * 4]),

    Shape([[False, True , False],
           [True , True , True ],
           [False, True , False]]),

    Shape([[True , True , True],
           [False, False, True],
           [False, False, True]]),

    Shape([[True], [True], [True], [True]]),

    Shape([[True, True],
           [True, True]]),
]

def part1(inputFile):
    jp = parseInput(inputFile)
    grid = Grid(jp)
    for i in range(2022):
        s = SHAPES[i % len(SHAPES)]
        grid.dropShape(s)
    return grid.maxHeight() - 1

def part2(inputFile):
    inputLen = len(parseInput(inputFile).pattern)
    totalNumRocks = 1000000000000

    jp = parseInput(inputFile)
    grid = Grid(jp)

    # Number of rocks dropped so far.
    numRocksDropped = 0

    numRowsForHash = 128
    # Return a hash of the content of the `numRowsForHash` top rows of the grid.
    def hashTopRows():
        topRowIdx = grid.maxHeight() - 1
        h = 0
        for i in range(numRowsForHash):
            row = grid.hitbox[topRowIdx-i]
            rowByte = 0
            for b in row:
                rowByte <<= 1
                rowByte |= (1 if b else 0)
            h <<= 8
            h |= rowByte
        return h

    # For each hash of `numRocksDropped` rows, record the max height and the
    # number of rocks dropped.
    cycleData = {}
    # The height of the cycle.
    cycleHeight = 0
    # The number of rocks dropped per cycle.
    cycleNumRocks = 0

    # First step is to find a repeating pattern. Drop rocks and at each rock
    # check if the last `numRocksDropped` top rows of the grid already appeared
    # in the past.
    while True:
        s = SHAPES[numRocksDropped % len(SHAPES)]
        grid.dropShape(s)
        numRocksDropped += 1
        maxH = grid.maxHeight() - 1
        if numRowsForHash < maxH:
            h = hashTopRows()
            if h in cycleData.keys():
                # We have seen those rows before. The max height difference
                # gives us the height of the repeating pattern. The difference
                # on the number of rocks dropped gives us how many rocks
                # constitute the pattern.
                cycleHeight = maxH - cycleData[h][0]
                cycleNumRocks = numRocksDropped - cycleData[h][1]
                break
            cycleData[h] = (maxH, numRocksDropped)
    print("cycleHeight   = {}".format(cycleHeight))
    print("cycleNumRocks = {}".format(cycleNumRocks))

    # How many full cycle / patterns are left before reaching 1 trillion rocks?
    numCyclesLeft = (totalNumRocks - numRocksDropped) // cycleNumRocks
    print("numCyclesLeft  = {}".format(numCyclesLeft))

    res = grid.maxHeight() - 1 + numCyclesLeft * cycleHeight

    # Now need to compute the top of the tower, this a fraction of a cycle /
    # pattern.
    maxHBefore = grid.maxHeight() - 1
    numRocksDropped += numCyclesLeft * cycleNumRocks
    while numRocksDropped <= totalNumRocks:
        s = SHAPES[numRocksDropped % len(SHAPES)]
        grid.dropShape(s)
        numRocksDropped += 1
    maxHAfter = grid.maxHeight() - 1

    res += maxHAfter - maxHBefore - 1
    return res

if __name__ == "__main__":
    inputFile = sys.argv[1]
    print("Part 1: {}".format(part1(inputFile)))
    print("Part 2: {}".format(part2(inputFile)))

#130:    |.......|
#129:    |.......|
#128:    |.......|
#127:    |.......|
#126:    |.......|
#125:    |....#..|
#124:    |....#..|
#123:    |..###.#|
#122:    |.####.#|
#121:    |###.###|
#120:    |.#####.|
#119:    |.###...|
#118:    |.###...|
#117:    |.#.#...|
#116:    |.#.#.#.|
#115:    |.######|
