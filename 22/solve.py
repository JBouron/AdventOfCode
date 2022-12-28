#!/usr/bin/env python

import sys
from enum import Enum
import re

# A position (x, y) in the 2D grid.
class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar):
        assert type(scalar) == int
        return Position(self.x * scalar, self.y * scalar)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return str((self.x, self.y))

DIRS = [Position(1, 0), Position(0, 1), Position(-1, 0), Position(0, -1)]

class Board:
    class CellType(Enum):
        Free = 1
        Rock = 2
        Oob = 3

    def __init__(self, grid):
        self.grid = grid
        self.width = len(grid[0])
        self.height = len(grid)

    # Compute the start index and the width of the row at height y.
    # The start index is the smallest x that is not out of bounds in this row.
    # The width is the number of cell from the start index that are not out of
    # bounds.
    def rowStartAndWidth(self, y):
        r = list(filter(lambda c: c[1] != Board.CellType.Oob,
                        enumerate(self.grid[y])))
        return (r[0][0], len(r))

    def colStartAndHeight(self, x):
        col = [self.grid[y][x] for y in range(self.height)]
        r = list(filter(lambda c: c[1] != Board.CellType.Oob, enumerate(col)))
        return (r[0][0], len(r))

    # Compute the password when tracing `path` onto the board.
    def computePassword(self, path, part2):
        # Compute the starting position.
        startX = self.rowStartAndWidth(0)[0]
        currPos = Position(startX, 0)
        # Start facing to the right.
        rotIdx = 0
        currRot = DIRS[rotIdx]

        # The list of next moves. First element is the first move, at each step
        # we pop the first element.
        moves = re.findall("[0-9]+|[A-Z]", path)

        # For a position `p` and a direction `d`, compute the next position on
        # the board. This could be `p` if we are walking against a rock, or this
        # could be on the other side of the board in case of wrap-around
        def getNextPosAndRot(p, d):
            # Split the logic between vertical and horizontal movements to make
            # it easier.
            if abs(d.x) == 1 and d.y == 0:
                # Horizontal movement.
                nextY = p.y
                s, w = self.rowStartAndWidth(p.y)
                nextX = s + (p.x - s + d.x) % w
            else:
                # Vertical movement.
                assert d.x == 0 and abs(d.y) == 1
                nextX = p.x
                s, h = self.colStartAndHeight(p.x)
                nextY = s + (p.y - s + d.y) % h
            nextPos = Position(nextX, nextY)
            # Sanity check that we computed the wrap-around correctly.
            assert self.grid[nextPos.y][nextPos.x] != Board.CellType.Oob
            if self.grid[nextPos.y][nextPos.x] == Board.CellType.Rock:
                # In case the next position lands on a rock, we don't move.
                return p, d
            else:
                return nextPos, d

        def faceId(p):
            key = Position(p.x // 50, p.y // 50)
            kToId = {
                Position(2, 0): 1,
                Position(1, 0): 2,
                Position(1, 1): 3,
                Position(1, 2): 4,
                Position(0, 2): 5,
                Position(0, 3): 6,
            }
            return kToId[key]

        def getNextPosAndRotPart2(p, d):
            # Split the logic between vertical and horizontal movements to make
            # it easier.
            fId = faceId(p)
            x, y = p.x, p.y
            nextX = None
            nextY = None
            nextDx = None
            nextDy = None
            # Right wrap.
            if d.x == 1:
                if fId == 1 and x == 149:
                    nextX = 99
                    nextY = 149 - y
                    nextDx = -1
                    nextDy = 0
                elif fId == 3 and x == 99:
                    nextX = 50 + y
                    nextY = 49
                    nextDx = 0
                    nextDy = -1
                elif fId == 4 and x == 99:
                    nextX = 149
                    nextY = 149 - y
                    nextDx = -1
                    nextDy = 0
                elif fId == 6 and x == 49:
                    nextX = y - 100
                    nextY = 149
                    nextDx = 0
                    nextDy = -1
            elif d.x == -1:
                # Left wrap.
                if fId == 2 and x == 50:
                    nextX = 0
                    nextY = 149 - y
                    nextDx = 1
                    nextDy = 0
                if fId == 3 and x == 50:
                    nextX = y - 50
                    nextY = 100
                    nextDx = 0
                    nextDy = 1
                if fId == 5 and x == 0:
                    nextX = 50
                    nextY = 149 - y
                    nextDx = 1
                    nextDy = 0
                if fId == 6 and x == 0:
                    nextX = y - 100
                    nextY = 0
                    nextDx = 0
                    nextDy = 1
            elif d.y == 1:
                # down wrap
                if fId == 1 and y == 49:
                    nextX = 99
                    nextY = x - 50
                    nextDx = -1
                    nextDy = 0
                if fId == 4 and y == 149:
                    nextX = 49
                    nextY = x + 100
                    nextDx = -1
                    nextDy = 0
                if fId == 6 and y == 199:
                    nextX = 100 + x
                    nextY = 0
                    nextDx = 0
                    nextDy = 1
            elif d.y == -1:
                # Up wrap
                if fId == 1 and y == 0:
                    nextX = x - 100
                    nextY = 199
                    nextDx = 0
                    nextDy = -1
                if fId == 2 and y == 0:
                    nextX = 0
                    nextY = x + 100
                    nextDx = 1
                    nextDy = 0
                if fId == 5 and y == 100:
                    nextX = 50
                    nextY = 50 + x
                    nextDx = 1
                    nextDy = 0

            if nextX is None:
                assert nextY is None and nextDx is None and nextDy is None
                nextDx = d.x
                nextDy = d.y
                # We are not going to another face.
                if abs(d.x) == 1 and d.y == 0:
                    # Horizontal movement.
                    nextY = p.y
                    s, w = self.rowStartAndWidth(p.y)
                    nextX = s + (p.x - s + d.x) % w
                else:
                    # Vertical movement.
                    assert d.x == 0 and abs(d.y) == 1
                    nextX = p.x
                    s, h = self.colStartAndHeight(p.x)
                    nextY = s + (p.y - s + d.y) % h

            nextPos = Position(nextX, nextY)
            # Sanity check that we computed the wrap-around correctly.
            assert self.grid[nextPos.y][nextPos.x] != Board.CellType.Oob
            if self.grid[nextPos.y][nextPos.x] == Board.CellType.Rock:
                # In case the next position lands on a rock, we don't move.
                return p, d
            else:
                return nextPos, Position(nextDx, nextDy)

        def rotateLeft(d):
            res = {
                Position(1, 0) : Position(0, -1),
                Position(0, 1) : Position(1, 0),
                Position(-1, 0) : Position(0, 1),
                Position(0, -1) : Position(-1, 0),
            }
            return res[d]

        def rotateRight(d):
            res = {
                Position(1, 0) : Position(0, 1),
                Position(0, 1) : Position(-1, 0),
                Position(-1, 0) : Position(0, -1),
                Position(0, -1) : Position(1, 0),
            }
            return res[d]

        while len(moves) > 0:
            currMove = moves.pop(0)
            if "L" in currMove:
                # Rotate to the left.
                currRot = rotateLeft(currRot)
            elif "R" in currMove:
                # Rotate to the right.
                currRot = rotateRight(currRot)
            else:
                # Make a few steps.
                numSteps = int(currMove)
                for i in range(numSteps):
                    if part2:
                        nextPos, currRot = getNextPosAndRotPart2(currPos, currRot)
                    else:
                        nextPos, currRot = getNextPosAndRot(currPos, currRot)
                    if nextPos == currPos:
                        # Ran into a wall, stop the move and go to the next one.
                        break
                    else:
                        currPos = nextPos

        rotVal = {
            Position(1, 0) : 0,
            Position(0, 1) : 1,
            Position(-1, 0) : 2,
            Position(0, -1) : 3,
        }

        return 1000 * (currPos.y + 1) + 4 * (currPos.x + 1) + rotVal[currRot]

def parseInput(inputFile):
    fd = open(inputFile, "r")
    lines = fd.readlines()
    blank = list(filter(lambda p: p[1] == "\n", enumerate(lines)))
    assert len(blank) == 1
    blankIdx = blank[0][0]

    lines = list(map(lambda l: l.replace("\n", ""), lines))

    grid = lines[:blankIdx]
    
    # Not all lines are the same length, pad the smaller lines with spaces.
    width = max(map(lambda l: len(l), grid))
    grid = list(map(lambda row: row + " "*(width - len(row)), grid))

    # Translate from chars to Board.CellType.
    def charToCellType(c):
        return Board.CellType.Free if c == "." else \
               Board.CellType.Rock if c == "#" else Board.CellType.Oob
    grid = list(map(lambda row: [charToCellType(c) for c in row], grid))

    board = Board(grid)

    # Parse the path.
    path = lines[blankIdx+1]
    fd.close()
    return (board, path)

def part1(inputFile):
    board, path = parseInput(inputFile)
    return board.computePassword(path, False)

def part2(inputFile):
    board, path = parseInput(inputFile)
    return board.computePassword(path, True)

if __name__ == "__main__":
    inputFile = sys.argv[1]
    print("Part 1: {}".format(part1(inputFile)))
    print("Part 2: {}".format(part2(inputFile)))
