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

    def show(self, output_filename, label_function = None):
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
                if label_function == None:
                    label = str(self.edges[i][2])
                else:
                    label = label_function(self.edges[i][2], self.edges[i][3])
                g.add_edge(edge_list[i][0], edge_list[i][1], label = label)
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
    
class ActivityNetwork(Graph):

    def __init__(self, dependence_table : dict):
        #Sample dependence table:
        '''
        {
        "A" : [[], 10],
        "B" : [[], 6],
        "C" : [["A"], 7],
        "D" : [["A"], 9],
        "E" : [["B"], 10],
        "F" : [["C", "E"], 3],
        "G" : [["D", "F"], 6]
        }
        '''
        self.dependence_table = dependence_table
        self.node_dict = self.event_dict()
        nodes = list(self.node_dict.keys())
        edges = []
        #Based on the node dictionary with the associated precursor and follower sets, creates edges
        #Checking every node and seeing what activities come into it
        for in_node in nodes:
            #Check every incoming activity for node
            for incoming_activity in self.node_dict[in_node][0]:
                #For each activity, checks all other nodes and finds their outgoing activities
                for out_node in nodes:
                    outgoing_activities = self.node_dict[out_node][1]
                    #if it finds an outgoing activity in any other nodes that match the incoming activity in current node
                    if out_node != in_node and incoming_activity in outgoing_activities:
                        if incoming_activity not in dependence_table:
                            edges.append([out_node, in_node, 0, ""])    
                        else:
                            edges.append([out_node, in_node, dependence_table[incoming_activity][1], incoming_activity])
                        break
        #initiate a graph object using the nodes and edges constructed
        super().__init__(nodes, edges, directed=True, weighted=True)
    
    def event_dict(self):
        '''
        #Makes a dictionary of nodes with corresponding precursor and follower activity sets
        '''
        activities = list(self.dependence_table.keys())
        left_activities = set(activities)
        initial_node_dict = dict()
        current_node = 0
        for activity in activities:
            dependence = tuple(sorted(self.dependence_table[activity][0]))
            for act in dependence:
                if act in left_activities: 
                    left_activities.remove(act)
            if dependence in initial_node_dict:
                initial_node_dict[dependence][0].append(activity)
            else:
                initial_node_dict[dependence] = [[activity], current_node]
                current_node += 1
        left_activities = tuple(sorted(left_activities))
        initial_node_dict[left_activities] = [[], current_node]
        node_dict = dict()
        for node in initial_node_dict:
            node_dict[initial_node_dict[node][1]] = [set(node), set(initial_node_dict[node][0])]
        self.__add_dummies(node_dict)
        print(node_dict)
        return node_dict
    
    def __add_dummies(self, node_dict):
        '''
        Using K. Neumann algorithm to add dummies to the event dict
        Neumann, K. (1999). A Heuristic Procedure for Constructing an Activity-on-Arc Project Network. In: Gaul, W., Schader, M. (eds) Mathematische Methoden der Wirtschaftswissenschaften. Physica, Heidelberg. https://doi.org/10.1007/978-3-662-12433-8_30
        The premise is to check for 3 conditions and keep adding dummies until they are satisfied
        '''
        dummy_counter = 0
        dummies_left = True
        nodes = list(node_dict.keys())
        while dummies_left:
            #Checking if if theres a precursor set which is a subset of another
            #(Condition 1)
            #If so, find maximum such set
            maximum_set_length = -math.inf
            maximum_nodes = None
            for node1 in node_dict:
                for node2 in node_dict:
                    p1, p2 = node_dict[node1][0], node_dict[node2][0]
                    if node1 != node2 and p1 != set() and p1.issubset(p2) and \
                        len(p1) > maximum_set_length:
                        maximum_set_length = len(p1)
                        maximum_nodes = (node1, node2)
            if maximum_nodes != None:
                node1, node2 = maximum_nodes
                p1, p2 = node_dict[node1][0], node_dict[node2][0]
                for activity in copy.copy(p2):
                    if activity in p1:
                        p2.remove(activity)
                        p2.add(str(dummy_counter))
                node_dict[node1][1].add(str(dummy_counter))
                dummy_counter += 1
            else:
                # Check if there are two precursors such that their intersection is not empty
                # (condition 2)
                # if so, find largest such intersection
                maximum_intersection_length = 0
                maximum_nodes = None
                for node1 in node_dict:
                    for node2 in node_dict:
                        p1, p2 = node_dict[node1][0], node_dict[node2][0]
                        intersection = p1 & p2
                        if node1 != node2 and p1 != p2 and len(intersection) > maximum_intersection_length:
                            maximum_intersection_length = len(intersection)
                            maximum_nodes = (node1, node2)
                if maximum_nodes != None:
                    node1, node2 = maximum_nodes
                    p1, p2 = node_dict[node1][0], node_dict[node2][0]
                    p3 = p1 & p2
                    new_node = nodes[-1] + 1
                    for activity in copy.copy(p1):
                        if activity in p3:
                            p1.remove(activity)
                            p1.add(str(dummy_counter))
                    for activity in copy.copy(p2):
                        if activity in p3:
                            p2.remove(activity)
                            p2.add(str(dummy_counter + 1))
                    f3 = {str(dummy_counter), str(dummy_counter + 1)}
                    node_dict[new_node] = [p3, f3]
                    dummy_counter += 2
                else:
                    # Check if there is precursor and follower which have more than 1 common activity
                    # (condition 3)
                    nodes_found = None
                    for node1 in node_dict:
                        for node2 in node_dict:
                            p1, f2 = node_dict[node1][0], node_dict[node2][1]
                            intersection = p1 & f2
                            if node1 != node2 and len(intersection) > 1:
                                nodes_found = (node1, node2)
                    if nodes_found != None:
                        node1, node2 = nodes_found
                        p1, f2 = node_dict[node1][0], node_dict[node2][1]
                        intersection = p1 & p2
                        r = len(intersection)
                        for i, activity in enumerate(intersection):
                            if i < r - 1:
                                p1.remove(activity)
                                p1.add(str(dummy_counter + i))
                                new_node = nodes[-1] + 1
                                p3 = {activity}
                                f3 = {str(dummy_counter + i)}
                                node_dict[new_node] = [p3, f3]
                        dummy_counter += r - 1
                    #if all 3 conditions are satisfied, no more dummies needed
                    else: 
                        dummies_left = False

    def calculate_early_late_event_times(self):
        '''
        Returns a dictionary with early and late event times for each node in this format:
        {node : [early_event_times, late_event_time], ...}
        '''
        times = {node : [-math.inf, math.inf] for node in self.nodes}
        self.__forward_pass(times)
        self.__backward_pass(times)
        return times
    
    def __forward_pass(self, times):
        '''
        Performs a breadth-first algorithm on network to calculate the early event times
        '''
        source = 0
        queue = [source]
        times[source][0] = 0
        adj = self.adjacency_dict()
        while queue != []:
            current_node = queue.pop(0)
            for (node2, weight, activity) in adj[current_node]:
                times[node2][0] = max(times[current_node][0] + weight, times[node2][0])
                queue.append(node2)

    def __backward_pass(self, times):
        '''
        Performs a breadth-first algorithm on a network with inversed arcs
        to calculate the late event times
        '''
        source = self.nodes[-1]
        queue = [source]
        times[source][1] = times[source][0]
        adj = self.reverse_adjacency_dict()
        while queue != []:
            current_node = queue.pop(0)
            for (node2, weight, activity) in adj[current_node]:
                times[node2][1] = min(times[current_node][1] - weight, times[node2][1])
                queue.append(node2)

    def float_of_activity(self, activity):
        '''
        Returns the float of an activity
        Total float of an activity is the amount of time that its start may be delayed 
        without affecting the duration of the project
        '''
        times = self.calculate_early_late_event_times()
        float_edge = None
        for edge in self.edges:
            if edge[3] == activity:
                float_edge = edge
        if float_edge == None:
            return None
        else:
            node1, node2, weight, activity = float_edge[0], float_edge[1], float_edge[2], float_edge[3] 
            return times[node2][1] - times[node1][0] - weight
        
    def total_project_duration(self):
        """
        Returns the total duration of the project
        """
        times = self.calculate_early_late_event_times()
        return times[self.nodes[-1]][0]

    def adjacency_dict(self):
        '''
        Returns an adjacency dictionary for an activity network
        '''
        adj_dict = dict()
        for node in self.nodes:
            adj_dict[node] = []
        for edge in self.edges:
            node1, node2, weight, activity = edge[0], edge[1], edge[2], edge[3]
            adj_dict[node1].append((node2, weight, activity))
        return adj_dict
    
    def reverse_adjacency_dict(self):
        '''
        Returns an adjacency dictionary for an activity network
        But instead of each node having the nodes part of its outdegree
        It has the nodes that are part of its indegree
        '''
        adj_dict = dict()
        for node in self.nodes:
            adj_dict[node] = []
        for edge in self.edges:
            node1, node2, weight, activity = edge[0], edge[1], edge[2], edge[3]
            adj_dict[node2].append((node1, weight, activity))
        return adj_dict
    
    def show(self, output_filename):
        '''
        Creates a .html file with output_filename in working directory containing a representation of the network
        '''
        def label_function(weight, name):
            return f"{name}({weight})"
        return super().show(output_filename, label_function)