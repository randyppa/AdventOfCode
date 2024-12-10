#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
day06.py

Created on Fri Dec  6 02:03 2024

Advent Of Code 2024, Day 6.

Part A: Trace a path through a grid with obstacles

You just know that part B is going to be a grid too big to keep in memory.
So work with a virtual grid for part A.

Part B: Deliberately create a loop by putting a new block in the grid

@author: rpoepa
"""

verbose = 0
sample = False
infile = 'input/day06.' + ('sample' if sample else 'input') + '.txt'

#=======================================
#  Functions and data structures
class Vrow:
    # A virtual row, represented as a sequence of runs.
    def __init__(self, width):
        self.width = width

class Vgrid:
    # Direction of a 90 degree right turn
    nextdir = {'N':'E', 'E':'S', 'S':'W', 'W':'N'}
    # A virtual grid
    def __init__(self, nrows, ncols):
        self.nrows = nrows
        self.ncols = ncols
        self.blocks_by_row = {} # Position of blocks in each row
        self.blocks_by_col = {} # Position of blocks in each column
        self.visited = set()    # Points that have been visited
        self.path = []
        self.loop = False
    
    def add_block(self, row, col):
        if row in self.blocks_by_row.keys():
            self.blocks_by_row[row].append(col)
            self.blocks_by_row[row].sort()
        else:
            self.blocks_by_row[row] = [col]
            
        if col in self.blocks_by_col.keys():
            self.blocks_by_col[col].append(row)
            self.blocks_by_col[col].sort()

        else:
            self.blocks_by_col[col] = [row]
    
    def remove_block(self, row, col):
        if row in self.blocks_by_row.keys():
            self.blocks_by_row[row].remove(col)
            self.blocks_by_row[row].sort()
        if col in self.blocks_by_col.keys():
            self.blocks_by_col[col].remove(row)
            self.blocks_by_col[col].sort()
    
    # Go in a given direction until block or off the grid
    def _stop_pos(self, startpos, direction):
        row = startpos[0]
        col = startpos[1]
        off_grid = False
        # N and S: Search current column for blocks
        if direction in 'NS':
            if col in self.blocks_by_col.keys():
                blocks = self.blocks_by_col[col]
                if direction == 'N':
                    blocks_ahead = [b + 1 for b in blocks if b < row]
                else: # 'S'
                    blocks_ahead = [b - 1 for b in blocks[::-1] if b > row]
            else:
                blocks_ahead = []
            
            if len(blocks_ahead) == 0:
                # No blocks, run off edge of grid
                stoprow = 0 if direction == 'N' else self.nrows - 1
                stoppos = (stoprow, col)
                off_grid = True
            else:
                stoppos = (blocks_ahead[-1], col)
        # E and W: Search current row for blocks
        else:
            if row in self.blocks_by_row.keys():
                blocks = self.blocks_by_row[row]
                if direction == 'W':
                    blocks_ahead = [b + 1 for b in blocks if b < col]
                else: # 'E'
                    blocks_ahead = [b - 1 for b in blocks[::-1] if b > col]
            else:
                blocks_ahead = []
            
            if len(blocks_ahead) == 0:
                # No blocks, run off edge of grid
                stopcol = 0 if direction == 'W' else self.ncols - 1
                stoppos = (row, stopcol)
                off_grid = True
            else:
                stoppos = (row, blocks_ahead[-1])
        return stoppos, off_grid, Vgrid.nextdir[direction]
                    
            
    def find_path(self, startpos, direction):
        # Keep track of each segment. 1st egment is one point at start.
        off_grid = False
        path = [(startpos, off_grid, 'N')]
        curpos = startpos
        self.loop = False
        while not off_grid:
            # Return is a tuple: final position, True if ran off the grid, and
            # direction of next walk
            pathnode = self._stop_pos(curpos, direction)
            # Infinite loop detector
            if pathnode in path:
                self.loop = True
                pathnode = (pathnode[0], True, pathnode[2])
                break
            
            path.append(pathnode)
            curpos, off_grid, direction = pathnode
        self.path = path.copy()
        return
        
    def mark_path(self):
        delta = {'N':(-1,0), 'E':(0,1), 'S':(1,0), 'W':(0,-1)}
        self.visited = set()
        if len(self.path) == 0:
            return
        prevnode = self.path[0]
        for node in self.path[1:]:
            curpos = prevnode[0]
            curdir = prevnode[2]
            endpos = node[0]
            step = delta[curdir]
            while curpos != endpos:
                self.visited.add(curpos)
                curpos = (curpos[0]+step[0], curpos[1]+step[1])
            self.visited.add(endpos)
            prevnode = node
            
#=======================================

#======== Begin main program =========
import time

with open(infile, 'r') as fin:
    lines = fin.readlines()

tic = time.perf_counter()

#=========== parsing =======
nrows = len(lines)
ncols = len(lines[0].strip())
grid = Vgrid(nrows, ncols)

for row,line in enumerate(lines):
    line = line.strip()
    for col,elem in enumerate(line):
        if elem == '#':
            grid.add_block(row, col)
        elif elem == '^':
            startpos = (row, col)


for irow in range(nrows):
    row = Vrow(ncols)


#======== The work =========

# Follows the walking rules until path goes off the edge or infinite loop
# detected. Modifies grid.path
grid.find_path(startpos, 'N')

# Create the set of visited pixels from the path
grid.mark_path()


tocA = time.perf_counter()
print(f'Part A: Path had {len(grid.path)} segments')
print(f'Total points visited = {len(grid.visited)}')
print(f'Execution time = {(tocA - tic) * 1000} ms ')

# Part B: Find all positions such that putting a new block there will
# create a loop.
#
# Assert: Such a position has to be one of the visited nodes. Otherwise
# the path will never intersect it.

grid.add_block(7,6)
grid.find_path(startpos, 'N')
grid.remove_block(7,6)

grid.add_block(7,7)
grid.find_path(startpos, 'N')
grid.remove_block(7,7)

candidates = grid.visited
# Don't block the starting position, there's somebody standing there!
candidates.remove(startpos)

solution = []
for candidate in candidates:
    grid.add_block(candidate[0], candidate[1])
    grid.find_path(startpos, 'N')
    if grid.loop:
        solution.append(candidate)
    grid.remove_block(candidate[0], candidate[1])


tocB = time.perf_counter()
print(f'Part B: Found {len(solution)} locations that create loops')
if verbose > 0:
    for soln in solution:
        print(soln)
print(f'Execution time = {(tocB - tocA) * 1000} ms ')
print(f'Total execution time = {(tocB - tic) * 1000} ms ')

