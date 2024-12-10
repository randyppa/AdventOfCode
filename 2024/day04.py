#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
day04.py -- template

Created on Tue Dec 3 00:00:00 2024

Advent Of Code 2024, Day 4.

Part A: Word search. Find the word XMAS in any of 8 directions
Part B: Pattern search: Find MAS in the shape of an X.

@author: rpoepa
"""

verbose = 0
sample = False
infile = 'input/day04.' + ('sample' if sample else 'input') + '.txt'

#=======================================
#  Functions and data structures

# Perform a word search in all 8 directions
def word_search(word, grid, i, j):
    word_arr = np.array([c for c in word])
    lenword = len(word)
    directions = [(-1, 0), (-1, 1), (0, 1), (1, 1),
                  (1, 0), (1, -1), (0, -1), (-1, -1)]
    count = 0
    for direct in directions:
        # Two different approaches. Timing results:
        # Using a takes about 347 ms, using b takes 391 ms.
        a = word_search_dir(word, grid, (i, j), direct)
        #b = np.all(gettext(grid, i, j, direct[0], direct[1], lenword) == word_arr)
        count += a
    return count

# Perform a word search in one direction
def word_search_dir(word, grid, startloc, delta):
    startloc = np.array(startloc)
    delta = np.array(delta)
    lenword = len(word)
    gridshape = grid.shape
    finalpos = startloc + (lenword - 1) * delta
    if any(finalpos < 0) or any(finalpos >= gridshape):
        return False
    
    loc = startloc
    for k in range(lenword):
        if grid[loc[0], loc[1]] != word[k]:
            return False
        loc += delta
    return True

def gettext(grid, i, j, delta_i, delta_j, nchars):
    dim = grid.shape
    text = np.zeros((nchars,), 'str')
    k = 0
    while k < nchars and i >= 0 and j >= 0 and i < dim[0] and j < dim[1]:
        text[k] = grid[i, j]
        i += delta_i
        j += delta_j
        k += 1
    return text

# Part B: Search for two MAS strings in the shape of an X.
#  Meaning one goes NE-SW (in either direction) and one goes NW-SE
def x_mas_search(grid, i, j):
    dim = grid.shape
    # Middle char must be an A
    if grid[i, j] != 'A':
        return False
    # Can't be on any edge
    if i == 0 or i == dim[0] - 1:
        return False
    if j == 0 or j == dim[1] - 1:
        return False
    
    # Explicitly check all four directions
    found_NW_SE = (grid[i-1, j-1] == 'M' and grid[i+1,j+1] == 'S') or \
        (grid[i-1,j-1] == 'S' and grid[i+1,j+1] == 'M')
    found_NE_SW = (grid[i-1, j+1] == 'M' and grid[i+1, j-1] == 'S') or \
        (grid[i-1, j+1] == 'S' and grid[i+1, j-1] == 'M')
    
    return found_NW_SE and found_NE_SW
    
#=======================================

#======== Begin main program =========
import time
import numpy as np

with open(infile, 'r') as fin:
    lines = fin.readlines()

tic = time.perf_counter()

#=========== parsing =======
# Convert the text into an n x m numpy array of chars
grid = []
for line in lines:
    line = line.strip()
    grid.append([c for c in line])

grid = np.array(grid)
dim = grid.shape
nrows = dim[0]
ncols = dim[1]

#======== The work =========
# Part A
total = 0
for row in range(nrows):
    for col in range(ncols):
        if grid[row,col] == 'X':
            num_found = word_search('XMAS', grid, row, col)
            total += num_found

tocA = time.perf_counter()
print(f'Part A: Count = {total}')
print(f'Execution time = {(tocA - tic) * 1000} ms ')

# Part B
count = 0
x_mas_search(grid, 1, 2)
for row in range(nrows):
    for col in range(ncols):
        found = x_mas_search(grid, row, col)
        count += found
        if verbose>0 and found:
            print(f'X-MAS found at ({row},{col})')

tocB = time.perf_counter()
print(f'Part B: Count = {count}')
print(f'Execution time = {(tocB - tocA) * 1000} ms ')
print(f'Total execution time = {(tocB - tic) * 1000} ms ')
