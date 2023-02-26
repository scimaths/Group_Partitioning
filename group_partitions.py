import igraph as ig
import numpy as np
import random
import argparse

parser = argparse.ArgumentParser(prog='Simulating group partitioning')
parser.add_argument('--num_graphs', type=int)
parser.add_argument('--nodes', type=int)
parser.add_argument('--seed', type=int, default=0)
parser.add_argument('--prob', type=float, default=0.7)

def set_seed(seed=0):
    np.random.seed(seed)
    random.seed(seed)

def generate_2_allocations(num: int):
    size = (num + 1)//2
    for i in range(2**(num-1)):
            bitmask = format(i, 'b').zfill(num)
            if bitmask.count('1') != size and bitmask.count('0') != size:
                continue
            indices = [i for i in range(num) if bitmask[i] == "1"]
            allocation = np.zeros((2, num))
            allocation[:, indices] = 1
            allocation[1, :] = 1-allocation[1, :]
            yield allocation

def test_generate_2_allocations():
    for num in range(2, 21):
        count = 0
        for _ in generate_2_allocations(num):
            count += 1
        print(num, count)

def utilities(g: ig.Graph, allocation: np.ndarray):
    k, n = allocation.shape
    graph_adj = np.array(g.get_adjacency().data)
    assert n == graph_adj.shape[0]

    utilities = graph_adj @ allocation.T
    cross_utilities = utilities @ allocation - graph_adj
    # cross_allocation = (allocation.T @ allocation).astype(np.bool)
    # cross_utilities[cross_allocation == True] = -1
    envy = np.maximum(0, cross_utilities - np.diag(cross_utilities).reshape(-1, 1))
    return {
        'cross_utilities': cross_utilities,
        'envy': envy
    }

def test_utilities():
    n = 5
    k = 2
    alloc = np.array([
        [0, 1, 1, 1, 0],
        [1, 0, 0, 0, 1]
    ])
    g = ig.Graph.Erdos_Renyi(n=n, m=6)
    print(utilities(g, alloc))

def get_min_envy_2_allocation(g: ig.Graph):
    n = len(g.get_adjacency().data)
    min_envy = n
    best_alloc = None
    for alloc in generate_2_allocations(n):
        util = utilities(g, alloc)
        if min_envy > np.max(util['envy']):
            best_alloc = alloc
            min_envy = int(np.max(util['envy']))
    return {
        'min_envy': min_envy,
        'swap_tuple': np.unravel_index(np.argmax(util['envy']), (n, n)),
        'best_alloc': best_alloc
    }

def test_ef_max(n, num_graphs=1000, seed=0, prob=0.7):
    set_seed(seed)
    filename = f"logs/log_{n}_{num_graphs}.txt"
    with open(filename, 'w') as f:
        f.write(f"Experiment with {num_graphs} graphs, number of nodes = {n}, seed = {seed}, edge-prob = {prob}\n\n")
    max_envy = 0
    for _ in range(num_graphs):
        g = ig.Graph.Erdos_Renyi(n=n, p=prob)
        result = get_min_envy_2_allocation(g)
        if result['min_envy'] > max_envy:
            max_envy = result['min_envy']
            with open(filename, 'a') as f:
                f.write(f"Envy of {max_envy} found, swap {result['swap_tuple']}\n")
                f.write(f"{'-'*12}GRAPH{'-'*13}\n" + str(np.array(g.get_adjacency().data)) + "\n")
                f.write(f"{'-'*10}ALLOCATION{'-'*10}\n" + str(result['best_alloc']) + "\n\n")
    with open(filename, 'a') as f:
        f.write(f"Experiment complete")

if __name__ == "__main__":
    args = parser.parse_args()
    test_ef_max(args.nodes, args.num_graphs, args.seed, args.prob)