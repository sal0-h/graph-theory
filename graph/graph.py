from pyvis.network import Network
from itertools import permutations
import copy, math

class Graph:
    def __init__(self, nodes : list, edges : list, directed=False, weighted=False):
        self.nodes = nodes #list of nodes - [node, node, node]
        self.edges = edges #list of edges - [[node, node, weight], [node, node, weight]] if weighted
        #no weights if not weighted
        self.directed = directed
        self.weighted = weighted

    def adjacency_dict(self):
        """
        Returns the adjacency list of the graph
        """
        adj_dict = dict()
        for node in self.nodes:
            adj_dict[node] = []
        for edge in self.edges:
            node1, node2 = edge[0], edge[1]
            #if graph is weighted, it is in this format:
            #{node : [(node1, weight), (node2, weight),,,]}
            if self.weighted:
                weight = edge[2]
                adj_dict[node1].append((node2, weight))
                if not self.directed:
                    adj_dict[node2].append((node1, weight))
            else:
                adj_dict[node1].append(node2)
                if not self.directed:
                    adj_dict[node2].append(node1)
        return adj_dict

    def adjacency_matrix(self):
        """
        Returns the adjacency matrix of the graph.
        Assumes that graph.nodes is a list of nodes from 0 to n.
        """
        adj_mat = [[0 for node in self.nodes] for node in self.nodes]
        for edge in self.edges:
            node1, node2 = edge[0], edge[1]
            if self.weighted:
                weight = edge[2]
                adj_mat[node1][node2] += weight
                if not self.directed:
                    adj_mat[node2][node1] += weight
            else:
                adj_mat[node1][node2] += 1
                if not self.directed:
                    adj_mat[node2][node1] += 1
        return adj_mat


    def show(self, output_filename):
        """
        Saves an HTML file locally containing a visualization of the graph
        Returns a pyvis Network instance of the graph.
        """
        g = Network(directed=self.directed)
        g.set_edge_smooth('dynamic')
        node_list = []
        for i in self.nodes:
            node_list.append(f".{i}.")
        g.add_nodes(node_list, title = [str(i) for i in self.nodes])
        edge_list = copy.deepcopy(self.edges)
        for i, edg in enumerate(edge_list):
            start = f".{edg[0]}."
            end = f".{edg[1]}."
            edge_list[i] = [start, end]
        if not self.weighted:
            g.add_edges(edge_list)
        else:
            for i in range(len(edge_list)):
                g.add_edge(edge_list[i][0], edge_list[i][1], label = str(self.edges[i][2]))
        g.show(output_filename)
        return g
    
    def find_eulerian_cycle(self):
        """
        Find a eulerian cycle inside the graph if one exists and returns the vertices of the cycle
        If no path exists, returns None
        """
        #Create the adjacency dict
        adj = self.adjacency_dict()
        #Checks if graph eulerian - all nodes must be even and graph must be connected
        for node in adj:
            if len(adj[node]) % 2 != 0 or len(adj[node]) == 0:
                return None
        #Generate any cycle v0 v1 v2 .... v0 
        start = self.nodes[0]
        path = self.generate_cycle(adj, start)
        #While the cycle is not eulerian (not all edges added)
        while len(path) - 1 < len(self.edges):
            #clean up the adj by removing the nodes with no edges
            for node in copy.deepcopy(adj):
                if adj[node] == []:
                    del adj[node]
            #find a node that connects to the existing path
            for node in adj:
                if node in path:
                    #make a cycle with the connector node, with the new adj
                    start = node
                    inner_path = self.generate_cycle(adj, start)
                    #cut the old path and paste the new one in place of the connecting vertex
                    for i in range(len(path)):
                        if path[i] == start:
                            path = path[:i] + inner_path + path[i + 1:]
                            break
                    break
        #Once thats done, the path is completed
        return path
        
    def generate_cycle(self, adj, start):
        '''
        Generates the longest possible cycle in a eulerian graph from the start node
        Graph must be eularian
        '''
        path = [start]
        current = start
        #Uses a repeat until structure
        while True:
            #If there are loops at a node, keep traversing loops
            while current in adj[current]:
                path.append(current)
                adj[current].remove(current)
                adj[current].remove(current)
            #Once no loops, stores current node
            prev = current
            current = None
            #Find the next node
            #Tries to find a node distinct from start and previous node
            for node in adj[prev]:
                if node != start and node != prev:
                    current = node
                    break
            #If did not find such node, cycle is done. Finish it with the start node
            if current == None: 
                current = start
            # add the new node to cycle, remove the edge between prev and current
            path.append(current)
            adj[prev].remove(current)
            adj[current].remove(prev)
            #If cycle finished, we are done
            if current == start:
                break
        return path
    
    def shortestPath(self, src):
        """
        Find the shortest path length between src and all nodes, and the corresponding paths
        Works on directed and undirected graphs
        Returns a disctionary of this format:
        {
        node1 : {
                length : num,
                path : [src, v1, v2, ..., node1]
                },
        node2 : {
                length : num
                path : [src, v1, v2, ..., node2]
                }
        }
        """
        #Keeps vertices with permanent labels and temp labels separate
        recent_vertex = src
        temp_vertices = {node for node in self.nodes}
        temp_vertices.remove(src)
        adj = self.adjacency_dict()
        #If graph not weighted, assigns 1 as weight to all edges
        if not self.weighted:
            for node1 in adj:
                for i, node2 in enumerate(adj[node1]):
                    adj[node1][i] = (node2, 1)
        #Each vertex has a lable
        #label[0] -> distance
        #label[1] -> preceding vertex
        labels = dict()
        #Initialize all labels to infinity, except the source
        for node in self.nodes:
            labels[node] = [math.inf, None]
        labels[src] = [0, None]

        #Repeat until structure
        #Runs until all nodes are assigned a permanent label
        while True:
            #Takes most recent node which got assigned permanent label
            current_vertex = recent_vertex
            #v - vertex, w - weight
            #Goes through every vertex adjacent to current one, updating labels
            for (v, w) in adj[current_vertex]:
                if v in temp_vertices and labels[current_vertex][0] + w < labels[v][0]:
                    labels[v][0] = labels[current_vertex][0] + w
                    labels[v][1] = current_vertex
            #Find the vertex with a temporary label of least weight
            min_weight = math.inf
            min_vertex = None
            for v in temp_vertices:
                if labels[v][0] < min_weight:
                    min_weight = labels[v][0]
                    min_vertex = v
            #If all temp vertices are at infinity, they cant be reached
            #Manually change label to -1 and assign permanent label to all
            if min_weight == math.inf:
                for v in temp_vertices: #n
                    labels[v][0] = -1
                temp_vertices = set()
            #Else, assign permanent label to the vertex of least weight
            else:
                recent_vertex = min_vertex
                temp_vertices.remove(min_vertex)
            if temp_vertices == set():
                break
        #Create an output dictionary
        output = dict()
        for v in self.nodes:
            output[v] = dict()
            output[v]["length"] = labels[v][0]
            #Find the path to each vertex by tracing back its previous vertex
            #using label[vertex][1]
            path = [v]
            current_vertex = v
            while labels[current_vertex][1] != None:
                current_vertex = labels[current_vertex][1]
                path.insert(0, current_vertex)
            if labels[v][0] != -1:
                output[v]["path"] = path
            else:
                output[v]["path"] = None
        return output
    
    def shortest_distances_all_pairs(self):
        """
        Works on a matrix representation of the graph
        Returns a 2d list where value of m[i][j] is shortest dist from vi to vj
        Assumes that self.nodes is a list of nodes from 0 to n.
        """
        adj = self.adjacency_matrix()
        d = [[0 for node in self.nodes] for node in self.nodes]
        #This makes use of the floyd warshall algorithm
        for i in self.nodes:
            for j in self.nodes:
                if i != j:
                    if adj[i][j] != 0:
                        d[i][j] = adj[i][j]
                    else:
                        d[i][j] = math.inf
        for k in self.nodes:
            for i in self.nodes:
                for j in self.nodes:
                    d[i][j] = min(d[i][j], d[i][k] + d[k][j])
        return d

    def chinese_postman(self):
        """
        Problem: find the shortest walk that covers every edge at least once
        This is done by duplicating edges in the graph such that a Eulerian circuit exists
        This finds such edges such that the obtained pseudograph has the minimum possible Eulerian circuit
        For a possibly weighted, undirected, connected graph
        Returns a tuple (g, duplicated_edges)
        g -> a Eulerian pseudogaph of minimum weight, obtained by duplicating edges of original graph
        duplicated_edges -> a list of edges that were duplicated to achieve the result
        """
        #If graph is eulerian, we are done
        if self.find_eulerian_cycle() != None:
            return (self, [])
        g_copy = copy.deepcopy(self)
        adj_dict = self.adjacency_dict()
        #Obtains a list of all odd nodes
        odd_nodes = []
        for node in adj_dict:
            if len(adj_dict[node]) % 2 == 1:
                odd_nodes.append(node)
        #Splits the nodes into pairs, and finds every possible partition of such pairings
        node_permutations = list(permutations(odd_nodes))
        seen_partitions = set()
        for perm in node_permutations:
            pairs = []
            #For each permutation, pairs two nodes next to each other (in the list)
            for i in range(0, len(perm), 2):
                pair = sorted([perm[i], perm[i + 1]])
                #sorting is to remove duplicate pairs - (0, 1) and (1, 0) are the same
                pairs.append(tuple(pair))
            #sorts to avoid duplicate partitions. A set is used for the same purpose
            pairs = tuple(sorted(pairs))
            if pairs not in seen_partitions:
                seen_partitions.add(pairs)
        #Find a partition in which the sum of distances between all the pairs are minimal
        min_weights = self.shortest_distances_all_pairs()
        min_weight = math.inf
        min_partition = None
        for partition in seen_partitions:
            weight = 0
            for pair in partition:
                weight += min_weights[pair[0]][pair[1]]
            if weight < min_weight:
                min_weight = weight
                min_partition = partition
        #Find shortest path between each pair in the minimal partition
        #Duplicates the edges in such path
        adj_mat = self.adjacency_matrix()
        duplicated_edges = []
        for pair in partition:
            output = self.shortestPath(pair[0])
            path = output[pair[1]]['path']
            for i in range(len(path) - 1):
                if not self.weighted:
                    new_edge = [path[i], path[i + 1]]
                else:
                    weight = adj_mat[path[i]][path[i + 1]]
                    new_edge = [path[i], path[i + 1], weight]
                duplicated_edges.append(new_edge)
        #Adds the duplicated adges to the new pseudograph
        g_copy.edges.extend(duplicated_edges)
        return (g_copy, duplicated_edges)
    
    def total_graph_weight(self):
        """
        Returns the total weight of all edges in a graph
        If graph is not weighted, returns number of edges
        """
        total = 0
        for edge in self.edges:
            if self.weighted:
                total += edge[2]
            else:
                total += 1
        return total
    




        
        



