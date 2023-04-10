import igraph as ig
import numpy as np
from group_partitions import utilities

def my_draw_networkx_edge_labels(
    G,
    pos,
    edge_labels=None,
    label_pos=0.5,
    font_size=10,
    font_color="k",
    font_family="sans-serif",
    font_weight="normal",
    alpha=None,
    bbox=None,
    horizontalalignment="center",
    verticalalignment="center",
    ax=None,
    rotate=True,
    clip_on=True,
    rad=0
):
    """Draw edge labels.

    Parameters
    ----------
    G : graph
        A networkx graph

    pos : dictionary
        A dictionary with nodes as keys and positions as values.
        Positions should be sequences of length 2.

    edge_labels : dictionary (default={})
        Edge labels in a dictionary of labels keyed by edge two-tuple.
        Only labels for the keys in the dictionary are drawn.

    label_pos : float (default=0.5)
        Position of edge label along edge (0=head, 0.5=center, 1=tail)

    font_size : int (default=10)
        Font size for text labels

    font_color : string (default='k' black)
        Font color string

    font_weight : string (default='normal')
        Font weight

    font_family : string (default='sans-serif')
        Font family

    alpha : float or None (default=None)
        The text transparency

    bbox : Matplotlib bbox, optional
        Specify text box properties (e.g. shape, color etc.) for edge labels.
        Default is {boxstyle='round', ec=(1.0, 1.0, 1.0), fc=(1.0, 1.0, 1.0)}.

    horizontalalignment : string (default='center')
        Horizontal alignment {'center', 'right', 'left'}

    verticalalignment : string (default='center')
        Vertical alignment {'center', 'top', 'bottom', 'baseline', 'center_baseline'}

    ax : Matplotlib Axes object, optional
        Draw the graph in the specified Matplotlib axes.

    rotate : bool (deafult=True)
        Rotate edge labels to lie parallel to edges

    clip_on : bool (default=True)
        Turn on clipping of edge labels at axis boundaries

    Returns
    -------
    dict
        `dict` of labels keyed by edge

    Examples
    --------
    >>> G = nx.dodecahedral_graph()
    >>> edge_labels = nx.draw_networkx_edge_labels(G, pos=nx.spring_layout(G))

    Also see the NetworkX drawing examples at
    https://networkx.org/documentation/latest/auto_examples/index.html

    See Also
    --------
    draw
    draw_networkx
    draw_networkx_nodes
    draw_networkx_edges
    draw_networkx_labels
    """
    import matplotlib.pyplot as plt
    import numpy as np

    if ax is None:
        ax = plt.gca()
    if edge_labels is None:
        labels = {(u, v): d for u, v, d in G.edges(data=True)}
    else:
        labels = edge_labels
    text_items = {}
    for (n1, n2), label in labels.items():
        (x1, y1) = pos[n1]
        (x2, y2) = pos[n2]
        (x, y) = (
            x1 * label_pos + x2 * (1.0 - label_pos),
            y1 * label_pos + y2 * (1.0 - label_pos),
        )
        pos_1 = ax.transData.transform(np.array(pos[n1]))
        pos_2 = ax.transData.transform(np.array(pos[n2]))
        linear_mid = 0.5*pos_1 + 0.5*pos_2
        d_pos = pos_2 - pos_1
        rotation_matrix = np.array([(0,1), (-1,0)])
        ctrl_1 = linear_mid + rad*rotation_matrix@d_pos
        ctrl_mid_1 = 0.5*pos_1 + 0.5*ctrl_1
        ctrl_mid_2 = 0.5*pos_2 + 0.5*ctrl_1
        bezier_mid = 0.5*ctrl_mid_1 + 0.5*ctrl_mid_2
        (x, y) = ax.transData.inverted().transform(bezier_mid)

        if rotate:
            # in degrees
            angle = np.arctan2(y2 - y1, x2 - x1) / (2.0 * np.pi) * 360
            # make label orientation "right-side-up"
            if angle > 90:
                angle -= 180
            if angle < -90:
                angle += 180
            # transform data coordinate angle to screen coordinate angle
            xy = np.array((x, y))
            trans_angle = ax.transData.transform_angles(
                np.array((angle,)), xy.reshape((1, 2))
            )[0]
        else:
            trans_angle = 0.0
        # use default box of white with white border
        if bbox is None:
            bbox = dict(boxstyle="round", ec=(1.0, 1.0, 1.0), fc=(1.0, 1.0, 1.0))
        if not isinstance(label, str):
            label = str(label)  # this makes "1" and 1 labeled the same

        t = ax.text(
            x,
            y,
            label,
            size=font_size,
            color=font_color,
            family=font_family,
            weight=font_weight,
            alpha=alpha,
            horizontalalignment=horizontalalignment,
            verticalalignment=verticalalignment,
            rotation=trans_angle,
            transform=ax.transData,
            bbox=bbox,
            zorder=1,
            clip_on=clip_on,
        )
        text_items[(n1, n2)] = t

    ax.tick_params(
        axis="both",
        which="both",
        bottom=False,
        left=False,
        labelbottom=False,
        labelleft=False,
    )

    return text_items

