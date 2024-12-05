#!/bin/python3

import sys

lines = list(map(lambda l: l.replace("\n", ""),
                 open(sys.argv[1], "r").readlines()))

def search_part1(lines, x, y, pattern):
    if lines[y][x] != pattern[0]:
        return 0
    matches = 0
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            if abs(dy) + abs(dx) == 0:
                continue
            for n in range(1, len(pattern)):
                px = x + n * dx
                py = y + n * dy
                if py < 0 or py >= len(lines) or px < 0 or px >= len(lines[py]):
                    break
                if lines[py][px] != pattern[n]:
                    break
                elif n == len(pattern) - 1: 
                    matches += 1
    return matches

part1 = 0
for y in range(len(lines)):
    for x in range(len(lines[y])):
        part1 += search_part1(lines, x, y, "XMAS")
print(f"Part 1: {part1}")

def search_part2(lines, x, y):
    if lines[y][x] != "A":
        return 0
    d1 = lines[y-1][x-1] + "A" + lines[y+1][x+1]
    d2 = lines[y+1][x-1] + "A" + lines[y-1][x+1]
    if (d1 == "MAS" or d1 == "SAM") and (d2 == "MAS" or d2 == "SAM"):
        return 1
    else:
        return 0

part2 = 0
for y in range(1, len(lines) - 1):
    for x in range(1, len(lines[y]) - 1):
        part2 += search_part2(lines, x, y)
print(f"Part 2: {part2}")
