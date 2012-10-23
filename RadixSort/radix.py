#!/usr/bin/python
import sys
from collections import defaultdict
from pprint import pprint as pp

def radixSort(t):
    trie = defaultdict(list)
    
    for l in t:
        idx = ord(l[0])
        trie[idx].append(l)
    
    pp(trie)


def main():
    if len(sys.argv) < 2:
        printUsage()
        sys.exit(1)

    lines = []
    with open(sys.argv[1], 'r') as f:
        for l in f:
            lines.append(l)
    
    radixSort(lines)


def printUsage():
    print "Usage: radix <in file>"


if __name__ == "__main__":
    main()
