# Hypothesis
# For each allocation with max-envy of >= 3, there exists at least one node swap that can bring the max-envy down by at least 1.

# FALSE
# Adjacency matrix - [[0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0], [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1], [0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1], [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0], [0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1], [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0], [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0], [0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0]]
# Allocation - [[0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1], [1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0]]

import numpy as np
import argparse
import igraph as ig
from group_partitions import generate_2_allocations, utilities, set_seed

def swap(alloc, x, y):
    result = np.copy(alloc)
    result[:, x] = alloc[:, y]
    result[:, y] = alloc[:, x]
    return result

parser = argparse.ArgumentParser(prog='Reducing Swap')
parser.add_argument('--nodes', type=int)
parser.add_argument('--edges', type=int)
args = parser.parse_args()

set_seed(0)
for _ in range(1000):
    g = ig.Graph.Erdos_Renyi(n=args.nodes, m=args.edges)
    for alloc in generate_2_allocations(args.nodes):
        util = utilities(g, alloc)
        swap_reduction = False
        if np.max(util['envy']) <= 2:
            continue
        for i in range(args.nodes):
            for j in range(args.nodes):
                if np.max(utilities(g, swap(alloc, i, j))['envy']) < np.max(util['envy']):
                        swap_reduction = True
        if not swap_reduction:
            print("Hypothesis negated")
            print(g.get_adjacency().data)
            print(alloc.tolist())
            exit()

print("Hypothesis verified")