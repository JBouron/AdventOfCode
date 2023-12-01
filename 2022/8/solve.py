#!/usr/bin/env python

import sys

def parseInput(inputFile):
    fd = open(inputFile, "r")
    lines = fd.readlines()

    grid = []
    for l in lines:
        grid.append([int(x) for x in l.replace("\n","")])
    fd.close()
    return grid

def part1(inputFile):
    grid = parseInput(inputFile)
    gridWidth = len(grid[0])
    gridHeight = len(grid)

    numBorderTrees = 2 * gridWidth + 2 * (gridHeight - 2)
    # Number of trees visible in the grid.
    numVisible = numBorderTrees
    for y in range(1, gridHeight - 1):
        for x in range(1, gridWidth - 1):
            # The height of the tree.
            h = grid[y][x]
            # Compute the height of the trees in all four directions.
            l = grid[y][:x]
            r = grid[y][x+1:]
            t = [grid[i][x] for i in range(0, y)]
            b = [grid[i][x] for i in range(y + 1, gridHeight)]
            isVisible = max(l) < h or max(r) < h or max(t) < h or max(b) < h
            if isVisible:
                numVisible += 1
    return numVisible

def part2(inputFile):
    grid = parseInput(inputFile)
    gridWidth = len(grid[0])
    gridHeight = len(grid)

    maxScore = 0
    # Since trees on the edge have at least one of their viewing distances be 0,
    # their scores will be 0 as well so we can skip them.
    for y in range(1, gridHeight - 1):
        for x in range(1, gridWidth - 1):
            # The height of the tree.
            h = grid[y][x]
            # Compute the height of the trees in all four directions.
            l = grid[y][:x]
            r = grid[y][x+1:]
            t = [grid[i][x] for i in range(0, y)]
            b = [grid[i][x] for i in range(y + 1, gridHeight)]
            
            # Quick and dirty!
            # For each direction we compute the index of the first tree that is
            # taller than the current tree.
            def getViewingDistance(viewVec, maxHeight):
                # First crop the viewVec so that it only contains trees up to
                # the first tree that is >= maxHeight.
                a = []
                # This is nasty.
                for t in viewVec:
                    if t < maxHeight:
                        a.append(t)
                    else:
                        break
                # If the tree has an unobstructed view (e.g. no tree was >=
                # maxHeight) then the viewing distance is len(a) otherwise it 
                # is len of a + 1 since it sees the tree that is >= maxHeight.
                if len(a) == len(viewVec):
                    # No tree was >= maxHeight
                    return len(a)
                else:
                    return len(a) + 1

            # Reverse the top and bottom viewing directions, so that array[0]
            # becomes the closest tree in that direction. This means that we can
            # use the same logic as with right and bottom.
            l.reverse()
            t.reverse()

            lvd = getViewingDistance(l, h)
            rvd = getViewingDistance(r, h)
            tvd = getViewingDistance(t, h)
            bvd = getViewingDistance(b, h)

            maxScore = max(maxScore, lvd * rvd * tvd * bvd)
    return maxScore

if __name__ == "__main__":
    inputFile = sys.argv[1]
    print("Part 1: {}".format(part1(inputFile)))
    print("Part 2: {}".format(part2(inputFile)))
