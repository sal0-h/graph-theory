from graph import *
nodes = list(range(1, 12))
edges = [[1, 3], [1, 2], [2, 4], [10, 6],[3, 4], [4, 6], [4, 7], [4, 10], [4, 9], [7, 11], [11, 9], [7, 9], [6, 9], [6, 7], [2, 5], [2, 8], [5, 8]]
g = Graph(nodes, edges)
g.show('basic.html')

# def find_eulerian_cycle(g):
#     #Create the adjacency dict
#     adj = g.adjacency_dict()
#     eulerian = True
#     #Checks if graph eulerian - all nodes must be even
#     for node in adj:
#         if len(adj[node]) % 2 != 0:
#             eulerian = False
#     if eulerian:
#         #Generate any cycle v0 v1 v2 .... v0 
#         start = g.nodes[0]
#         path = generate_cycle(adj, start)
#         #While the cycle is not eulerian (not all edges added)
#         while len(path) - 1 < len(g.edges):
#             #clean up the adj by removing the nodes with no edges
#             for node in copy.deepcopy(adj):
#                 if adj[node] == []:
#                     del adj[node]
#             #find a node that connects to the existing path
#             for node in adj:
#                 if node in path:
#                     #make a cycle with the connector node, with the new adj
#                     start = node
#                     inner_path = generate_cycle(adj, start)
#                     #cut the old path and paste the new one in place of the connecting vertex
#                     for i in range(len(path)):
#                         if path[i] == start:
#                             path = path[:i] + inner_path + path[i + 1:]
#                             break
#                     break
#         #Once thats done, the path is completed
#         return path
#     else:
#         return None
    
# def generate_cycle(adj, start):
#     path = [start]
#     current = start
#     while True:
#         while current in adj[current]:
#             path.append(current)
#             adj[current].remove(current)
#             adj[current].remove(current)
#         prev = current
#         current = None
#         for node in adj[prev]:
#             if node != start and node != prev:
#                 current = node
#                 break
#         if current == None: 
#             current = start
#         path.append(current)
#         adj[prev].remove(current)
#         adj[current].remove(prev)
#         if current == start:
#             break
#     return path

    
# print(find_eulerian_cycle(g))
print(g.find_eulerian_cycle())