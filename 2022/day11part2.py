#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advent of Code, Day 11, Part 2

Though it's only a slight change in the rules, I opted to create a separate
code for Part 2.'

Read in a description of "monkeys", the items they hold (value is a 
"worry level") and rules for passing the items around and modifying the
worry levels.

Part 1: Levels were divided by 3 on each inspection, and the process ran for
20 rounds. Here worries are not divided, and the procexss runs for 10000
rounds.

As a result, the numbers quickly become huge and arithmetic becomes unwieldy
to the point that 10000 iterations may take hours or days. Instead of direct
arithmetic, a modulo approach is used.

Created on Sun Dec 11 07:46:47 2022

@author: randyppa
"""
import time


class Item:
    def __init__(self, value, keys):
        self.modvals = {key:value % key for key in keys}
    
    def mult(self, other):
        for key, val in self.modvals.items():
            self.modvals[key] = (val * (other % key)) % key
    
    def add(self, other):
        for key, val in self.modvals.items():
            self.modvals[key] = (val + other) % key
    
    def square(self):
        for key, val in self.modvals.items():
            self.modvals[key] = (val * val) % key
    
    def __str__(self):
        return str(self.modvals)
        
class Monkey:
    def __init__(self):
        self.index = 0      # Counter: Not used, just for debug
        self.start_vals = []     # Initial value of items
        self.op = ('*',1)   # Worry modification rule
        self.testval = 1    # Divisibility test
        self.iftrue = 0     # Where to throw if divisible
        self.iffalse = 0    # Where to throw if not divisible
        self.inspect_count = 0
        self.items = []
        self.itemkeys = []
    
    def addvalue(self, value):
        self.start_vals.append(value)
    
    def additem(self, item):
        self.items.append(item)
    
    def set_item_keys(self, keys):
        self.items = [Item(val, keys) for val in self.start_vals]

    def inspect(self, item):      # Perform inspection rules
        self.inspect_count += 1
        
        # Step 1: Perform the operation
        # A rule like new = old * old is encoded as ('*', None)
        if self.op[0] == '*':
            if self.op[1] is None:
                item.square()
            else:
                item.mult(self.op[1])
        else:
            item.add(self.op[1])
        
        return item
            
    def throwto(self, item):
        if item.modvals[self.testval] == 0:
            return self.iftrue
        else:
            return self.iffalse
    
    # Pretty print
    def __str__(self):
        output = f'Monkey {self.index}:\n'
        output += '  Items' 
        for item in self.items:
            output += '\n    ' + str(item)
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
            for item in tokens[2:]:
                monkey.addvalue(int(item.replace(',', ' ')))
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

toc1 = time.perf_counter()

# Build the modular representations
keys = [monkey.testval for monkey in all_monkeys]
for monkey in all_monkeys:
    monkey.set_item_keys(keys)
    print(monkey)

# Part 2. Loop through the monkeys 10000 times
for rounds in range(10000):
    for monkey in all_monkeys:
        while len(monkey.items) > 0:
            item = monkey.inspect(monkey.items.pop(0))
            all_monkeys[monkey.throwto(item)].additem(item)
    # if rounds % 500 == 49:
    #     toc2 = time.perf_counter()
    #     print(f'Round {rounds+1} done. Time so far = {toc2 - toc1} ')

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
print(f'Time for Part 2 = {toc2 - toc1} ms')