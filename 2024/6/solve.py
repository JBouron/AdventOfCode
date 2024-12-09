#!/bin/python3

import sys

fd = open(sys.argv[1], "r")
lines = list(map(lambda l: l.replace("\n", ""), fd.readlines()))
grid = list(filter(lambda l: len(l) > 0, lines))
grid = list(map(lambda l: list(l), grid))
fd.close()

def find_guard(grid):
    guard_orientations = ["^", "<", ">", "v"]
    for y, row in enumerate(grid):
        for o in guard_orientations:
            try:
                x = row.index(o)
                return (y, x)
            except:
                pass

startY, startX = find_guard(grid)
currY, currX = find_guard(grid)

delta_YX = {
    "^": (-1, 0),
    "<": (0, -1),
    ">": (0, 1),
    "v": (1, 0),
}

def rotated(guard):
    r = {
        "^": ">",
        "<": "^",
        ">": "v",
        "v": "<",
    }
    return r[guard]

visited = set()

part1 = 0
while 0 <= currY < len(grid) and 0 <= currX < len(grid[currY]):
    if (currY, currX) not in visited:
        part1 += 1
        visited.add((currY, currX))
    g = grid[currY][currX]
    dy, dx = delta_YX[g]
    nextY, nextX = currY + dy, currX + dx
    step = False
    if 0 <= nextY < len(grid) and 0 <= nextX < len(grid[nextY]) and grid[nextY][nextX] == "#":
        # Stay in same spot and rotate to the right.
        grid[currY][currX] = rotated(g)
    elif 0 <= nextY < len(grid) and 0 <= nextX < len(grid[nextY]):
        grid[nextY][nextX] = g
        currY, currX = nextY, nextX
    else:
        currY, currX = nextY, nextX
print(f"Part 1: {part1}")

# Brute force.
part2 = 0
for ny in range(len(grid)):
    for nx in range(len(grid[0])):
        if ny == startY and nx == startX:
            continue
        fd = open(sys.argv[1], "r")
        lines = list(map(lambda l: l.replace("\n", ""), fd.readlines()))
        grid = list(filter(lambda l: len(l) > 0, lines))
        grid = list(map(lambda l: list(l), grid))
        fd.close()

        grid[ny][nx] = "#"

        currY, currX = find_guard(grid)
        startO = grid[currY][currX]
        visited = {}

        steps = 0
        while 0 <= currY < len(grid) and 0 <= currX < len(grid[currY]):
            g = grid[currY][currX]
            if (currY, currX) in visited.keys() and g in visited[(currY, currX)]:
                part2 += 1
                break

            if (currY, currX) in visited.keys():
                visited[(currY, currX)].append(g)
            else:
                visited[(currY, currX)] = [g]
            dy, dx = delta_YX[g]
            nextY, nextX = currY + dy, currX + dx
            step = False
            if 0 <= nextY < len(grid) and 0 <= nextX < len(grid[nextY]) and grid[nextY][nextX] == "#":
                # Stay in same spot and rotate to the right.
                grid[currY][currX] = rotated(g)
            elif 0 <= nextY < len(grid) and 0 <= nextX < len(grid[nextY]):
                grid[nextY][nextX] = g
                currY, currX = nextY, nextX
            else:
                currY, currX = nextY, nextX
            steps += 1
print(f"Part 2: {part2}")
