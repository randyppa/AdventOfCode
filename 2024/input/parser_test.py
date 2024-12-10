#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
parser_test.py

Created on Tue Dec  3 20:12:10 2024

For testing of the general parser code being developed on the Day 03 problem.

@author: rpoepa
"""

class Parser:
    def __init__(self, token_file):
        self.load_tokens(token_file)

    def load_tokens(self, token_file):
        with open(token_file, 'r') as fin:
            lines = fin.readlines()
        for line in lines:
            # Remove whitespace and any comments
            line = line.strip()
            comment = line.find("#")
            if comment >= 0:
                line = line[:comment]
            if len(line) == 0:
                continue
            
            # Now parse the token definitions.
            
from ply.lex import lex

# Tokens
tokens = (
    'MUL',
    'DO',
    'DONT',
    'NUM',
    'LPAREN',
    'RPAREN',
    'COMMA'
    )

# Simple token rules
t_MUL = r"mul"
t_DO = r"do"
t_DONT = r"don't"
t_LPAREN = "\("
t_RPAREN = "\)"
t_COMMA = ","

# Complex token rules
def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex()

sample = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

lexer.input(sample)
while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)
#P = Parser('input/day03.tokens')