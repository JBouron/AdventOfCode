#!/usr/bin/env python

import sys
import re

# A position (x, y, z) in the 3D space.
class Position:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __repr__(self):
        return str((self.x, self.y, self.z))

# Return list of 3D position.
def parseInput(inputFile):
    fd = open(inputFile, "r")
    p = fd.readlines()
    p = list(map(lambda l: re.findall("[0-9]+", l), p))
    p = list(map(lambda c: Position(int(c[0]), int(c[1]), int(c[2])), p))
    fd.close()
    return p

def part1(inputFile):
    cubes = parseInput(inputFile)
    area = 0
    for c in cubes:
        neighbours = [
            Position(c.x+1, c.y, c.z),
            Position(c.x-1, c.y, c.z),
            Position(c.x, c.y+1, c.z),
            Position(c.x, c.y-1, c.z),
            Position(c.x, c.y, c.z+1),
            Position(c.x, c.y, c.z-1),
        ]
        for n in neighbours:
            if n not in cubes:
                area += 1
    return area

def part2(inputFile):
    cubes = parseInput(inputFile)

    maxX = max([p.x for p in cubes]) + 1
    minX = min([p.x for p in cubes]) - 1
    maxY = max([p.y for p in cubes]) + 1
    minY = min([p.y for p in cubes]) - 1
    maxZ = max([p.z for p in cubes]) + 1
    minZ = min([p.z for p in cubes]) - 1

    def inBounds(p):
        return minX <= p.x <= maxX and minY <= p.y <= maxY and minZ <= p.z <= maxZ

    root = Position(maxX, maxY, maxZ)
    reachable = set()
    area = 0


    visited = set([root])
    q = [root]
    while len(q) > 0:
        curr = q.pop(0)

        c = curr
        neighbours = [
            Position(c.x+1, c.y, c.z),
            Position(c.x-1, c.y, c.z),
            Position(c.x, c.y+1, c.z),
            Position(c.x, c.y-1, c.z),
            Position(c.x, c.y, c.z+1),
            Position(c.x, c.y, c.z-1),
        ]
        neighbours = list(filter(lambda n: inBounds(n) and n not in visited, neighbours))
        for n in neighbours:
            if n in cubes:
                area += 1
            else:
                visited.add(n)
                q.append(n)

    return area

if __name__ == "__main__":
    inputFile = sys.argv[1]
    print("Part 1: {}".format(part1(inputFile)))
    print("Part 2: {}".format(part2(inputFile)))
