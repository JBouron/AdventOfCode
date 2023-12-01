#!/usr/bin/env python

import sys
import re

def parseInput(inputFile):
    fd = open(inputFile, "r")
    nums = []
    for l in fd.readlines():
        nums.append(int(re.findall("-?[0-9]+", l)[0]))
    return nums

# Find the response for part 1 and part 2. Set decryptionKey to 1 for part 1.
# This is not very efficient, I'll prob go back to this in the future to find a
# better solution (insert "... and other jokes you can tell yourself" meme
# here).
def find(inputFile, decryptionKey):
    nums = parseInput(inputFile)
    nums = list(map(lambda n: n * decryptionKey, nums))
    # Keep track of the original index of each number in the mixed list.
    indices = list(range(len(nums)))

    assert len(list(filter(lambda n: n == 0, nums))) == 1

    for _ in range(10 if decryptionKey != 1 else 1):
        N = len(nums)
        for mixRound in range(N):
            i = list(filter(lambda e: e[1] == mixRound, enumerate(indices)))
            assert len(i) == 1
            i, k = i[0]

            v = nums.pop(i)
            j = (i + v) % len(nums)
            if j == 0:
                j = len(nums)
            nums.insert(j,v)

            indices.pop(i)
            indices.insert(j,k)
    # Find 0.
    zeroIdx = list(filter(lambda p: p[1] == 0, enumerate(nums)))[0][0]
    l = len(nums)
    return nums[(zeroIdx+1000)%l] + nums[(zeroIdx+2000)%l] + nums[(zeroIdx+3000)%l]

def part1(inputFile):
    return find(inputFile, 1)

def part2(inputFile):
    return find(inputFile, 811589153)

if __name__ == "__main__":
    inputFile = sys.argv[1]
    print("Part 1: {}".format(part1(inputFile)))
    print("Part 2: {}".format(part2(inputFile)))
