#!/bin/python3

import sys
from dataclasses import dataclass

@dataclass
class CalibrationEquation:
    target: int
    operands: list[int]

    def is_solvable(self, part2: bool) -> bool:
        def inner(acc: int, l: list[int]) -> bool:
            if len(l) == 0:
                return acc == self.target
            else:
                next_op = l[0]
                mul = acc * next_op
                if mul <= self.target and inner(mul, l[1:]):
                    return True
                add = acc + next_op
                if add <= self.target and inner(add, l[1:]):
                    return True
                cat = int(str(acc) + str(next_op))
                if part2 and cat <= self.target and inner(cat, l[1:]):
                    return True
                return False
        return inner(self.operands[0], self.operands[1:])

equations = []
fd = open(sys.argv[1], "r")
for line in fd:
    line = line.replace("\n", "")
    left, right = line.split(": ")
    target = int(left)
    operands = list(map(lambda e: int(e), right.split()))
    equations.append(CalibrationEquation(target, operands))

part1 = sum(
            map(
                lambda e: e.target,
                filter(
                    lambda e: e.is_solvable(False),
                    equations)
                )
            )
print(f"Part 1: {part1}")

part2 = sum(
            map(
                lambda e: e.target,
                filter(
                    lambda e: e.is_solvable(True),
                    equations)
                )
            )
print(f"Part 2: {part2}")
