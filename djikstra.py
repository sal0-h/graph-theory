
import math
from graph import Graph
# n - num of vertices
def shortestPath(n, edges, src, dest):
    done_vertices = [src]
    temp_vertices = {i for i in range(n)}
    temp_vertices.remove(src)
    g = Graph([i for i in range(n)], edges, True, True)
    adj = g.adjacency_dict()
    labels = []
    init_labels(labels, src, n)    

    while True: #n
        current_vertex = done_vertices[-1]
        for (v, w) in adj[current_vertex]:#n - 1 
            if v in temp_vertices and labels[current_vertex][0] + w < labels[v][0]:
                labels[v][0] = labels[current_vertex][0] + w
                labels[v][1] = current_vertex
        min_weight = math.inf
        min_vertex = None
        for v in temp_vertices: # n
            if labels[v][0] < min_weight:
                min_weight = labels[v][0]
                min_vertex = v
        if min_weight == math.inf:
            for v in temp_vertices: #n
                labels[v][0] = -1
            temp_vertices = set()
        else:
            done_vertices.append(min_vertex)
            temp_vertices.remove(min_vertex) #n
        if temp_vertices == set():
            break
    output = dict()
    for v in range(n):
        output[v] = labels[v][0]
    final_path = [dest]
    current_vertex = dest
    while labels[current_vertex][1] != None:
        current_vertex = labels[current_vertex][1]
        final_path.insert(0, current_vertex)
    print("Path: ", final_path) if labels[dest][0] != -1 else print('No path exists')
    print(output)

def init_labels(labels, src, n):
    for i in range(n):
        labels.append([math.inf, None])
    labels[src] = [0, None]

#10
    
# 4
n=5
edges=[[0,1,10],[0,2,3],[1,3,2],[2,1,4],[2,3,8],[2,4,2],[3,4,5]]
src = 1
dest = 0
shortestPath(n, edges, src, dest)
g = Graph(list(range(n)), edges, directed=True, weighted=True)
g.show('basic.html')
print(g.shortestPath(src))

print(g.total_graph_weight())