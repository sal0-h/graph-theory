from graph import *
nodes = list(range(6))
edges = [[0, 1, 1], [0, 2, 3], [0, 4, 1], [0, 5, 4], [1, 4, 2], [1, 2, 1], [2, 3, 3], [3, 4, 1], [3, 5, 2], [4, 5, 2]]
g = Graph(nodes, edges, directed=False, weighted=True)
g.show('basic.html')
d = g.shortest_distances_all_pairs()