#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
day01.py

Created on Sun Dec  1 10:54:33 2024

Advent Of Code 2024, Day 1.

Part A: sort 2 lists and compute the distance between them as sum(|a_i - b_i|)
Part B: find a similarity score = sum (item_i * # of times item_i from list a
                                       appears in list b)
The similarity score sums over duplicates. That is, if there are two 3's in
list a the value 3 occurs 5 times in list b, they contribute 2 * 3 * 5'

@author: rpoepa
"""

verbose = 1
sample = False
infile = 'input/day01.' + ('sample' if sample else 'input') + '.txt'

#=======================================
#  Functions and data structures

from collections import defaultdict

def count_items(list_in):
    # Count unique items in the input list.
    # Return the unique items as a set and the counts as a default_dict
    counts = defaultdict(int)
    unique_items = set()
    for x in list_in:
        counts[x] += 1
        unique_items.add(x)
    return unique_items, counts

#=======================================

#======== Begin main program =========
import time

with open(infile, 'r') as fin:
    lines = fin.readlines()

tic = time.perf_counter()

#=========== parsing =======

list_a = []
list_b = []
# Note for future parsing, this from Stack Overflow
# s = 'a.b....c......d.ef...g'
# sp = re.compile('\.+').split(s)
# print(sp)
for line in lines:
    vals = line.split()
    list_a.append(int(vals[0]))
    list_b.append(int(vals[1]))

#======== The work =========

list_a.sort()
list_b.sort()

# Part A
dist = 0
for pair in zip(list_a, list_b):
    dist += abs(pair[0] - pair[1])
tocA = time.perf_counter()
print(f'Part A: Total distance = {dist}')
print(f'Execution time = {(tocA - tic) * 1000} ms ')

# Part B
items_a, counters_a = count_items(list_a)
items_b, counters_b = count_items(list_b)
similarity = 0
for val in items_a:
    similarity += val * counters_a[val] * counters_b[val]
tocB = time.perf_counter()
print(f'Part B: Total similarity = {similarity}')
print(f'Execution time = {(tocB - tocA) * 1000} ms ')
print(f'Total execution time = {(tocB - tic) * 1000} ms ')

