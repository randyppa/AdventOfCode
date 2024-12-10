#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
day09.py -- template

Created on Mon Dec  9 08:15 2024

Advent Of Code 2024, Day 9.

Part A: File system garbage collection
Part B: Garbage collection but keeping files contiguous

@author: rpoepa
"""

verbose = 0
sample = False
infile = 'input/day09.' + ('sample' if sample else 'input') + '.txt'

#=======================================
#  Functions and data structures
class Block:
    def __init__(self, startsector, nsectors, id):
        self.startsector = startsector
        self.nsectors = nsectors
        self.id = id
    
    def __lt__(self, other):
        return self.startsector < other.startsector
    
    def __gt__(self, other):
        return self.startsector > other.startsector
    
    def __eq__(self, other):
        return self.startsector == other.startsector
    
    def __str__(self):
        s = f'Block: sectors {self.startsector} - '
        s += f'{self.startsector + self.nsectors - 1}, '
        if self.id >= 0:
            s += f'ID = {self.id}'
        else:
            s += 'FREE'
        return s
    
    def checksum(self):
        if self.id < 0:
            return 0
        total = 0
        for sectorno in range(self.startsector, self.startsector + self.nsectors):
            total += sectorno * self.id
        return total
    
# Debug stuff
def print_freeblocks():
    for block in freeblocks:
        print(block)
    
def print_usedblocks():
    for block in usedblocks:
        print(block)

def print_allblocks():
    print_freeblocks()
    print_usedblocks()
#=======================================

#======== Begin main program =========
import time
import numpy as np

with open(infile, 'r') as fin:
    lines = fin.readlines()

tic = time.perf_counter()

#=========== parsing =======
blocks = [int(x) for x in lines[0].strip()]
nsectors = sum(blocks)

id = 0 
diskmap = -1 * np.ones((nsectors,),dtype='int')
free = False
sectorno = 0
freelist = []
usedblocks = []
freeblocks = []
for blocksize in blocks:
    block = Block(sectorno, blocksize, id)
    if not free:
        diskmap[sectorno:sectorno + blocksize] = id
        if blocksize > 0:
            usedblocks.append(block)
        id += 1
    else:
        block.id = -1
        if blocksize > 0:
            freeblocks.append(block)
    free = not free
    sectorno += blocksize
    if verbose > 1:
        print(block)
    
# List the free sectors = numbers from 1 to nblocks corresponding to a -1
# in the diskmap
sectornos = np.array([x for x in range(nsectors)])
freelist = sectornos[diskmap == -1]
usedlist = sectornos[diskmap >= 0]
if verbose > 1:
    for block in usedblocks:
        print(block)
    for block in freeblocks:
        print(block)

#======== The work =========
# Part A. Disk compression
lastused = usedlist[-1]
firstfree = freelist[0]
if verbose > 0:
    print(f'firstfree: {firstfree}, lastused = {lastused}')
while lastused > firstfree:
    # swap the contents of the last used sector and first free one
    diskmap[firstfree], diskmap[lastused] = \
        diskmap[lastused], diskmap[firstfree]
    # Take that now-used sector off the freelist and add the now-free sector
    freelist = np.concatenate((freelist[1:],[lastused]))
    usedlist = np.concatenate(([firstfree],usedlist[:-1]))
    lastused = usedlist[-1]
    firstfree = freelist[0]
    if verbose > 0:
        print(f'firstfree: {firstfree}, lastused = {lastused}')

# Compute checksum
checksum = sum(diskmap[usedlist] * usedlist)

tocA = time.perf_counter()
print(f'Part A: checksum = {checksum}')
print(f'Execution time = {(tocA - tic)*1000} ms')

# Part B: Operate on the freeblocks and usedblocks lists
# Search used blocks from the right, free blocks from the left
for block in usedblocks[::-1]:
    # Search for a free block this size with lower sectorno
    match = None
    for freeblock in freeblocks:
        if freeblock > block:
            break
        if freeblock < block and freeblock.nsectors >= block.nsectors:
            match = freeblock
            break
    
    if match is not None:
        # Do the move
        # Do we have to worry about merging free sectors into larger ones?
        # I don't think so. I think we won't be using this region again
        newfree = Block(block.startsector, block.nsectors, -1)
        freeblocks.append(newfree)
        block.startsector = match.startsector
        if match.nsectors > block.nsectors:  # There's a leftover free block
            match.startsector += block.nsectors
            match.nsectors -= block.nsectors
        else:  # no leftovers
            freeblocks.remove(match)
        if verbose > 0:
            print(f'Moved block with ID = {block.id}')
            print_allblocks()
    else:
        if verbose > 0:
            print(f'Can\'t move block with ID = {block.id}')
        
# Calculate checksum by blocks
checksum = 0
for block in usedblocks:
    checksum += block.checksum()
    
tocB = time.perf_counter()
print(f'Part B: checksum = {checksum}')
print(f'Execution time = {(tocB - tocA) * 1000} ms ')
print(f'Total execution time = {(tocB - tic) * 1000} ms ')

        
        

