#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
day05.py

Created on Thu Dec  5 00:19 2024

Advent Of Code 2024, Day 5.

Part A: Given a set of ordering rules, examine sequences to see if they comply
Part B: Sort the lists using the ordering rules

NOTE: It appears that the rules do not define transitive ordering. That is,
you can have a < b and b < c, but c < a. There are 49 unique numbers which
give rise to 1176 pairs, but there are 2288 rules, which seems to imply some
pairs occur more than once

@author: rpoepa
"""

verbose = 1
sample = False
infile = 'input/day05.' + ('sample' if sample else 'input') + '.txt'

import time
import itertools as it
from collections import defaultdict
import functools

#=======================================
#  Functions and data structures

# Class to implement the numbers are "pages" with the custom ordering.
class Page():
    rules = defaultdict(lambda: '<')
    # rules is a dictionary whose keys are tuples (a, b). If the value is '>'
    # then a > b, and if the value is '<' then a < b.
    # By using a defaultdict, unspecified pairs will always return '<', meaning
    # the order is correct.
        
    def __init__(self, pagenum):
        self.pagenum = pagenum
    
    @classmethod
    # Add a comparison rule to the class rules
    def add_pair(cls, pair):
        cls.rules[pair[1], pair[0]] = '>'
    
    @property
    def value(self):
        return self.pagenum
        
    # Comparison methods    
    def __str__(self):
        return str(self.pagenum)
    
    def __eq__(self, other):
        return self.pagenum == other.pagenum
    
    def __lt__(self, other):
        return Page.rules[(self.pagenum, other.pagenum)] == '<'
    
    def __gt__(self, other):
        return Page.rules[(self.pagenum, other.pagenum)] == '>'
    
    def __ge__(self, other):
        return self > other or self == other
    
# Check for any pair found in the rule dictionary with a value of '>'.
# That indicates a pair in the wrong order
def check_order(order):
    for pair in it.combinations(order, 2):
        if pair[0] >= pair[1]:
            return False
    return True

# Comparison function to use in the Part B sort
def cmp(a, b):
    if a < b:
        return -1
    elif a > b:
        return 1
    else:
        return 0

#=======================================

#======== Begin main program =========

with open(infile, 'r') as fin:
    lines = fin.readlines()

tic = time.perf_counter()

#=========== parsing =======


print_orders = []
first_part = True
for line in lines:
    line = line.strip()
    if first_part:
        vals = line.split('|')
        if len(vals) == 2:
            nums = [int(x) for x in vals]
            Page.add_pair(nums)
        else:
            first_part = False
            continue
    else:
        nums = [Page(int(x)) for x in line.split(',')]
        print_orders.append(nums)

#======== The work =========
total = 0
wrong_orders = []
for order in print_orders:
    if check_order(order):
        n = len(order)
        middle_value = order[(n - 1)//2].value
        total += middle_value
    else:
        wrong_orders.append(order) # Store for Part B

tocA = time.perf_counter()
print(f'Part A: Total of middle values = {total}')
print(f'{len(wrong_orders)} were in the wrong order')
print(f'Execution time = {(tocA - tic) * 1000} ms ')

# Part B: Sort the orders that were incorrect
total = 0
for order in wrong_orders:
    order.sort(key=functools.cmp_to_key(cmp))
    n = len(order)
    middle_value = order[(n - 1)//2].value
    total += middle_value

tocB = time.perf_counter()
print(f'Part B: Total of middle values = {total}')
print(f'Execution time = {(tocB - tocA) * 1000} ms ')
print(f'Total execution time = {(tocB - tic) * 1000} ms ')
   
    
    