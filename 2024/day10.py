#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
day10.py

Created on Tue Dec  10 08:15 2024

Advent Of Code 2024, Day 10.

Part A: Find "trails" = consecutive grid trails that rise from 0 to 9
Part B: Part A scoring is the unique endpoints from each start location. Part B
   uses the same structures, but the score is the number of trails.

@author: rpoepa
"""

verbose = 1
sample = False
infile = 'input/day10.' + ('sample' if sample else 'input') + '.txt'

#=======================================
#  Functions and data structures

import numpy as np

class Grid:
    def __init__(self, vals):
        self.vals = np.array(vals)
        shape = self.vals.shape
        self.nrows = shape[0]
        self.ncols = shape[1]
        self.trails = {}
    
    # Utility function: Look up value at specified coordinates. Allow 
    # out-of-bound coordinates, and return -1
    def val(self, row, col):
        if row < 0 or col < 0 or row >= self.nrows or col >= self.ncols:
            return -1
        else:
            return self.vals[row, col]
    
    # Utility function: Get the neighboring cells that have a given value
    def neighbors_by_val(self, row, col, val):
        nbrs = []
        if self.val(row - 1, col) == val:
            nbrs += [(row - 1, col)]
        if self.val(row + 1, col) == val:
            nbrs += [(row + 1, col)]
        if self.val(row, col - 1) == val:
            nbrs += [(row, col - 1)]
        if self.val(row, col + 1) == val:
            nbrs += [(row, col + 1)]
        return nbrs
        
    
    def trails_from(self, row, col):
        # Retrieve or create all the trails that start at the given location,
        # increase by 1 each step, and end at 9
        # A trail is a list of coordinate pairs.
        # The return value of this method is a list of trails
        
        # Check whether we've already analyzed this 
        examined = (row, col) in self.trails.keys()
        if examined:
            return self.trails[row, col]
        
        # Exit condition
        if self.vals[row, col] == 9:
            self.trails[row, col] = [[(row, col)]]
        # Otherwise, recursively find trails beginning with the next higher
        # value
        else:
            self.trails[row, col] = []
            candidates = self.neighbors_by_val(row, col, self.vals[row, col] + 1)
            for cand in candidates:
                subtrails = self.trails_from(cand[0], cand[1])
                if len(subtrails) > 0:
                    for subtrail in subtrails:
                        self.trails[row, col].append( [(row,col)] + subtrail)
        return self.trails[row, col]
    
    # All the known trails beginning with a 0
    @property
    def trailheads(self):
        rows, cols = np.where(self.vals == 0)
        coords = [(rows[k], cols[k]) for k in range(len(rows))]
        heads = []
        for coord in coords:
            if len(self.trails_from(coord[0], coord[1])) > 0:
                heads.append(coord)
        return heads
    
    # Part A scoring algorithm: Count the unique value-9 cells reachable
    # from this cell.
    def trail_score(self, row, col):
        if (row, col) not in grid.trails.keys():
            return 0
        
        endpoints = set()
        trails = grid.trails[row, col]
        for trail in trails:
            endpoints.add(trail[-1])
        return len(endpoints)
        
#=======================================

#======== Begin main program =========
import time

with open(infile, 'r') as fin:
    lines = fin.readlines()

tic = time.perf_counter()

#=========== parsing =======
val_array = [[int(c) for c in line.strip()] for line in lines]
grid = Grid(val_array)

#======== The work =========

score = 0
heads = grid.trailheads
for head in heads:
    score += grid.trail_score(head[0], head[1])
    
tocA = time.perf_counter()
print(f'Part A: score = {score}')
print(f'Execution time = {(tocA - tic) * 1000} ms ')
rating = 0
heads = grid.trailheads
for head in heads:
    rating += len(grid.trails_from(head[0], head[1]))
tocB = time.perf_counter()
print(f'Part B: rating = {rating}')
print(f'Execution time = {(tocB - tocA) * 1000} ms ')
print(f'Total execution time = {(tocB - tic) * 1000} ms ')
