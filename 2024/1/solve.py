#!/bin/python3

# This is some poorly written inefficient python code due to the fact that I had
# a late start and needed to quickly catch-up.

import sys

puzzle_input = list(filter(lambda l: len(l) > 0, open(sys.argv[1], "r").read().split("\n")))
left = sorted(list(map(lambda e: int(e.split()[0]), puzzle_input)))
right = sorted(list(map(lambda e: int(e.split()[1]), puzzle_input)))
sol = 0
for i in range(len(left)):
    sol += abs(left[i] - right[i])

print(f"Part 1: {sol}")

freq = {}
for e in right:
    freq[e] = freq.get(e, 0) + 1

sol = 0
for e in left:
    sol += e * freq.get(e, 0)
print(f"Part 2: {sol}")
