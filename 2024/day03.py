#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
day03.py

Created on Tue Dec  3 07:53 2024

Advent Of Code 2024, Day 3.

Part A: Parsing problem. Extracting all strings of the form "mul(num,num)"
Part B: Also search for "don't()" and "do()" instructions, which turn
   processing of the mul instructions off and on, respectively

    Pretty trivial with regexes. Go that way first for the points.
@author: rpoepa
"""

verbose = 1
sample = False
infile = 'input/day03.' + ('sample' if sample else 'input') + '.txt'

#=======================================
#  Functions and data structures
    
#=======================================

#======== Begin main program =========
import time
import re

if sample:
    lines = r"xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64]" + \
        r"(mul(11,8)undo()?mul(8,5))"
else:
    with open(infile, 'r') as fin:
        lines = fin.read()


#=========== parsing =======

# Extract all numeric arguments
def parse_it(text, part='A'):
    # Part A: Only mul(n,n) is accepted
    valid_str = 'mul\(\d+,\d+\)'
    # Part B: Also accept "do" or "don't" calls
    if part == 'B':
        valid_str += "|do\(\)|don\'t\(\)"
        
    # Extract all properly formed instructions
    instr = re.findall(valid_str, text)
    
    # Get the product factors, processing dos and don'ts using "enabled"
    # flag to turn on/off parsing
    factors = []
    enabled = True
    for token in instr:
        if token == 'do()':
            enabled = True
        elif token == "don\'t()":
            enabled = False
        elif enabled:
            factors.append([int(x) for x in re.findall('\d+', token)])
    return factors

#args = [[int(x) for x in re.findall('\d+', func_call)] for func_call in instr]
#======== The work =========

for part in ['A', 'B']:
    tic = time.perf_counter()
    args = parse_it(lines, part = part)
    total = 0
    for pair in args:
        total += pair[0] * pair[1]
    
    toc = time.perf_counter()
    
    print(f'Part {part}: Total = {total}')
    print(f'Execution time = {(toc - tic) * 1000} ms ')
