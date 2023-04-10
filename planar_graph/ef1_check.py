import igraph as ig
import numpy as np
import argparse
import sys, os
sys.path.append(os.path.dirname(os.getcwd()))
from group_partitions import generate_2_allocations, utilities, set_seed
from generate_random import planar_graph

parser = argparse.ArgumentParser(prog='EF on Planar Graphs')
parser.add_argument('--nodes', type=int)
parser.add_argument('--seed', type=int, default=0)
args = parser.parse_args()

set_seed(0)
node_cnt = [args.nodes] if args.nodes != -1 else range(10, 30)
for nodes in node_cnt:
    total_nodes = 0
    total_edges = 0
    for _ in range(100):
        adj_graph = planar_graph(nodes)
        g = ig.Graph.Adjacency(adj_graph)
        total_nodes += adj_graph.shape[0]
        total_edges += adj_graph.sum()
        ef1_check = False
        ef2_check = False
        for alloc in generate_2_allocations(adj_graph.shape[1]):
            if np.max(utilities(g, alloc)['envy']) <= 2:
                ef2_check = True
            if np.max(utilities(g, alloc)['envy']) <= 1:
                ef1_check = True
                break
        if not ef2_check:
            print("EF-2 violated")
            print(adj_graph)
            exit()
        elif not ef1_check:
            print("EF-1 violated")
    print(f"Checked for {nodes} nodes, avg size", total_nodes/100, total_edges/100)