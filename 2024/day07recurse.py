#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
day07recurse.py

Created on Sat Dec 7  16:54 2024
7
Advent Of Code 2024, Day 7.

Part A: Insert * and + operators into an equation to make it true.
Part B: Also include a concatenation || operator.

Complete reworking of the machinery, inspired by online discussion using
the word "recursion".

Now I see a recursive approach, working from right to left. You can easily
check whether the last number coukd have been added, multiplied or concatenated.

@author: rpoepa
"""

import itertools as it

verbose = 0
sample = False
infile = 'input/day07.' + ('sample' if sample else 'input') + '.txt'

#=======================================
#  Functions and data structures

class Equation:
    
    def __init__(self, arguments, result):
        self.arguments = arguments  # The n numbers to be operated on
        self.rhs = result           # The desired result
        self.operators = []         # The (n - 1) operators '+','*' or '||'
        self.truth = False          # Truth value
       
    def solve(self, allowed_ops):
        # Recursively work out a solution from the end
        if len(self.arguments) == 1:
            return self.arguments[0] == self.rhs
        
        solved = False
        lastnum = self.arguments[-1]
        # Check if the last op could have been concatenation
        if '||' in allowed_ops:
            lastnum = self.arguments[-1]
            laststr = str(lastnum)
            rhsstr = str(self.rhs)
            if len(rhsstr) > len(laststr) and rhsstr.endswith(laststr):
                if verbose > 0:
                    print(f'Candidate for ||: {rhsstr}')
                subrhs = int(rhsstr[:-len(laststr)])
                subeqn = Equation(self.arguments[:-1], subrhs)
                solved = subeqn.solve(allowed_ops)
                if solved:
                    self.operators = subeqn.operators.copy()
                    self.operators.append('||')
                    
        if not solved:
            if '*' in allowed_ops:
                # Check if the rhs is a multiple of the last num
                if 0 == self.rhs % lastnum:
                    subrhs = self.rhs // lastnum
                    subeqn = Equation(self.arguments[:-1], subrhs)
                    solved = subeqn.solve(allowed_ops)
                    if solved:
                        self.operators = subeqn.operators.copy()
                        self.operators.append('*')
        
        if not solved:
            if '+' in allowed_ops:
                if self.rhs - lastnum >= 0:
                    subrhs = self.rhs - lastnum
                    subeqn = Equation(self.arguments[:-1], subrhs)
                    solved = subeqn.solve(allowed_ops)
                    if solved:
                        self.operators = subeqn.operators.copy()
                        self.operators.append('+')
        return solved
                
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
        nargs = len(eqn.arguments)
        if part == 'A':
            operators = ['*', '+']
        else:
            operators = ['*', '+', '||']
        if eqn.solve(operators):
            eqn.eval(lazy=True)  # Check that it's a solution'
            if eqn.truth:
                calibration += eqn.rhs
    toc.append(time.perf_counter())
    print(f'Part {part}: Total calibration value = {calibration}')

print(f'Execution time part A = {toc[0] - tic} s ')
print(f'Execution time part B = {toc[1] - toc[0]} s ')
print(f'Total execution time = {toc[1] - tic} s ')

