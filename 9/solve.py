#!/usr/bin/env python

import sys
from enum import Enum

class Direction(Enum):
    Right = 1
    Left = 2
    Up = 4
    Down = 8

class Motion:
    def __init__(self, d, steps):
        self.direction = d
        self.steps = steps

    def __repr__(self):
        return "(" + str(self.direction) + " " + str(self.steps) + ")"

# Converts a char (R, L, U or D) to the corresponding Direction enum.
def charToDirection(char):
    if char == "R":
        return Direction.Right
    elif char == "L":
        return Direction.Left
    elif char == "U":
        return Direction.Up
    elif char == "D":
        return Direction.Down
    else:
        raise Exception("Unknown direction: " + char)

# Read the input file and return a list of the moves to perform.
def parseInput(inputFile):
    fd = open(inputFile, "r")
    lines = fd.readlines()
    moves = []
    for l in lines:
        d, s = l.split(" ")
        motion = Motion(charToDirection(d), int(s))
        moves.append(motion)
    fd.close()
    return moves

# Describe the position (x, y) in the 2D plane.
class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Compute the next position if we move from that position to the given
    # direction.
    def next(self, direction):
        if direction == Direction.Right:
            return Position(self.x+1, self.y)
        elif direction == Direction.Left:
            return Position(self.x-1, self.y)
        elif direction == Direction.Up:
            return Position(self.x, self.y-1)
        elif direction == Direction.Down:
            return Position(self.x, self.y+1)
        else:
            raise Exception("Invalid direction")

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return "(" + str(self.x) + " " + str(self.y) + ")"

# For a given configuration head and tail, compute the next position of the
# tail. Return the Position object.
def updateTail(head, tail):
    # First check if head and tail are touching.
    if abs(head.x - tail.x) <= 1 and abs(head.y - tail.y) <= 1:
        # Head and tail are touching, no need to update the tail. This condition
        # also handles the case where the head and tail are overlapping.
        return Position(tail.x, tail.y)
    
    dx = head.x - tail.x
    dy = head.y - tail.y
    newX = tail.x + ((dx // abs(dx)) if dx != 0 else 0)
    newY = tail.y + ((dy // abs(dy)) if dy != 0 else 0)
    return Position(newX, newY)

def part1(inputFile):
    moves = parseInput(inputFile)

    head = Position(0, 0)
    tail = Position(0, 0)

    # Hold the positions visited by the tail.
    visited = {}
    visited[tail] = True

    for m in moves:
        for s in range(0, m.steps):
            head = head.next(m.direction)
            tail = updateTail(head, tail)
            visited[tail] = True

    return len(visited.keys())

def part2(inputFile):
    moves = parseInput(inputFile)

    numKnots = 10
    knots = [Position(0, 0) for i in range(0, numKnots)]

    # Hold the positions visited by the tail.
    visited = {}
    visited[knots[-1]] = True

    for m in moves:
        for s in range(0, m.steps):
            knots[0] = knots[0].next(m.direction)
            for i in range(1, numKnots):
                knots[i] = updateTail(knots[i-1], knots[i])
            visited[knots[-1]] = True

    return len(visited.keys())

if __name__ == "__main__":
    inputFile = sys.argv[1]
    print("Part 1: {}".format(part1(inputFile)))
    print("Part 2: {}".format(part2(inputFile)))
