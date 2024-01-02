from graph import *
nodes = list(range(1, 12))
edges = [[1, 3], [1, 2], [2, 4], [10, 6],[3, 4], [4, 6], [4, 7], [4, 10], [4, 9], [7, 11], [11, 9], [7, 9], [6, 9], [6, 7], [2, 5], [2, 8], [5, 8]]
g = Graph(nodes, edges)
print(g.find_eulerian_cycle()) #[1, 3, 4, 7, 11, 9, 7, 6, 9, 4, 6, 10, 4, 2, 5, 8, 2, 1]