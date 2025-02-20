#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
import networkx as nx
from itertools import pairwise
from functools import cache

## Current file direction
cfd = Path(__file__).parent.absolute()

## Read input
with open(str(cfd) + '/data/D21_input.txt', 'r') as f:
    lines = f.read().splitlines()

numpad = {
    0: '7',
    1j: '8',
    2j: '9',
    1: '4',
    1 + 1j: '5',
    1 + 2j: '6',
    2: '1',
    2 + 1j: '2',
    2 + 2j: '3',
    3: None,
    3 + 1j: '0',
    3 + 2j: 'A',
}

keypad = {
    0: None,
    1j: '^',
    2j: 'A',
    1: '<',
    1 + 1j: 'v',
    1 + 2j: '>',
}

fourdir = {1: 'v', -1: '^', 1j: '>', -1j: '<'}

def shortest_paths(grid):
    G = nx.DiGraph((z, z + dz) for z in grid for dz in fourdir if grid.get(z + dz))

    return {
        (grid[start], grid[end]): [
            ''.join(fourdir[v - u] for u, v in pairwise(path)) for path in paths
        ]
        for start, ends in nx.all_pairs_all_shortest_paths(G)
        for end, paths in ends.items()
    }

shortest_numpad = shortest_paths(numpad)
shortest_keypad = shortest_paths(keypad)

@cache
def shortest_path_length(bot, keys, target_bot):
    if bot == target_bot + 1:
        return len(keys)
    all_shortest = shortest_keypad if bot else shortest_numpad
    return sum(
        min(
            shortest_path_length(bot + 1, path + 'A', target_bot)
            for path in all_shortest[start, end]
        )
        for start, end in pairwise('A' + keys)
    )

comp = sum(int(code[:-1]) * shortest_path_length(0, code, 2) for code in lines)

print(f'The sum of the complexities is {comp} (2 robot case).')

comp = sum(int(code[:-1]) * shortest_path_length(0, code, 25) for code in lines)

print(f'The sum of the complexities is {comp} with 25 directional keypads.')