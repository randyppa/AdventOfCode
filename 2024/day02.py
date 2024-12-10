#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
day02.py -- template

Created on Mon Dec  2 00:49 2024

Advent Of Code 2024, Day 2.

Part A: Analyze reports (sequences of numbers) and determine if they are
    "safe" or "unsafe" based on certain rules.
Part B: Allow deletion of one entry to correct unsafe sequences

@author: rpoepa
"""

verbose = 0
sample = False
infile = 'input/day02.' + ('sample' if sample else 'input') + '.txt'

#=======================================
#  Functions and data structures

# Check a sequence against the "safe" rules
def is_safe(seq):
    # Rules:
    #   1. Must be either all decreasing or all increasing
    #   2. Jump between entries must be 1, 2, or 3
    delta = [seq[k] - seq[k-1] for k in range(1, len(seq))]
    signs = [d >= 0 for d in delta]
    # Check for a change of sign
    if any(signs) and not all(signs):
        return False
    # If decreasing, flip the signs of the deltas
    if not signs[0]:
        delta = [-d for d in delta]
    # Check magnitude of deltas
    for d in delta:
        if d < 1 or d > 3:
            return False
    return True
        
# Attempt correction of unsafe sequence
def is_safe_if_dampened(seq):
    n = len(seq)
    for k in range(n):
        seq1 = seq.copy()
        seq1.pop(k)
        if is_safe(seq1):
            return True
        
    return False
#=======================================

#======== Begin main program =========
import time

with open(infile, 'r') as fin:
    lines = fin.readlines()

tic = time.perf_counter()

#=========== parsing =======
reports = []
for line in lines:
    vals = [int(x) for x in line.split()]
    reports.append(vals)


#======== The work =========
safe_count = 0
for report in reports:
    safe = is_safe(report)
    if verbose > 0:
        print(*report, ': ', 'SAFE' if safe else 'NOT SAFE')
    if safe:
        safe_count += 1

tocA = time.perf_counter()
print(f'Part A: Safe count = {safe_count}')
print(f'Execution time = {(tocA - tic) * 1000} ms ')

#  Part B
safe_count = 0
for report in reports:
    safe = is_safe(report)
    if not safe:
        safe = is_safe_if_dampened(report)
    if verbose > 0:
        print(*report, ': ', 'SAFE' if safe else 'NOT SAFE')
    if safe:
        safe_count += 1

tocB = time.perf_counter()
print(f'Part B: Safe count = {safe_count}')
print(f'Execution time = {(tocB - tocA) * 1000} ms ')
print(f'Total execution time = {(tocB - tic) * 1000} ms ')

