#!/usr/bin/env python

import sys
import copy
import math

# A position (x, y) in the 2D grid.
class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Position(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        assert type(scalar) == int
        return Position(self.x * scalar, self.y * scalar)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return str((self.x, self.y))

CHARTODIR = {
    ">": Position(1, 0),
    "^": Position(0, -1),
    "<": Position(-1, 0),
    "v": Position(0, 1),
}

# Width and height of the valley, counting the walls.
VALLEY_WIDTH = 0
VALLEY_HEIGHT = 0

class Blizzard:
    def __init__(self, pos, dir):
        self.pos = pos
        self.dir = dir

    def nextPos(self):
        global VALLEY_WIDTH
        global VALLEY_HEIGHT
        #n = self.pos + self.dir - Position(1, 1)
        n = Position(1 + (self.pos.x + self.dir.x - 1) % (VALLEY_WIDTH - 2), \
                     1 + (self.pos.y + self.dir.y - 1) % (VALLEY_HEIGHT - 2))
        return n

class Valley:
    def __init__(self, width, height, startPos, exitPos, blizzards):
        # Width and height are not counting the walls.
        self.width = width
        self.height = height
        self.startPos = startPos
        self.exitPos = exitPos
        self.blizzards = blizzards

        self.blizzardsMask = []
        self.__precomputeBlizzardsPos()

    def __precomputeBlizzardsPos(self):
        # The positions occupied by the blizzards repeat itself every [w-2,h-2]
        # minutes.
        mod = math.lcm(self.width - 2, self.height - 2)
        B = copy.deepcopy(self.blizzards)
        for t in range(mod):
            # Compute mask of positions occupied by blizzards.
            mask = [[False] * self.width for _ in range(self.height)]
            for b in B:
                mask[b.pos.y][b.pos.x] = True
            self.blizzardsMask.append(mask)
            B = {Blizzard(b.nextPos(), b.dir) for b in B}

    # Check if a pos `p` at `time` minutes is occupied by a blizzard.
    def posInBlizzard(self, p, time):
        m = math.lcm(self.width - 2, self.height - 2)
        return self.blizzardsMask[time % m][p.y][p.x]

# Parse the input a Valley object.
def parseInput(inputFile):
    fd = open(inputFile, "r")
    y = 0
    width = 0
    startPos = None
    exitPos = None
    blizzards = set()
    for l in fd.readlines():
        width = len(l) - 1
        if y == 0:
            # The top line contains the start position.
            startX = [c[0] for c in enumerate(l) if c[1] == "."][0]
            startPos = Position(startX, 0)
        elif "####" in l:
            # The bottom line contains the exit position.
            exitX = [c[0] for c in enumerate(l) if c[1] == "."][0]
            exitPos = Position(exitX, y)
        for x, c in enumerate(l):
            if c in CHARTODIR.keys():
                blizzards.add(Blizzard(Position(x, y), CHARTODIR[c]))
        y += 1
    height = y
    global VALLEY_WIDTH
    global VALLEY_HEIGHT
    VALLEY_WIDTH = width
    VALLEY_HEIGHT = height
    fd.close()
    blizzards = frozenset(blizzards)
    return Valley(width, height, startPos, exitPos, blizzards)

def findShortestPath(valley, startTime):
    # Check if a Position is within the bounds of the valley.
    def posInBounds(p):
        return p == valley.startPos or p == valley.exitPos or \
               (1 <= p.x <= valley.width - 2 and 1 <= p.y <= valley.height - 2)

    class State:
        def __init__(self, exPos):
            self.numSteps = startTime
            self.exPos = exPos
            self.parent = None

        def __eq__(self, other):
            return self.numSteps == other.numSteps and \
                   self.exPos == other.exPos

        def __hash__(self):
            return hash((self.numSteps, self.exPos))

        # Compute the set of possible next states from this state.
        def nextStates(self):
            nextStates = []
            DIRS = [
                # Stay.
                Position(0, 0),
                # Right.
                Position(1, 0),
                # Down.
                Position(0, 1),
                # Left.
                Position(-1, 0),
                # Up.
                Position(0, -1)
            ]
            for d in DIRS:
                nextPos = self.exPos + d
                if posInBounds(nextPos) and \
                   not valley.posInBlizzard(nextPos, self.numSteps + 1):
                    s = State(nextPos)
                    s.numSteps = self.numSteps + 1
                    nextStates.append(s)
            return nextStates

    startState = State(valley.startPos)

    todo = [startState]
    minPath = 999999

    def h(s):
        return abs(s.exPos.x - valley.exitPos.x) + abs(s.exPos.y - valley.exitPos.y)

    DEF_SCORE = 999999
    gScores = {startState: 0}
    fScores = {startState: h(startState)}
    scores = {startState: 0}

    while len(todo) > 0:
        curr = todo.pop(0)

        if len(todo) > 0:
            assert fScores[curr] <= fScores[todo[0]]

        assert not valley.posInBlizzard(curr.exPos, curr.numSteps)

        #print(f"{curr.exPos} -> {curr.numSteps}")
        if curr.exPos == valley.exitPos:
            minPath = min(minPath, curr.numSteps)
            continue
        elif minPath < curr.numSteps + h(curr):
            # We cannot beat the current shortest path, give up on this path.
            continue

        nextStates = curr.nextStates()
        toAdd = []
        for s in nextStates:
            tentativeScore = gScores[curr] + 1
            if tentativeScore < gScores.get(s, DEF_SCORE):
                gScores[s] = tentativeScore
                fScores[s] = tentativeScore + h(s)
                if s not in todo:
                    toAdd.append(s)
        toAdd.sort(key=lambda s: fScores[s])
        i = 0
        while len(toAdd) > 0:
            s = toAdd.pop(0)
            while i < len(todo) and fScores[todo[i]] <= fScores[s]:
                i += 1
            todo.insert(i, s)
    return minPath

def part1(inputFile):
    valley = parseInput(inputFile)
    return findShortestPath(valley, 0)

def part2(inputFile):
    valley = parseInput(inputFile)
    # Go to the exit
    toExit = findShortestPath(valley, 0)
    # Now go back for the snack, need to swap the start and end positions.
    tmp = valley.startPos
    valley.startPos = valley.exitPos
    valley.exitPos = tmp
    backToStart = findShortestPath(valley, toExit)
    # Now go back to the exit
    tmp = valley.startPos
    valley.startPos = valley.exitPos
    valley.exitPos = tmp
    backToExit = findShortestPath(valley, backToStart)
    return backToExit

if __name__ == "__main__":
    inputFile = sys.argv[1]
    print("Part 1: {}".format(part1(inputFile)))
    print("Part 2: {}".format(part2(inputFile)))
