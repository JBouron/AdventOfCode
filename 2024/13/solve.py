#!/bin/python3

import sys
from dataclasses import dataclass

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

INF = (1 << 32)

@dataclass
class Machine:
    buttonA: Pos2d
    buttonB: Pos2d
    prize: Pos2d

    def solve(self):
        cache = {}
        def helper(x, y, pressesA, pressesB):
            key = (x, y)
            if key in cache.keys():
                return cache[key]
            if pressesA > 100 or pressesB > 100:
                return INF
            elif x == self.prize.x and y == self.prize.y:
                return 0
            elif x > self.prize.x or y > self.prize.y:
                # Assumption, buttons can never have negative offsets, hence we
                # can already give up this attempt.
                return INF

            res = min(
                3 + helper(x + self.buttonA.x, y + self.buttonA.y, pressesA + 1, pressesB),
                1 + helper(x + self.buttonB.x, y + self.buttonB.y, pressesA, pressesB + 1)
            )
            cache[key] = res
            return res
        return min(helper(0, 0, 0, 0), INF)

def parse_button(line):
    parts = line.split("+")
    y = int(parts[2])
    x = int(parts[1].split(",")[0])
    return Pos2d(x, y)

def parse_input(filename):
    fd = open(filename, "r")
    lines = fd.readlines()
    res = []
    while len(lines):
        ba = parse_button(lines.pop(0))
        bb = parse_button(lines.pop(0))
        bp = lines.pop(0)
        if len(lines):
            # Remove new lines
            lines.pop(0)
        parts = bp.split("=")
        y = int(parts[2])
        x = int(parts[1].split(",")[0])
        prize = Pos2d(x, y)
        res.append(Machine(ba, bb, prize))
    return res

machines = parse_input(sys.argv[1])

part1 = 0
for m in machines:
    s = m.solve()
    if s != INF:
        part1 += s
print(f"Part 1: {part1}")
