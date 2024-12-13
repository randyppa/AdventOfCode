#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
day12.py

Created on Thu Dec 12 12:06 2024

Advent Of Code 2024, Day 12.

Part A: Divide a map into contiguous regions
Part B: Count the walls around each region

@author: randyppa
"""

verbose = 0
sample = False
infile = 'input/day12.' + ('sample' if sample else 'input') + '.txt'

#=======================================
#  Functions and data structures

class Cell:
    def __init__(self, label):
        self.visited = False
        self.perimeter = 0
        self.region = None
        self.label = label
        self.loc = None

class Region:
    highest_id = 0
    def __init__(self):
        self.cells = set()
        self.id = Region.highest_id
        self.walls = 0
        self.label = '.'
        Region.highest_id += 1
    
    def add_cell(self, cell):
        if cell not in self.cells:
            self.cells.add(cell)
        cell.region = self
    
    def perimeter(self):
        perim = 0
        for cell in self.cells:
            perim += cell.perimeter
        return perim
    
    def area(self):
        return len(self.cells)
    
#=======================================

#======== Begin main program =========
import time
import numpy as np

with open(infile, 'r') as fin:
    lines = fin.readlines()

tic = time.perf_counter()

#=========== parsing =======
regions = {}
grid = np.array([[c for c in line.strip()] for line in lines])
nrows = len(grid)
ncols = len(grid[0])
map = {}
# Create an array of Cells to hold the information
# Include a 1-cell margin around all sides, as region 0
border = Region()
regions[border.id] = border
for row in range(-1, nrows + 1):
    for col in range(-1, ncols + 1):
        if row < 0 or row >= nrows or col < 0 or col >= ncols:
            cell = Cell('.')
            regions[border.id].add_cell(cell)
            cell.region = regions[border.id]
            cell.visited = True
        else:
            cell = Cell(grid[row, col])
        map[row, col] = cell
        cell.loc = (row, col)

# Identify neighbors of each cell
for row in range(nrows):
    for col in range(ncols):
        cell = map[row, col]
        nbrs = [map[row - 1, col], map[row + 1, col], 
                map[row, col - 1], map[row, col + 1]]
        nbrs = [nbr for nbr in nbrs if nbr.label == cell.label]
        cell.nbrs = nbrs
        cell.perimeter = 4 - len(nbrs)
#======== The work =========
# Scan for regions

unvisited = set()
for cell in map.values():
    if cell.visited:
        continue
    
    region = Region()
    regions[region.id] = region
    region.add_cell(cell)
    region.label = cell.label
    # Look for neighbors with the same label that have not yet been
    # visited
    cell.visited = True
    unvisited.update([nbr for nbr in cell.nbrs if not nbr.visited])

    while len(unvisited) > 0:
        next_cell = unvisited.pop()
        next_cell.visited = True
        region.add_cell(next_cell)
        unvisited.update([nbr for nbr in next_cell.nbrs if not nbr.visited])
        next_cell.visited = True

# Score the regions
score = 0
for region in regions.values():
    score += region.area() * region.perimeter()
    
tocA = time.perf_counter()
print(f'Part A: Score = {score}')
print(f'Execution time = {(tocA - tic) * 1000} ms ')

# Part B: Identify the walls between regions

for row in range(nrows):
    # Northern walls. Scan each row to see where there is a wall above it.
    in_wall = False     # Set True when a wall begins
    # Regions to north and south of the wall
    curN = None
    curS = None
    for col in range(ncols):
        nextN = map[row - 1, col].region
        nextS = map[row, col].region
        if nextN != nextS and (not in_wall or \
            (in_wall and nextS != curS)):
            # New wall begins
            in_wall = True
            nextS.walls += 1
        curN = nextN
        curS = nextS
        if curN == curS:
            in_wall = False
            
    # Southern walls. Scan each row to see where there is a wall above it.
    in_wall = False     # Set True when a wall begins
    # Regions to north and south of the wall
    curN = None
    curS = None
    for col in range(ncols):
        nextN = map[row, col].region
        nextS = map[row + 1, col].region
        if nextN != nextS and (not in_wall or \
            (in_wall and nextN != curN)):
            # New wall begins
            in_wall = True
            nextN.walls += 1
        curN = nextN
        curS = nextS
        if curN == curS:
            in_wall = False

# Now scan for western and eastern walls
for col in range(ncols):
    in_wall = False     # Set True when a wall begins
    curW = None
    curE = None
    for row in range(nrows):
        nextW = map[row, col - 1].region
        nextE = map[row, col].region
        if nextW != nextE and (not in_wall or \
            (in_wall and nextE != curE)):
            # New wall begins
            in_wall = True
            nextE.walls += 1
        curW = nextW
        curE = nextE
        if curW == curE:
            in_wall = False
            
    in_wall = False     # Set True when a wall begins
    curW = None
    curE = None
    for row in range(nrows):
        nextW = map[row, col].region
        nextE = map[row, col + 1].region
        if nextW != nextE and (not in_wall or \
            (in_wall and nextW != curW)):
            # New wall begins
            in_wall = True
            nextW.walls += 1
        curW = nextW
        curE = nextE
        if curW == curE:
            in_wall = False

score = 0
for region in regions.values():
    if verbose > 0:
        print(f'Region {region.label}: walls = {region.walls}, area = {region.area()}')
    score += region.walls * region.area()
 
tocB = time.perf_counter()
print(f'Part B: score = {score}')
print(f'Execution time = {(tocB - tocA) * 1000} ms ')
print(f'Total execution time = {(tocB - tic) * 1000} ms ')


