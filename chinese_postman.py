from graph import *
#Defines an unweighted graph
nodes = list(range(9))
edges = [[0, 4], [1, 4], [1, 5], [1, 7], [7, 8], [5, 8], [4, 3], [5, 3], [3, 6], [6, 8], [8, 2], [5, 4]]
g = Graph(nodes, edges)
#returns a new pseudograph and th edges that were duplicated to obtain it
g_new, dup_edges = g.chinese_postman()
print(g.chinese_postman()[1]) #(0, 4) (4, 3), (1, 5), (5, 8), (8, 2)

nodes = list(range(8))
edges = [[0, 2], [0, 7], [0, 4], [1, 7], [1, 4], [1 ,6], [2, 3], [3, 4], [4, 5], [5, 6]]
g = Graph(nodes, edges)
print(g.chinese_postman()[1]) # (0, 4), (4, 1)

#This is an example of a weighted graph
nodes = list(range(8))
edges = [[0, 1, 12], [0, 6, 19], [0, 7, 21], [1, 2, 17], [1, 6, 22], [1, 3, 35], 
         [2, 6, 12], [2, 4, 15], [2, 3, 19], [3, 4, 21], [3, 5, 29], [4, 5, 20], [4, 7, 30], [4, 6, 7], 
         [5, 7, 14], [6, 7, 8]]
g = Graph(nodes, edges, weighted=True)
g_new, dup_edges = g.chinese_postman()
print(g_new.total_graph_weight()) # 340
print(dup_edges) # (0, 6), (4, 5)

