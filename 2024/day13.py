#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
day13.py

Created on Fri Dec 13 00:21 2024

Advent Of Code 2024, Day 13.

Part A: Solve an integer programming problem to win prizes
Part B:

@author: randyppa
"""

verbose = 0
sample = False
infile = 'input/day13.' + ('sample' if sample else 'input') + '.txt'

#=======================================
#  Functions and data structures

import numpy as np
class Machine:
    def __init__(self):
        self.ax = 0
        self.ay = 0
        self.bx = 0
        self.by = 0
        self.prizex = 0
        self.prizey = 0
#        self.solutions = []
        self.best_soln = None
    
    def solve(self):
        # Algebraic approach. Solve the 2 x 2 linear system
        # Just for grins, do it with Cramer's Rule instead of invoking too
        # much of numpy's linalg library
        A = np.array( [[self.ax, self.bx], [self.ay, self.by]])
        A1 = np.array( [[self.prizex, self.bx], [self.prizey, self.by]])
        A2 = np.array( [[self.ax, self.prizex], [self.ay, self.prizey]])
        detA = np.linalg.det(A)
        na = np.linalg.det(A1) / detA
        nb = np.linalg.det(A2) / detA
        if detA == 0:
            print('Matrix is singular!')
            # This never came up in the data
        # Check whether solution is an integer by rounding to int and
        # substituting. (Numerical solution has slight errors)
        na = round(na)
        nb = round(nb)
        cost = 3 * na + nb
        if na * self.ax + nb * self.bx == self.prizex and \
            na * self.ay + nb * self.by == self.prizey:
                self.best_soln = (na, nb, cost)
        else:
            self.best_soln = None
            
#=======================================

#======== Begin main program =========
import time
import re

with open(infile, 'r') as fin:
    lines = fin.readlines()

tic = {}
tic['A'] = time.perf_counter()

#=========== parsing =======
machines = []
lineno = 0
while lineno < len(lines):
    machine = Machine()
    machines.append(machine)
    nums = re.findall('\d+', lines[lineno])
    machine.ax = int(nums[0])
    machine.ay = int(nums[1])
    nums = re.findall('\d+', lines[lineno + 1])
    machine.bx = int(nums[0])
    machine.by = int(nums[1])
    nums = re.findall('\d+', lines[lineno + 2])
    machine.prizex = int(nums[0])
    machine.prizey = int(nums[1])
    lineno += 4
#======== The work =========

toc = {}
for part in ['A', 'B']:
    tot_na = 0
    tot_nb = 0
    tot_cost = 0
    nprizes = 0
    for m, machine in enumerate(machines):
        if part == 'B':
            machine.prizex += 10000000000000
            machine.prizey += 10000000000000
        machine.solve()
        if machine.best_soln is None:
            if verbose > 0:
                print(f'Machine {m}: No solutions')
        else:
            na = machine.best_soln[0]
            nb = machine.best_soln[1]
            cost = machine.best_soln[2]
            nprizes += 1
            tot_na += na
            tot_nb += nb
            tot_cost += cost
            if verbose > 0:
                print(f'Machine {m}: {na} A + {nb} B, cost = {cost}')
    
    toc[part] = time.perf_counter()
    tic['B'] = toc['A']
    print(f'Part {part}: # prizes = {nprizes}, cost = {tot_cost}')
    print(f'Execution time = {(toc[part] - tic[part]) * 1000} ms ')

print(f'Total execution time = {(toc["B"] - tic["A"]) * 1000} ms ')


