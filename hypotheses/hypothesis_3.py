# Hypothesis
# For every graph with even number of nodes, there exists at least one allocation where envy >= 2 is present only for one colour.

import numpy as np
import argparse
import igraph as ig
import sys, os
sys.path.append(os.path.dirname(os.getcwd()))
from group_partitions import generate_2_allocations, utilities, set_seed

parser = argparse.ArgumentParser(prog='Even Node Induction')
parser.add_argument('--nodes', type=int)
parser.add_argument('--edges', type=int)
args = parser.parse_args()

set_seed(0)
if args.edges == -1:
    edges = range(args.nodes, (args.nodes * (args.nodes-1))//2 + 1)
else:
    edges = [args.edges]
for edge_cnt in edges:
    for idx in range(1000):
        g = ig.Graph.Erdos_Renyi(n=args.nodes, m=edge_cnt)
        pos = False
        for alloc in generate_2_allocations(args.nodes):
            envy = utilities(g, alloc)['envy']
            if np.max(envy) > 2:
                continue
            max_envies = np.max(envy, axis=1)
            max_groups = np.max(max_envies.reshape((1, -1)) * alloc, axis=1)
            if np.min(max_groups) <= 1:
                pos = True
                # print(f"Graph {idx} - found")
                break
        if not pos:
            print(f"Hypothesis negated for {edge_cnt} edges")
            print(g.get_adjacency().data)
            exit()
    print(f"Hypothesis verified for {edge_cnt} edges")