#!/bin/python3

import sys

def processSet(s):
    # s is of the form "N color, M color"
    res = {"red": 0, "green": 0, "blue":0}
    for p in s.split(","):
        num, color = p.strip().split(" ")
        res[color] = int(num)
    return res

if __name__ == "__main__":
    fd = open(sys.argv[1], "r")
    part1 = 0
    part2 = 0
    for line in fd.readlines():
        parts = line.split(":")
        gameId = int(parts[0].split(" ")[1])
        sets = list(map(lambda s: processSet(s), parts[1].split(";")))
        part1Possible = True
        minReds = max([s["red"] for s in sets])
        minGreen = max([s["green"] for s in sets])
        minBlue = max([s["blue"] for s in sets])
        for s in sets:
            if s["red"] > 12 or s["green"] > 13 or s["blue"] > 14:
                part1Possible = False
                break
        if part1Possible:
            part1 += gameId
        part2 += minReds * minGreen * minBlue
    print("Part 1: {}".format(part1))
    print("Part 2: {}".format(part2))

