#!/bin/python3

# This is some poorly written inefficient python code due to the fact that I had
# a late start and needed to quickly catch-up.

import sys

reports = list(filter(lambda l: len(l) > 0, open(sys.argv[1], "r").read().split("\n")))
reports = list(map(lambda l: l.split(), reports))

def is_safe(report):
    prev = int(report[0])
    # -1 -> decreasing
    # 0  -> unknown
    # 1  -> increasing
    trend = 0
    for i in range(1, len(report)):
        curr = int(report[i])
        diff = curr - prev
        curr_trend = (diff / abs(diff)) if diff != 0 else 0
        if (not (1 <= abs(diff) <= 3)) or (trend != 0 and trend != curr_trend):
            return False
        trend = curr_trend
        prev = curr
    return True

sol = 0
for r in reports:
    if is_safe(r):
        sol += 1
print(f"Part 1: {sol}")

sol = 0
for r in reports:
    if is_safe(r):
        sol += 1
    else:
        # This is probably the worst code I have ever written in my life...
        for i in range(len(r)):
            rc = r.copy()
            del rc[i]
            if is_safe(rc):
                sol += 1
                break
print(f"Part 2: {sol}")
