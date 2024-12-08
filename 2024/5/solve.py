#!/bin/python3

# Nasty stuff. Had to write it in a hurry.

import sys

fd = open(sys.argv[1], "r")

rules = {}

line = fd.readline()
while line != "\n":
    line = line.replace("\n", "")
    assert "|" in line
    left, right = line.split("|")
    left, right = int(left), int(right)
    if left in rules.keys():
        rules[left].append(right)
    else:
        rules[left] = [right]
    line = fd.readline()

def valid(updated_pages, curr):
    if curr not in rules.keys():
        # No ordering constraints to add the current page, so far this is a
        # valid sequence.
        return True
    else:
        for p in updated_pages:
            if p in rules[curr]:
                return False
        return True

part1 = 0

lines = fd.readlines()
lines = list(map(lambda l: l.replace("\n", ""), lines))

for line in lines:
    # Process new rule
    pages = list(map(lambda e: int(e), line.split(",")))
    valid_update = True
    for i in range(len(pages)):
        if not valid(pages[:i], pages[i]):
            valid_update = False
            break
    if valid_update:
        part1 += pages[len(pages) // 2]
print(f"Part 1: {part1}")

def fixup(pages):
    for i in range(1, len(pages)):
        for j in range(i):
            pj, pi = pages[j], pages[i]
            if pi in rules.keys() and pj in rules[pi]:
                # The ordering "pi appears before pj" is violated. Insert pi
                # before pj.
                pages.pop(i)
                pages.insert(j, pi)
                break
    return pages 

part2 = 0
lines = list(
        map(
            lambda l: list(map(lambda e: int(e), l.split(","))),
            lines))
for pages in lines:
    # Process new rule
    valid_update = True
    for i in range(len(pages)):
        if not valid(pages[:i], pages[i]):
            valid_update = False
            break
    if not valid_update:
        fixed = fixup(pages)
        part2 += fixed[len(fixed) // 2]
print(f"Part 2: {part2}")
