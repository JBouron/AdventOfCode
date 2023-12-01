#!/usr/bin/env python

import sys

def readStream(inputFile):
    return open(inputFile, "r").readlines()[0].replace("\n", "")

def findMarker(stream, markerLen):
    # Read the stream and find the first marker (e.g. sequence of distinct
    # chars) that is of length `markerLen` characters.
    # Return 0 if no such marker exists.
    def isMarker(chars):
        # Return True if the str chars is a marker, False otherwise.
        return len(set(chars)) == markerLen

    for i in range(len(stream) - markerLen + 1):
        chars = stream[i:i+markerLen]
        if isMarker(chars):
            # This is a marker, we are done here.
            return i + markerLen

    # The puzzle does not seem to give a stream without a marker. So not really
    # necessary here.
    return 0

def findPacketStartMarker(stream):
    # Get the first packet start marker in the stream.
    # Returns the index of the beginning of the message after the marker.
    # Return 0 if no such marker exists.
    return findMarker(stream, 4)

def findMessageStartMarker(stream):
    # Get the first message start marker in the stream.
    # Returns the index of the beginning of the message after the marker.
    # Return 0 if no such marker exists.
    return findMarker(stream, 14)

def part1(inputFile):
    stream = readStream(inputFile)
    return findPacketStartMarker(stream)

def part2(inputFile):
    stream = readStream(inputFile)
    return findMessageStartMarker(stream)

if __name__ == "__main__":
    inputFile = sys.argv[1]
    print("Part 1: {}".format(part1(inputFile)))
    print("Part 2: {}".format(part2(inputFile)))
