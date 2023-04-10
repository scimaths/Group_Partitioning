import igraph as ig
import numpy as np
import argparse
import sys, os
sys.path.append(os.path.dirname(os.getcwd()))
from group_partitions import generate_2_allocations, utilities, set_seed

parser = argparse.ArgumentParser(prog='EF-1 on Lattice Graphs')
parser.add_argument('--grid_size', type=int)
parser.add_argument('--nodes', type=int)
parser.add_argument('--seed', type=int, default=0)
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
                if np.sum(np.abs(coords[i] - coords[j])) == 1:
                    adj_graph[i, j] = 1
        g = ig.Graph.Adjacency(adj_graph)
        ef1_check = False
        for alloc in generate_2_allocations(nodes):
            if np.max(utilities(g, alloc)['envy']) <= 1:
                ef1_check = True
                break
        if not ef1_check:
            print("EF-1 violated")
            print(coords)
            exit()
    print(f"Checked for {nodes} nodes")