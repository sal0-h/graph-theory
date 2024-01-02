
import math
from graph import Graph
#Example on a directed graph
n = 5
edges=[[0,1,10],[0,2,3],[1,3,2],[2,1,4],[2,3,8],[2,4,2],[3,4,5]]
src = 1
g = Graph(list(range(n)), edges, directed=True, weighted=True)
result = g.shortestPath(src)
#Result is in this formal
# {
#     node1 : {
#             length : length_of_path,
#             path : [src, v1, v2, ..., node1]
#             },
#     node2 : {
#             length : num
#             path : [src, v1, v2, ..., node2]
#             }
#     }