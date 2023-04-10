import numpy as np
import networkx as nx
from scipy.spatial import Voronoi,voronoi_plot_2d
import matplotlib.pyplot as plt

#we create a function to generate a planar graph from a voronoi diagram

def voronoi_to_networkx(points):
    # we get the voronoi diagram
    vor = Voronoi(points)
    G = nx.Graph()
    # Add an edge for each ridge in the Voronoi diagram that connects two points in the range [0,1] 
    for simplex in vor.ridge_vertices:
        if -1 not in simplex:
            i, j = simplex
            p = vor.vertices[i]
            q = vor.vertices[j]
            if 0 <= p[0] <= 1 and 0 <= p[1] <= 1 and 0 <= q[0] <= 1 and 0 <= q[1] <= 1:
                distance = np.linalg.norm(p - q) # Calculate the Euclidean distance between p and q
                G.add_edge(tuple(p), tuple(q),weight=distance)
    return G

def planar_graph(num_nodes: int):
    points=np.random.rand(num_nodes, 2)
    graph=voronoi_to_networkx(points)
    return (nx.adjacency_matrix(graph).toarray() > 1e-5).astype(np.int32)

if __name__ == "__main__":
    print(planar_graph(20))