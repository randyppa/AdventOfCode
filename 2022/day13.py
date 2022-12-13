#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Advent of Code 2022, day 13.

Hierarchical lists of lists and numbers. Parse and compare them.

Approach: Build them as ordinary Python lists. Use built-in eval() to parse.

Rework: Build a parser. Add the "lazy" flag to revert to eval() for checking.
"eval" is considered dangerous and really should be avoided.

Created on Tue Dec 13 09:28:51 2022


@author: randyppa
"""
import time
from numpy import sign
from functools import cmp_to_key

def parse(input_str):
    if len(input_str) == 0:
        return None, input_str
    if input_str[0] == ',':
        value, rem_str = parse(input_str[1:])
        return (value, rem_str)
    elif input_str[0].isnumeric():
        k = 0
        while k < len(input_str) and input_str[k].isnumeric():
            k += 1
        value = int(input_str[:k])
        return(value, input_str[k:])
    elif input_str[0] == '[':
        output_list = []
        rem_str = input_str[1:]
        while rem_str[0] != ']':
            value, rem_str = parse(rem_str)
            output_list.append(value)
        return (output_list, rem_str[1:])

def myeval(line, lazy):
    if lazy:
        return eval(line)
    else:
        value, output_str = parse(line)
        return value

# Hierarchical list-or-number compare
def compare(a, b):
    islist_a = isinstance(a, list)
    islist_b = isinstance(b, list)
    # Case 1: Both ints
    if not (islist_a or islist_b):
        return sign(a - b)
    # Otherwise, do a list compare, converting any ints to singleton lists

    if not islist_a:
        a = [a]
    if not islist_b:
        b = [b]
    
    # Element by element compare
    na = len(a)
    nb = len(b)
    for i in range(max(na, nb)):
        # Detect if one is shorter. If na == nb, i should never reach either
        # value and these tests won't trigger.
        if i >= na:  # a is shorter
            return -1
        
        if i >= nb:
            return 1
        
        # Recursive compare of the i-th elements.
        cmp = compare(a[i], b[i])
        # If an unequal element found, a < b or b > a.
        if cmp != 0:
            return cmp
    
    # If we're here, then a and b are equal-length lists and every element is
    # equal. So they are equal.
    return 0

#===============================
# Begin script
#===============================
lazy = False

tic = time.perf_counter()
packets = []
with open('input/input.2022day13.txt', 'r') as f:
    for lineno, line in enumerate(f):
        if lineno % 3 == 0:
            pack1 = myeval(line.strip(), lazy)
        elif lineno % 3 == 1:
            pack2 = myeval(line.strip(), lazy)
            packets.append([pack1, pack2])
toc = time.perf_counter()

total = 0
numequal = 0
for index, pair in enumerate(packets):
    cmp = compare(pair[0], pair[1])
    if cmp <= 0:
        total += index + 1
        if cmp == 0:
            numequal += 1
            numequal += 1
toc2 = time.perf_counter()

#======  PART 2 ======
# Sort using the above comparison order.

# First convert the pairs to one long list.
all_packets = []
div1 = [[2]]
div2 = [[6]]
packets.append([div1, div2])  # Include the "divider packets"
    
for pair in packets:
    all_packets.append(pair[0])
    all_packets.append(pair[1])

all_packets.sort(key = cmp_to_key(compare))
loc_div1 = all_packets.index(div1) + 1
loc_div2 = all_packets.index(div2) + 1
toc3 = time.perf_counter()

print(f'Time to parse input = {(toc - tic) * 1000} ms')
print(f'Total of Part 1 indices = {total}')
print(f'Number of equal packets = {numequal}')
print(f'Time for Part 1 = {(toc2 - toc) * 1000} ms')
print(f'Decoder key = {loc_div1 * loc_div2}')
print(f'Time for Part 2 = {(toc3 - toc2) * 1000} ms')
        