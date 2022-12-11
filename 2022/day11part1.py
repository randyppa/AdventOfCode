#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advent of Code, Day 11, Part 1

Read in a description of "monkeys", the items they hold (value is a 
"worry level") and rules for passing the items around and modifying the
worry levels.

Created on Sun Dec 11 07:46:47 2022

@author: randyppa
"""
import time

class Monkey:
    def __init__(self):
        self.index = 0      # Counter: Not used, just for debug
        self.items = []     # The list of items, FIFO
        self.op = ('*',1)   # Worry modification rule
        self.testval = 1    # Divisibility test
        self.iftrue = 0     # Where to throw if divisible
        self.iffalse = 0    # Where to throw if not divisible
        self.inspect_count = 0
    
    def additem(self, item):
        self.items.append(item)

    def inspect(self, item):      # Perform inspection rules
        self.inspect_count += 1
        
        # A rule like new = old * old is encoded as ('*', None)
        arg = item if self.op[1] is None else self.op[1]
        
        # Step 1: Perform the operation
        if self.op[0] == '+':
            item += arg
        else:
            item *= arg
        
        # Step 2: Divide by 3. Return new value
        return item // 3
    
    def throwto(self, item):
        if item % self.testval == 0:
            return self.iftrue
        else:
            return self.iffalse
    
    # Pretty print
    def __str__(self):
        output = f'Monkey {self.index}:\n'
        output += '  Items' 
        for item in self.items:
            output += ' ' + str(item)
        output += '\n'
        output += f'  Operation: new = old {self.op[0]} '
        output += 'old' if self.op[1] is None else str(self.op[1])
        output += '\n'
        output += f'  If div by {self.testval} throw to {self.iftrue}'
        output += f' else throw to {self.iffalse}\n'
        return output

tic = time.perf_counter()
# Input parsing
all_monkeys = []
monkey = None
#with open('input/test.2022day11.txt', 'r') as f:
with open('input/input.2022day11.txt', 'r') as f:
    for line in f:
        tokens = line.strip().split()
        if len(tokens) == 0:
            continue
        
        if tokens[0] == 'Monkey':
            monkey = Monkey()
            monkey.index = len(all_monkeys)
            all_monkeys.append(monkey)
        elif tokens[0] == 'Starting':
            monkey.items = [int(item.replace(',', ' ')) for item in tokens[2:]]
        elif tokens[0] == 'Operation:':
            arg = int(tokens[-1]) if tokens[-1].isnumeric() else None
            monkey.op = (tokens[-2], arg)
        elif tokens[0] == 'Test:':
            monkey.testval = int(tokens[-1])
        elif tokens[0] == 'If':
            if tokens[1] == 'true:':
                monkey.iftrue = int(tokens[-1])
            else:
                monkey.iffalse = int(tokens[-1])

#for monkey in all_monkeys:
#    print(monkey)
toc1 = time.perf_counter()

# Part 1. Loop through the monkeys 20 times
for rounds in range(20):
    for monkey in all_monkeys:
        while len(monkey.items) > 0:
            item = monkey.inspect(monkey.items.pop(0))
            all_monkeys[monkey.throwto(item)].additem(item)

counts = []
for monkey in all_monkeys:
    counts.append(monkey.inspect_count)

counts.sort(reverse=True)
toc2 = time.perf_counter()
print(f'Time to parse input = {(toc1 - tic) * 1000} ms')
print('Final inspection counts')
for monkey in all_monkeys:
    print(f'Monkey {monkey.index} inspected {monkey.inspect_count} items')

print(f'Top two counts = {counts[0:2]}')
print(f'Product = {counts[0] * counts[1]}')
print(f'Time for Part 1 = {(toc2 - toc1) * 1000} ms')