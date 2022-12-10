#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Advent of Code 2022, Day 1, Part 1 and Part 2.

Simple text file parsing.

Created on Sat Dec  3 10:28:06 2022

@author: randyppa
"""

import time

# INPUT PROCESSING
tic = time.perf_counter()
with open('input/input.2022day1.txt', 'r') as f:
    elf = []        # One elf is a list of food values
    elves = []      # List of elves.
    for line in f:
        valstr = line.strip()
        if len(valstr) == 0:    # Blank line. End of this elf's data
            elves.append(elf)
            elf = []
        else:
            elf.append(int(valstr))
    
    if len(elf) > 0:    # If file didn't end with a blank, add the last elf
        elves.append(elf)
        elf = []

elf_totals = [sum(elf) for elf in elves]


# PART 1: Find highest total.
# Part 2: Find total of top 3 totals

elf_totals.sort(reverse=True)
toc = time.perf_counter()
print(f'{len(elves)} elves found')
print(f'Top three totals = {elf_totals[0]}, {elf_totals[1]}, {elf_totals[2]}')
print(f'Highest total is {elf_totals[0]}')
print(f'Sum of top three is {sum(elf_totals[0:3])}')
print(f'Total execution time = {(toc - tic) * 1000} ms')