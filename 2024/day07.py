#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
day07.py

Created on Sat Dec 7  06:24 2024
7
Advent Of Code 2024, Day 7.

Part A: Insert * and + operators into an equation to make it true.
Part B: Also include a concatenation || operator.

Efficiency ideas:
    1. All the operations, since the arguments are positive integers,
    increase the result. So as soon as you've exceeded the desired result,
    you know you've failed. Implement this as "lazy evaluation"
    2. A sort of "branch and bound". Once you have a lazy failure, you know
    any sequence of operations starting the same way will also fail.
    
    Result: #1 saved maybe 8%. #2 caused it to take MORE time!!!, about 20%

@author: rpoepa
"""

import itertools as it

verbose = 1
sample = False
infile = 'input/day07.' + ('sample' if sample else 'input') + '.txt'

#=======================================
#  Functions and data structures

class Equation:
    
    def __init__(self, arguments, result):
        self.arguments = arguments  # The n numbers to be operated on
        self.rhs = result           # The desired result
        self.operators = []         # The (n - 1) operators '+' and '*'
        self.truth = False          # Truth value
        self.invalid_sets = {}      # Sets of invalid operator sequences,
                                    # keyed by length
    
    # Add an operator seqeunce to the appropriate-length invalid set
    def mark_invalid(self, ops):
        n = len(ops)
        if n not in self.invalid_sets.keys():
            self.invalid_sets[n] = set()
        self.invalid_sets[n].add(''.join(ops))
    
    # Check the operator sequence against the invalid sets
    def check_invalid(self):
        for item in self.invalid_sets.items():
            n = item[0]
            if ''.join(self.operators[:n]) in item[1]:
                return True
        return False
    
    def clear_invalid(self):
        self.invalid_sets = {}
    
    # Evaluate the expression. "Lazy" evaluation only evaluates enough
    # to determine whether it's true or false. Since all operations only
    # increase the value, we can stop as soon as we've exceeded the rhs.
    def eval(self, lazy = False):
        # Utility function to implement concatenation
        def concat(a, b):
            return int(str(a) + str(b))

        if len(self.operators) != len(self.arguments) - 1:
            self.truth = False
            return
        
        if lazy:
            if self.check_invalid():
                self.truth = False
                return
        
        result = self.arguments[0]
        for index, nextop in enumerate(
                zip(self.operators, self.arguments[1:])):
            if nextop[0] == '+':
                result += nextop[1]
            elif nextop[0] == '*':
                result *= nextop[1]
            elif nextop[0] == '||':
                result = concat(result, nextop[1])
            else:   # invalid
                self.truth = False
                return
            if result > self.rhs and lazy:
                self.truth = False
                self.mark_invalid(self.operators[:index+1])
                return
            
        self.truth = result == self.rhs

    
#=======================================

#======== Begin main program =========
import time

with open(infile, 'r') as fin:
    lines = fin.readlines()

tic = time.perf_counter()

#=========== parsing =======
eqns = []
for line in lines:
    vals = line.strip().split()
    result = int(vals[0][:-1])
    nums = [int(x) for x in vals[1:]]
    eqns.append( Equation(nums, result) )

#======== The work =========
toc = []
for part in ['A', 'B']:
    calibration = 0
    for eqn in eqns:
        eqn.clear_invalid()
        nargs = len(eqn.arguments)
        if part == 'A':
            operators = ['*', '+']
        else:
            operators = ['*', '+', '||']
        for ops in it.product(operators, repeat = nargs - 1):
            eqn.operators = ops
            eqn.eval(lazy=True)
            if eqn.truth:
                calibration += eqn.rhs
                break
    toc.append(time.perf_counter())
    print(f'Part {part}: Total calibration value = {calibration}')

print(f'Execution time part A = {toc[0] - tic} s ')
print(f'Execution time part B = {toc[1] - toc[0]} s ')
print(f'Total execution time = {toc[1] - tic} s ')

