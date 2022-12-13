#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advent of Code 2022, Day 12.

Part 1.
Find the shortest path from a given start to end point over an elevation
grid. Elevations go from 'a' to 'z' (start is at 'a', end is at 'z') and
allowed steps are L, R, U, D and must be a change of elevation of 0 or 1.

Approach: Djikstra's algorithm'

Part 2. Use every 'a' as a start point and find the shortest of the shortest
paths.

Created on Mon Dec 12 09:09:01 2022

@author: randyppa
"""
import time
#import numpy as np

TheGrid = {}
Infinity = 1e9 # A suitably large value to use as "infinity"
class Gridpoint:
    def __init__(self, height):
        self.neighbors = []
        self.visited = False
        self.distance = Infinity
        self.height = height
        self.prev = None  # predecessor and successor on shortest path
        self.next = None
        
# Djikstra's algorithm
def shortest_path(startloc, endloc):
    # Note: "current" is a set of coordinates, like (3,4). "curpoint" is the object
    # describing that location.
    unvisited_set = set() # The "unvisited set" keeps track of those with FINITE
                          # distance from start
                          
    current = startloc
    TheGrid[current].distance = 0
    abort = False
    while not abort and current != endloc:
        curpoint = TheGrid[current]
        for nbr in curpoint.neighbors:
            if not TheGrid[nbr].visited:
                tentative_distance = curpoint.distance + 1
                if tentative_distance < TheGrid[nbr].distance:
                    TheGrid[nbr].distance = tentative_distance
                    TheGrid[nbr].prev = current
                    if not nbr in unvisited_set:
                        unvisited_set.add(nbr)
        curpoint.visited = True
        if current in unvisited_set:
            unvisited_set.remove(current)
        
        if len(unvisited_set) > 0:
            # Next point to consider is the unvisited point with smallest distance
            current = min(unvisited_set, key = lambda xy: TheGrid[xy].distance)
        else:
            #print('ERROR! No path')
            abort = True
            return Infinity
    return TheGrid[endloc].distance

def show_shortest_path(endloc):
    # For output, trace the path back and connect it up in the forward direction
    current = endloc
    while current in TheGrid.keys() and not TheGrid[current].prev is None:
        curpoint = TheGrid[current]
        TheGrid[curpoint.prev].next = current
        current = curpoint.prev
    
    current = startloc
    path = ''
    while not current is None:
        path += ' ' + str(current)
        current = TheGrid[current].next
    
    return path

def reset_grid():
    for point in TheGrid.values():
        point.prev = None
        point.next = None
        point.distance = Infinity
        point.visited = False
        
#======================================
#  Begin script
#======================================
tic = time.perf_counter()
grid = []
#with open('input/test.2022day12.txt', 'r') as f:
with open('input/input.2022day12.txt') as f:
    for line in f:
        grid.append([ord(c) - ord('a') for c in line.strip()])

# Find start and end points
startval = ord('S') - ord('a')
endval = ord('E') - ord('a')
startloc = (0, 0)
endloc = (0, 0)
nrows = len(grid)
ncols = len(grid[0])
#unvisited_set = set()

for i, row in enumerate(grid):
    if startval in row:
        j = row.index(startval)
        startloc = (i, j)
        row[j] = 0
    if endval in row:
        j = row.index(endval)
        endloc = (i, j)
        row[j] = 25
    # Convert to a dictionary of Gridpoint objects
    for j in range(ncols):
        TheGrid[(i,j)] = Gridpoint(row[j])
        #unvisited_set.add((i,j))

# Identify neighbors (can be reached by a legal step)
for i in range(nrows):
    for j in range(ncols):
        point = TheGrid[(i,j)]
        if i > 0 and TheGrid[(i-1,j)].height - point.height <= 1:
            point.neighbors.append( (i-1, j) )
        if i < nrows - 1 and TheGrid[(i+1,j)].height - point.height <= 1:
            point.neighbors.append( (i+1, j) )
        if j > 0 and TheGrid[(i, j-1)].height - point.height <= 1:
            point.neighbors.append( (i, j-1) )
        if j < ncols - 1 and TheGrid[(i, j+1)].height - point.height <= 1:
            point.neighbors.append( (i, j+1) )
            
toc = time.perf_counter()
print(f'Time to load and setup = {(toc - tic) * 1000} ms')

dist = shortest_path(startloc, endloc)
path = show_shortest_path(endloc)

toc2 = time.perf_counter()

print(f'Shortest path from {startloc} to {endloc} is {path}')
print(f'Path length = {TheGrid[endloc].distance}')
print(f'Time for Part 1 = {toc2 - toc} s')

toc2 = time.perf_counter()
# Part 2: Use every cell with height 0 ('a' in the original input) as a
# startpoint. See which one has the shortest path to endloc.
count = 0
shortest_dist = Infinity
for ij in TheGrid.keys():
    if TheGrid[ij].height == 0:
        reset_grid()
        count += 1
        dist = shortest_path(ij, endloc)
        #print(f'Distance from {ij} = ' + 
        #      'NO PATH' if dist == Infinity else f'{dist}')
        if dist < shortest_dist:
            shortest_dist = dist
toc3 = time.perf_counter()
print(f'{count} start points tested')
print(f'Shortest of shortest paths = {shortest_dist}')
print(f'Time for Part 2 = {toc3 - toc2}')
         