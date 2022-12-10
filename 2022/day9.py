#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advent Of Code, Day 9

Part 1. Move a marker H (head of a rope) around a grid. T follows it according
to certain rules. Determine how many positions the T visits.

Part 2. The rope has 10 knots. Each knot follows the knot in front of it using
the same 2-knot rule as part 1.

Created on Fri Dec  9 00:27:31 2022

@author: randyppa
"""
import numpy as np
import time

# Based on current position of head (xh, yh) and tail (xt, yt) determine
# by the movement rules what the new position of the tail should be.
def move_tail(xh, yh, xt, yt):
    dx = xh - xt
    dy = yh - yt
    if dx > 1:
        xt += 1
        if dy > 0:
            yt += 1
        elif dy < 0:
            yt -= 1
    elif dx < -1:
        xt -= 1
        if dy > 0:
            yt += 1
        elif dy < 0:
            yt -= 1
    elif dy > 1:
        yt += 1
        if dx > 0:
            xt += 1
        elif dx < 0:
            xt -= 1
    elif dy < -1:
        yt -= 1
        if dx > 0:
            xt += 1
        elif dx < 0:
            xt -= 1
    return (xt, yt)
        

tic = time.perf_counter()
with open('input/input.2022day9.txt', 'r') as f:
    moves = [line.strip().split(' ') for line in f]

toc1 = time.perf_counter()

# Do the moves
xh = 0
yh = 0
xt = 0
yt = 0
patht = set()
patht.add((xt, yt))
for k, move in enumerate(moves):
    dist = int(move[1])
    if move[0] == 'U':
        dx = 0
        dy = 1
    elif move[0] == 'D':
        dx = 0
        dy = -1
    elif move[0] == 'R':
        dx = 1
        dy = 0
    elif move[0] == 'L':
        dx = -1
        dy = 0

    for _ in range(dist):
        xh += dx
        yh += dy
        xt, yt = move_tail(xh, yh, xt, yt)
        patht.add((xt, yt))

toc2 = time.perf_counter()
print(f'Number of points on tail path = {len(patht)}')
print(f'Time for load = {(toc1 - tic)*1e6} μs')
print(f'Time for Part 1 = {(toc2 - toc1)*1000} ms')

toc3 = time.perf_counter()

# Part 2: 10 knots (head + 9 followers)
knots = [(0,0)] * 10
patht10 = set()
patht10.add(knots[9])
for k, move in enumerate(moves):
    dist = int(move[1])
    if move[0] == 'U':
        dx = 0
        dy = 1
    elif move[0] == 'D':
        dx = 0
        dy = -1
    elif move[0] == 'R':
        dx = 1
        dy = 0
    elif move[0] == 'L':
        dx = -1
        dy = 0

    xh, yh = knots[0]
    for _ in range(dist):
        xh += dx
        yh += dy
        knots[0] = (xh, yh)
        for k in range(1,10):
            knots[k] = move_tail(knots[k-1][0], knots[k-1][1], 
                                 knots[k][0], knots[k][1])
        patht10.add(knots[9])

toc4 = time.perf_counter()
print(f'Number of points on tail path for 10-knot rope = {len(patht10)}')
print(f'Time for part 2 = {(toc4 - toc3)*1000} ms')



    