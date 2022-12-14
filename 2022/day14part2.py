#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advent of Code 2022, Day 14, Part 2.

Same rock formation as Part 1, but add a floor to catch the sand (no "into the
abyss"). Instead, pour until the sand reaches the top, the start location at
(500,0).


Created on Wed Dec 14 05:56:30 2022

@author: rpoepa
"""
import time
import numpy as np

tic = time.perf_counter()
Infinity = 99999  # Use for "impossibly large integer"
# First read in the rock paths
rockpaths = []
with open('input/input.2022day14.txt', 'r') as f:
#with open('input/test.2022day14.txt', 'r') as f:
    for line in f:
        pathstr = line.strip().replace('->',' ').split()
        path = []
        for pair in pathstr:
            xy = pair.split(',')
            path.append([int(xy[0]), int(xy[1])])
        rockpaths.append(path)

# Determine limits of the grid
xmin = Infinity
xmax = -Infinity
ymin = Infinity
ymax = -Infinity
for path in rockpaths:
    for xy in path:
        xmin = min(xmin, xy[0])
        xmax = max(xmax, xy[0])
        ymin = min(ymin, xy[1])
        ymax = max(ymax, xy[1])

ymin = 0   # Force extra rows at the top

# Add the floor. These calculations allow for a diagonal going in either
# direction from (500, 0), plus a few points for margin
xmin_save = xmin  # Save these for final output
xmax_save = xmax
xmin = min(500 - (ymax - ymin + 5), xmin)
xmax = max(500 + (ymax - ymin + 5), xmax)
ymax += 2
rockpaths.append([[xmin,ymax],[xmax,ymax]])

# Convenience function for coordinate transformation
xy_to_ij = lambda xy: (xy[1] - ymin, xy[0] - xmin)
    
# Build grid and trace paths
width = xmax - xmin + 1
height = ymax - ymin + 1
grid = [['.']*width for _ in range(height)]
for path in rockpaths:
    ij0 = xy_to_ij(path[0])
    for point in path[1:]:
        ij1 = xy_to_ij(point)
        di = np.sign(ij1[0] - ij0[0])  # One of these is always 0
        dj = np.sign(ij1[1] - ij0[1])
        i = ij0[0]
        j = ij0[1]
        while i != ij1[0] or j != ij1[1]:
            grid[i][j] = '#'
            i += di
            j += dj
        grid[ij1[0]][ij1[1]] = '#'  # Add the endpoint
        ij0 = ij1


for row in grid:
    print(''.join(row))
toc = time.perf_counter()

print(f'Time to build map = {(toc - tic) * 1000} ms')

toc = time.perf_counter()
# Begin dropping sand.
into_the_abyss = False
grains = 0
full = False
while not (full or into_the_abyss):
    # Create a new grain of sand
    (i, j) = xy_to_ij([500, 0])
    grains += 1
    if grid[i][j] != '.':
        full = True
        break
    blocked = False
    
    # Dropping logic
    while not blocked or into_the_abyss:
        i += 1
        if i >= height:
            into_the_abyss = True
            break
        if grid[i][j] == '.':
            continue

        # Blocked below. Try left.            
        if j == 0:
            into_the_abyss = True
            break
        if grid[i][j-1] =='.':
            j -= 1
            continue
        
        # Blocked left. Try right.
        if j >= width - 1:
            into_the_abyss = True
            break
        
        if grid[i][j+1] == '.': 
            j += 1
            continue
        
        grid[i-1][j] = 'o'
        blocked = True

grains -= 1  # That last one that fell into the abyss
toc2 = time.perf_counter()
print(f'Time to drop {grains} grains of sand = {toc2 - toc} s')

# Print final grid, chopping off the extra margins
_, jmin = xy_to_ij([xmin_save, 0])
_, jmax = xy_to_ij([xmax_save, 0])
for row in grid:
    print(''.join(row[jmin:jmax+1]))
            
