import igraph as ig
import numpy as np
import random

random.seed(0)

def utilities(g: ig.Graph, allocation: np.ndarray):
    k, n = allocation.shape
    graph_adj = np.array(g.get_adjacency().data)
    assert n == graph_adj.shape[0]

    utilities = graph_adj @ allocation.T
    cross_utilities = utilities @ allocation - graph_adj
    # cross_allocation = (allocation.T @ allocation).astype(np.bool)
    # cross_utilities[cross_allocation == True] = -1
    envy = np.maximum(0, cross_utilities - np.diag(cross_utilities).reshape(-1, 1))
    print(graph_adj)
    print(cross_utilities)
    print(envy)

n = 5
k = 2

alloc = np.array([
    [0, 1, 1, 1, 0],
    [1, 0, 0, 0, 1]
])

g = ig.Graph.Erdos_Renyi(n=n, m=6)

utilities(g, alloc)