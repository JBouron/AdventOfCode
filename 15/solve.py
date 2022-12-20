#!/usr/bin/env python

import sys
import copy
import re
import math

# A position (x, y) in the 2D grid.
class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return str((self.x, self.y))

    # Compute the Manhattan distance between this point and other.
    def dist(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

# Class holding information about a sensor.
class Sensor:
    # `pos` is the sensor's position. `nearestBeacon` is the position of the
    # beacon that is nearest to this sensor, as indicated in the input file.
    def __init__(self, pos, nearestBeacon):
        # The position of the sensor.
        self.pos = copy.copy(pos)
        # The position of the nearest beacon.
        self.beacon = copy.copy(nearestBeacon)
        # The manhattan distance between the sensor and its nearest beacon. This
        # indicates the radius around the sensor in which there cannot be a
        # beacon.
        self.dist = pos.dist(nearestBeacon)

    def __repr__(self):
        return "Sensor, pos = {}, dist = {}".format(self.pos, self.dist)

# Parse the input and return a set of sensors.
def parseInput(inputFile):
    fd = open(inputFile, "r")
    sensors = set()
    for l in fd.readlines():
        coords = re.findall("-?[0-9]+", l)
        coords = list(map(lambda c: int(c), coords))
        sensorPos = Position(coords[0], coords[1])
        beaconPos = Position(coords[2], coords[3])
        sensors.add(Sensor(sensorPos, beaconPos))
    fd.close()
    return sensors

def part1(inputFile):
    sensors = parseInput(inputFile)
    Y = 2000000
    Xs = set()
    # Solve for x the eq |x - s.pos.x| + |Y - s.pos.y| = s.dist. Add all such x
    # in a set. The set makes sure that we are not double counting in case two
    # sensors have their radius overlapping.
    for s in sensors:
        Xs |= set(range(s.pos.x, s.dist - abs(Y - s.pos.y) + s.pos.x + 1))
        Xs |= set(range(abs(Y - s.pos.y) + s.pos.x - s.dist, s.pos.x))
        # Make sure not to count the beacons.
        Xs -= set([s.beacon.x] if s.beacon.y == Y else [])

    return len(Xs)

def part2(inputFile):
    sensors = parseInput(inputFile)

    # We know that there is only one position p so that for all sensor si,
    # dist(p, si.pos) > si.dist.
    # Also, because there is only a single such p, this position must be
    # "surrounded" by sensors, like as follows:
    #    #####*##S##*####S##*
    #    *###*#######*#######
    #    #*#*#########*#####*
    #    ##*#########*#*###*#
    #    S#**#######*#*.*#*##
    #    #*#**#####*###*#*###
    #    *###**###*#####*####
    #    #####**#*###S###**##
    #    ######**#*#####**#*#
    #    #######**S*###**###*
    # '.' indicates the position p, '*' are the perimeter of the sensors radius.
    # Therefore p must lie on the periphery of multiple sensors (typically 4).
    # The periphery of a sensor si is defined as the set of points that are at a
    # distance of si.dist+1 from si.pos.
    # So what we do here is that we compute the lines that make the periphery of
    # each sensor' lozenge. We don't bother computing the start and end of such
    # line, instead we express all such lines as a*x + b. Then we compute all
    # the intersections of all such lines and for each intersection we check if
    # it lies withing a sensor's lozenge. If not then this is the position we
    # were looking for.
    # Note that this does not work if the position we are looking for resides on
    # the edge of the searchable area for instance at (0, 0). But it does not
    # seem to be the case.
    diagonals = set()
    for s in sensors:
        diagonals.add((1, s.dist - s.pos.x + s.pos.y + 1))
        diagonals.add((1, -s.dist - s.pos.x + s.pos.y - 1))
        diagonals.add((-1, s.dist + s.pos.x + s.pos.y + 1))
        diagonals.add((-1, -s.dist + s.pos.x + s.pos.y - 1))

    Ymax = 4000000
    Xmax = Ymax
    candidates = set()
    for d in diagonals:
        for o in diagonals:
            if d == o or d[0] == o[0]:
                continue

            #    d0*x + d1 == o0*x + o1
            # => (d0 - o0)*x = o1 - d1
            # => x = (o1-d1)/(d0-o0).
            x1 = math.ceil((o[1]-d[1])/(d[0]-o[0]))
            y1 = d[0] * x1 + d[1]
            x2 = (o[1]-d[1])//(d[0]-o[0])
            y2 = d[0] * x2 + d[1]

            if 0 <= x1 <= Xmax and 0 <= y1 <= Ymax:
                candidates.add(Position(x1, y1))
            if 0 <= x2 <= Xmax and 0 <= y2 <= Ymax:
                candidates.add(Position(x2, y2))

    def findSensorForPos(pos):
        for s in sensors:
            if pos.dist(s.pos) <= s.dist:
                return s
        return None

    for c in candidates:
        if findSensorForPos(c) is None:
           return c.x * 4000000 + c.y
    assert False

if __name__ == "__main__":
    inputFile = sys.argv[1]
    print("Part 1: {}".format(part1(inputFile)))
    print("Part 2: {}".format(part2(inputFile)))
