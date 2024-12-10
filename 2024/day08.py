#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
day08.py

Created on Sun Dec  8 03:31 2024

Advent Of Code 2024, Day 8.

Part A: Antenna placement. Find all locations in a grid that meet certain
criteria.
Part B:

@author: rpoepa
"""

verbose = 1
sample = False
infile = 'input/day08.' + ('sample' if sample else 'input') + '.txt'

#=======================================
#  Functions and data structures

# A virtual grid to store the objects
class Vgrid:
    def __init__(self, nrows, ncols):
        self.nrows = nrows
        self.ncols = ncols
        self.objects = {}   # Objects are lists of coordinates indexed by the
                            # object type (a string like '#')
    
    # Add an object at the specified location
    # Returns False if the position was clipped, True otherwise
    def add_obj(self, obj, row, col, clip=True):
        if clip and (row < 0 or row >= self.nrows or
                     col < 0 or col >= self.ncols):
            return False
        if obj not in self.objects.keys():
            self.objects[obj] = set()
        self.objects[obj].add( (row, col) )
        return True
    
    # Get all the locations of a specific object type
    def get_obj_loc(self, obj):
        if obj in self.objects.keys():
            return self.objects[obj]
        else:
            return None
    
    # Get all the object names
    def get_objects(self):
        return list(self.objects.keys())
#=======================================

#======== Begin main program =========
import time
import itertools as it
import math

with open(infile, 'r') as fin:
    lines = fin.readlines()

tic = time.perf_counter()

#=========== parsing =======
nrows = len(lines)
ncols = len(lines[0].strip())
grid = Vgrid(nrows, ncols)

for row, line in enumerate(lines):
    for col, c in enumerate(line.strip()):
        if c != '.':
            grid.add_obj(c, row, col)
            
#======== The work =========
object_names = grid.get_objects()

for obj in object_names:
    loc = grid.get_obj_loc(obj)
    for pair in it.permutations(loc, r=2):
        # Given a pair at locations loc0 and loc1, there's an antinode location
        # at loc1 + (loc1 - loc0) = 2 * loc1 - loc0
        ant_r = 2 * pair[1][0] - pair[0][0]
        ant_c = 2 * pair[1][1] - pair[0][1]
        grid.add_obj('#', ant_r, ant_c)  # Will be clipped if off the grid

ant_locs = grid.get_obj_loc('#')

tocA = time.perf_counter()
print(f'Part A: Number of antinodes = {len(ant_locs)}')
print(f'Execution time = {(tocA - tic) * 1000} ms ')

# Part B: Antennas

# Get all the object types again, without the # objects
for obj in object_names:
    loc = grid.get_obj_loc(obj)
    for pair in it.permutations(loc, r=2):
        # This time use all positions on the line which are integers.
        # First calculate the delta and reduce the slope ratio
        delta_r = pair[1][0] - pair[0][0]
        delta_c = pair[1][1] - pair[0][1]
        reduce = math.gcd(delta_r, delta_c)
        if reduce > 1:
            delta_r //= reduce
            delta_c //= reduce
        row = pair[0][0]
        col = pair[0][1]
        while grid.add_obj('#', row, col):
            row += delta_r
            col += delta_c

ant_locs = grid.get_obj_loc('#')
tocB = time.perf_counter()
print(f'Part B: Number of antinodes = {len(ant_locs)}')
print(f'Execution time = {(tocB - tocA) * 1000} ms ')
print(f'Total execution time = {(tocB - tic) * 1000} ms ')

