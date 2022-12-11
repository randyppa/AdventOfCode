#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advent of Code, Day 10.

Part 1. Decode an elf assembly-language program and calculate execution times
and values in a register.

Part 2. Add drawing to the program

Created on Sat Dec 10 07:58:02 2022

@author: randyppa
"""

import time

def render(ram, row_len):
    ram_size = len(ram)
    for pix in range(0, ram_size, row_len):
        print(''.join(ram[pix:pix + row_len]))


tic = time.perf_counter()

# Some useful numbers
timing = {'noop':1, 'addx':2}  # Command duration in cycles
magic = [20, 60, 100, 140, 180, 220]   # When to check register value

program = []
# Read the command lines.
# There are only two commands: noop (do nothing) and addx (add the argument
# to the x register)
#with open('input/test.2022day10.txt', 'r') as f:
with open('input/input.2022day10.txt', 'r') as f:
    for line in f:
        # "compile" into command, effect on x register, and instruction time
        cmd = line.strip().split(' ')
        tokens = [cmd[0], 0, 0]
        if tokens[0] == 'addx':
            tokens[1] = int(cmd[1])
        tokens[2] = timing[cmd[0]]
        
        program.append(tokens)

toc = time.perf_counter()

# Part 1: Execute the program
x_reg = 1 # WARNING! BOTH OF THESE START AT 1, NOT 0!
cycle = 1
check = 0
next_check = magic[check]
total_value = 0
for cmd in program:
    cycle_end = cycle + cmd[2]
    if next_check >= cycle and next_check < cycle_end:
        total_value += x_reg * next_check
        check += 1
        if check < len(magic):
            next_check = magic[check]
    x_reg += cmd[1]
    cycle = cycle_end

toc2 = time.perf_counter()

# Part 2: Execute and draw
x_reg = 1
cycle = 1
pixel = 0 # This cycles 0-39
rows = 10
ram_size = rows * 40
screen_ram = ['.' for _ in range(ram_size)]
row = 0  # Increments by 1 every 40
for cmd in program:
    cycle_end = cycle + cmd[2]
    while cycle < cycle_end:
        if pixel >= x_reg - 1 and pixel <= x_reg + 1:
            screen_ram[cycle - 1] = '#'
        cycle += 1
        pixel += 1
        if pixel >= 40:
            pixel = 0
    x_reg += cmd[1]

toc3 = time.perf_counter()

print(f'Time for input processing = {(toc - tic) * 1000} ms')
print(f'Time to execute Elf program = {(toc2 - toc) * 1000} ms')
print(f'Part 1: Total of signal values = {total_value}')
        
# Display the contents of screen RAM, 40 pixels per row
print('Part 2:')
render(screen_ram, 40)

print(f'Time for Part 2 = {(toc3 - toc2) * 1000} ms')
