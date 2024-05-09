from graph import Graph

nodes = ['A', 'B', 'C', 'D', 'E']
edges = [['A', 'B', 1], ['A', 'C', 7], ['A', 'D', 10], ['A', 'E', 5], 
         ['B', 'C', 3], ['C', 'D', 4], ['D', 'E', 2]]
G = Graph(nodes, edges, weighted=True)
T = G.kruskal()
T.show("kruskal.html")