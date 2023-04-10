import igraph as ig
import numpy as np
import argparse
import sys, os
sys.path.append(os.path.dirname(os.getcwd()))
from group_partitions import generate_2_allocations, utilities_adj, set_seed

parser = argparse.ArgumentParser(prog='EF-1 on Lattice Graphs')
parser.add_argument('--grid_size', type=int)
parser.add_argument('--nodes', type=int)
parser.add_argument('--seed', type=int, default=0)
parser.add_argument('--prob', type=float, default=0.5)
parser.add_argument('--check', type=int, default=1)
args = parser.parse_args()

set_seed(0)
node_cnt = [args.nodes] if args.nodes != -1 else [i for i in range(2, args.grid_size ** 2 + 1)]
for nodes in node_cnt:
    for _ in range(100):
        grid = np.arange(args.grid_size ** 2 + 1, dtype=int)
        choice = np.random.permutation(args.grid_size ** 2)[:nodes]
        points = grid[choice].tolist()
        coords = list(map(lambda point: np.array([point//args.grid_size, point%args.grid_size]), points))
        adj_graph = np.zeros((nodes, nodes))
        for i in range(nodes):
            for j in range(nodes):
                if i <= j:
                    break
                if np.sum(np.abs(coords[i] - coords[j])) == 1:
                    adj_graph[i, j] = 2*(np.random.rand() > args.prob) - 1
                    adj_graph[j, i] = adj_graph[i, j]
        ef_check = False
        for alloc in generate_2_allocations(nodes):
            if np.max(utilities_adj(adj_graph, alloc)['envy']) <= args.check:
                ef_check = True
                break
        if not ef_check:
            print(f"EF-{args.check} violated")
            print(coords)
            print(adj_graph.tolist())
            exit()
    print(f"Checked for {nodes} nodes")