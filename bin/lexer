#!/usr/bin/env python

import os.path
import sys

sys.path.extend(['./src/','../src/'])

import lex
from tokenizer import tokenizer

def Print():
    print('%20s   %20s   %20s'%("Token", "Occurrances", "Lexemes",))
    print('_'*70)
    print()

    for i,j in table.items():
        if j[0] == 0:
            continue
        else:
            k = list(j[1])
            l = len(k)
            print('%20s    %20d   %20s'%(i, j[0], k[0],))
            for x in range(1,l):
                print('%20s    %20s   %20s'%("", "", k[x],))

if __name__ == "__main__":
    tokens = tokenizer.tokens
    table = { k:[0,set()] for k in tokens}
    lexer = lex.lex(module=tokenizer())
    filename = sys.argv[1]
    if os.path.exists(filename):
        file = open(filename, 'r')
        data = file.read()
        lexer.input(data)
        while True:
            tokk = lexer.token()
            if not tokk: break
            table[tokk.type][0] += 1
            table[tokk.type][1].add(tokk.value)
        file.close()
    else:
        print("File Does Not Exist")
    Print()
