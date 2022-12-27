#!/usr/bin/env python

import sys

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

North = Position(0, 1)
South = Position(0, -1)
West = Position(-1, 0)
East = Position(1, 0)
DirProposal = [
    (West + North, North, North + East),
    (West + South, South, South + East),
    (West + North, West, West + South),
    (East + North, East, East + South)
]

# Parse the input, returs the list of elves positions.
def parseInput(inputFile):
    fd = open(inputFile, "r")
    elves = []
    y = 0
    lines = fd.readlines()
    lines.reverse()
    for l in lines:
        for x, c in enumerate(l):
            if c == "#":
                elves.append(Position(x, y))
        y += 1

    fd.close()
    return elves

def part1(inputFile):
    elves = parseInput(inputFile)
    # Run the rounds.
    for _ in range(10):
        def propose(p):
            def needProposal(p):
                for y in range(p.y - 1, p.y + 2):
                    for x in range(p.x - 1, p.x + 2):
                        candidate = Position(x, y)
                        if candidate != p and candidate in elves:
                            return True
                return False
            if not needProposal(p):
                return (p, p)
            else:
                for l, d, r in DirProposal:
                    if (l + p) not in elves and \
                       (d + p) not in elves and \
                       (r + p) not in elves:
                        return (d + p, p)
                return (p, p)
        
        proposals = {propose(p) for p in elves}
        numProp = {}
        for p in proposals:
            numProp[p[0]] = numProp.get(p[0], 0) + 1
        elves = {(p[0] if numProp[p[0]] == 1 else p[1]) for p in proposals}

        DirProposal.append(DirProposal.pop(0))

    # Count the empty tiles.
    xMin = min([p.x for p in elves])
    xMax = max([p.x for p in elves])
    yMin = min([p.y for p in elves])
    yMax = max([p.y for p in elves])
    count = 0
    for y in range(yMin, yMax + 1):
        for x in range(xMin, xMax + 1):
            if Position(x, y) not in elves:
                count += 1
    return count


def part2(inputFile):
    global DirProposal
    DirProposal = [
        (West + North, North, North + East),
        (West + South, South, South + East),
        (West + North, West, West + South),
        (East + North, East, East + South)
    ]
    elves = parseInput(inputFile)
    # Run the rounds.
    numRounds = 0
    done = False
    while not done:
        numRounds += 1

        def propose(p):
            def needProposal(p):
                for y in range(p.y - 1, p.y + 2):
                    for x in range(p.x - 1, p.x + 2):
                        candidate = Position(x, y)
                        if candidate != p and candidate in elves:
                            return True
                return False
            if not needProposal(p):
                return (p, p)
            else:
                for l, d, r in DirProposal:
                    if (l + p) not in elves and \
                       (d + p) not in elves and \
                       (r + p) not in elves:
                        return (d + p, p)
                return (p, p)
        
        proposals = {propose(p) for p in elves}
        numProp = {}
        for p in proposals:
            numProp[p[0]] = numProp.get(p[0], 0) + 1

        done = True
        def getNextPos(pair):
            nonlocal done
            if numProp[pair[0]] == 1:
                if pair[0] != pair[1]:
                    done = False
                return pair[0]
            else:
                return pair[1]
        elves = {getNextPos(p) for p in proposals}

        DirProposal.append(DirProposal.pop(0))

    return numRounds

if __name__ == "__main__":
    inputFile = sys.argv[1]
    print("Part 1: {}".format(part1(inputFile)))
    print("Part 2: {}".format(part2(inputFile)))
