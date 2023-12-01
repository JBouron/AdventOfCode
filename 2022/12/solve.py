#!/usr/bin/env python

import sys

# 2D coordinates in the height map.
class Position:
    # Create a Position value for coordinates (x, y)
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Compare two Positions.
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

# Keep state of a height map and allows to compute shortest distances between
# starting points and the end position.
class HeightMap:
    def __init__(self, heights, start, end):
        self.map = heights
        self.start = start
        self.end = end
        self.width = len(self.map[0])
        self.height = len(self.map)
        # A grid that, for each position (x, y), keeps track of the minimum
        # number of steps required to reach the end position.
        self.distance = self._computeDistGrid()

    # Compute the minimum number of steps required to go from any position to
    # the end position. Returns a 2D grid such that grid[y][x] is the minimum
    # number of steps required to go from (x, y) to self.end.
    def _computeDistGrid(self):
        # The "infinite" distance.
        inf = 9999999
        # Distance grid. For each position (x, y) this keeps track of the number
        # of steps required to go from (x, y) to self.end. A value of inf
        # indicates that there is no path (yet).
        dist = [[inf for x in range(self.width)] for y in range(self.height)]
        # Keeps track of the cells that were visited or not.
        visited = [[False for x in range(self.width)] for y in range(self.height)]

        # For a given position, return a list of reachable, unvisited
        # neighbours. Reachable here means that a step can be taken from the
        # neighbour to pos (e.g. the height of pos is at most one higher than
        # the height of the neighbour).
        def reachableUnvisitedNeighbours(pos):
            l = Position(pos.x-1, pos.y)
            r = Position(pos.x+1, pos.y)
            t = Position(pos.x, pos.y-1)
            b = Position(pos.x, pos.y+1)
            neigh = [l, r, t, b]
            res = []
            for n in neigh:
                if n.x < 0 or n.y < 0 or self.width <= n.x or self.height <= n.y:
                    # This happens if pos was on the edge, in this case this is
                    # not a valid neighbour and we can skip.
                    continue
                elif visited[n.y][n.x]:
                    # The neighbour was already visited, skip.
                    continue
                elif self.map[pos.y][pos.x] - self.map[n.y][n.x] > 1:
                    # Neighbour is too low compared to pos, e.g. not possible to
                    # move from neighbour to pos. Skip.
                    continue
                else:
                    # Neighbour is valid, not visited, and moving from neighbour
                    # to pos is allowed, return it.
                    res.append(n)
            return res

        # The set of positions to be visited. Sorted on their distance. We start
        # with the end position, for which we set the distance to 0.
        toVisit = [self.end]
        dist[self.end.y][self.end.x] = 0
        # Visit all the nodes.
        while len(toVisit) > 0:
            # The pos we are visiting.
            pos = toVisit.pop(0)
            # Sanity checks, we can only visit a position for which there is a
            # known min distance.
            assert not visited[pos.y][pos.x]
            assert dist[pos.y][pos.x] != inf

            # Mark this position as visited.
            visited[pos.y][pos.x] = True

            # Check each unvisited and reachable neighbour and update their
            # distance accordingly. Add them to toVisit.
            neighs = reachableUnvisitedNeighbours(pos)
            for n in neighs:
                if dist[pos.y][pos.x] + 1 < dist[n.y][n.x]:
                    # We found a shorter path to the neighbour, update it.
                    dist[n.y][n.x] = dist[pos.y][pos.x] + 1
                    if n not in toVisit:
                        toVisit.append(n)

            # Keep toVisit sorted so that the first element is always the one
            # with the smallest distance to end.
            toVisit.sort(key=lambda p: dist[p.y][p.x])

        return dist

    # Return the minimum number of steps required to go from the starting
    # position to the end position.
    def minStepsFromStart(self):
        return self.distance[self.start.y][self.start.x]

    # Considers all cells with elevation 0 (e.g. height = 'a' in input) and
    # return the fewest steps required to go from any cell with elevation 0 to
    # the end position.
    def minStepsFromElevation0(self):
        minElevationPos = []
        # There must be a cleaner way to do this ...
        for y in range(self.height):
            for x in range(self.width):
                if self.map[y][x] == 0:
                    minElevationPos.append(Position(x, y))
        minSteps = [self.distance[p.y][p.x] for p in minElevationPos]
        return min(minSteps)

# Parse the input file and returns the corresponding HeightMap.
def parseInput(inputFile):
    fd = open(inputFile, "r")
    lines = fd.readlines()
    startPos = None
    endPos = None
    grid = []
    for row in lines:
        row = row.replace("\n", "")
        startX = row.find("S")
        if startX != -1:
            # We found the starting position.
            assert startPos is None
            startPos = Position(startX, len(grid))
            row = row.replace("S", "a")
        endX = row.find("E")
        if endX != -1:
            # We found the end position.
            assert endPos is None
            endPos = Position(endX, len(grid))
            row = row.replace("E", "z")
        heights = [ord(c) - ord('a') for c in row]
        grid.append(heights)
    fd.close()
    return HeightMap(grid, startPos, endPos)

def part1(inputFile):
    hm = parseInput(inputFile)
    return hm.minStepsFromStart()

def part2(inputFile):
    hm = parseInput(inputFile)
    return hm.minStepsFromElevation0()

if __name__ == "__main__":
    inputFile = sys.argv[1]
    print("Part 1: {}".format(part1(inputFile)))
    print("Part 2: {}".format(part2(inputFile)))