def visualize_graph_2_allocation(g: ig.Graph, alloc: np.ndarray, pos=None):
    import networkx as nx
    import matplotlib.pyplot as plt
    
    G_adj = nx.Graph()
    G_envy = nx.DiGraph()
    color_map = []
    num_nodes = alloc.shape[1]
    util = utilities(g, alloc)
    G_adj.add_nodes_from([i for i in range(num_nodes)])
    G_envy.add_nodes_from([i for i in range(num_nodes)])
    
    for node in range(num_nodes):
        color_map.append('red' if np.argmax(alloc[:,node]) == 1 else 'blue')
    
    adj_list = g.get_adjacency().data
    for i in range(num_nodes):
        for j in range(num_nodes):
            if i > j and adj_list[i][j] == 1:
                G_adj.add_edge(i, j)
                G_adj[i][j]['color'] = 'black'
    
    for i in range(num_nodes):
        for j in range(num_nodes):
            if util['envy'][i, j] > 0:
                G_envy.add_edge(i, j)
                G_envy[i][j]['color'] = 'green'
                G_envy[i][j]['label'] = util['envy'][i, j]

    curved_edges = [edge for edge in G_envy.edges() if reversed(edge) in G_envy.edges()]
    straight_edges = list(set(G_envy.edges()) - set(curved_edges))

    plt.close('all')
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(20, 10))
    ax[0].set_title('Adjacency Graph', fontsize=30)
    ax[1].set_title('Envy Graph', fontsize=30)

    if not pos:
        pos = nx.spring_layout(G_adj, k=5)
    nx.draw(G_adj, pos=pos, node_color=color_map, ax=ax[0], with_labels=True, node_size=1000)
    # nx.draw(G_envy, pos=pos, node_color=color_map, ax=ax[1], with_labels=True, node_size=1000)
    
    nx.draw_networkx_nodes(G_envy, pos, ax=ax[1], node_color=color_map, node_size=300)
    nx.draw_networkx_labels(G_envy, pos, ax=ax[1])
    nx.draw_networkx_edges(G_envy, pos=pos, edgelist=straight_edges, ax=ax[1], arrowsize=30, arrowstyle='-|>')
    nx.draw_networkx_edge_labels(G_envy, pos=pos, ax=ax[1], edge_labels={(i, j): G_envy[i][j]['label'] for i, j in straight_edges}, rotate=False, font_color='red', label_pos=0.5)
    
    arc_rad = 0.1
    nx.draw_networkx_edges(G_envy, pos=pos, edgelist=curved_edges, ax=ax[1], connectionstyle=f'arc3, rad = {arc_rad}', arrowsize=30, arrowstyle='-|>')
    my_draw_networkx_edge_labels(G_envy, pos=pos, ax=ax[1], edge_labels={(i, j): G_envy[i][j]['label'] for i, j in curved_edges}, rotate=False, rad=arc_rad, font_color='red', label_pos=0.5)

    plt.show()

    return pos