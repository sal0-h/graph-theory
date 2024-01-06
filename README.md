# Graph Algorithms Library

A Python library for working with graph structures and implementing various graph algorithms. The library provides a `Graph` class that allows users to create, manipulate, and analyze both directed and undirected graphs. Key features include:

- Representation of graphs using adjacency lists and matrices.
- Visualization of graphs using the `pyvis` library.
- Algorithms for finding Eulerian cycles, shortest paths, and solving the Chinese Postman problem.
- Support for weighted and unweighted graphs as well as directed and undirected graphs.

It also provides an `ActivityNetwork` class that takes in a dependence table as a parameter and creates a `Graph` subclass, `ActivityNetwork`, which is a representation of the project as an Activity-On-Arc network. 

Explore the power of graph algorithms with this easy-to-use Python library!

# How to use

The `Graph` and `ActivityNetwork` classes are inside the `graph.py` file in the graph folder. The other files show examples of how methods of the classes can be used.

## To instantiate Graph:
`g = Graph(nodes : list, edges : list, directed=False, weighted=False)`

* `nodes` is a list of intergers of strings that represent the graph nodes
* `edges` is a list of items of following format: 
* * `[[node1, node2, weight1], [node2, node3, weight2]]` if graph is weighted. This edge list defines an edge between `node1` and `node2` with `weight1`, and an edge between `node2` and `node3` with `weight2`. If the graph is directed, then this defines an arc, which only goes from one node to another and not the other way. An unweighted graph will omit the `weight1` and `weight2`

## Adjacency dictionary
`adj_dict = g.adjacency_dict()`

* Returns an adjacency dictionary for the graph

## Adjacency matrix
`adj_mat = g.adjacency_matrix()`

* Returns an adjacency matrix for the graph
* Only works for graph where nodes are ordered from 0 to n - 1 where n is the number of nodes

## Graph visual representation
`g.show(output_filename : str)`

* Takes in a .html filename as parameter
* Creates an html file with given filename in working directory showing the graph
* Will try to do something weird and open a random tab in the browser, Ignore

## Finding a eulerian cycle in a graph
`cycle = g.find_eulerian_cycle()`

* If a eulerian cycle exists in the graph, returns a list of the nodes of such cycle
* Othwerwise, returns `None`

## Finding shortest path from a node
`paths = g.shortest_path(src)`

* From the given source node `src` finds the shortest paths to all other nodes in the graph
* Used Djikstra's algorithm
* Returns a dictionary of this format:
```
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
```

## Finding a shortest distance matrix between all nodes
`distance_matrix = g.shortest_distances_all_pairs()`

* Returns a 2d list where value of `distance_matrix[i][j]` is shortest dist from node i to node j
* Uses the Floyd-Warshall algorithm
* Only works for graph where nodes are ordered from 0 to n - 1 where n is the number of nodes

## Chinese postman (Route inspection algorithm)
`new_g = g.chinese_postman()`

* Returns a tuple `(new_g, duplicated_edges)`
* `new_g` -> a Eulerian pseudogaph of minimum weight, obtained by duplicating edges of original graph
* `duplicated_edges` -> a list of edges that were duplicated to achieve the result
* By running `cycle = new_g.find_eulerian_cycle()`, you can find the shortest possible inspection route from the graph `g`

## Total graph weight
`weight = g.total_graph_weight`

* Returns the sum of all weights of the edges of the graph

## Minimum spanning tree algorithms
Coming soon...

## To instantiate an activity network
`net = ActivityNetwork(dependence_table : dict)`

* `dependence_table` is a dictionary of the following format:
```
{
activity : [list_of_precursors, weight],
...
}
```
For example:
```
{
"A" : [[], 10],
"B" : [[], 9],
"C" : [["A", "B"], 3],
"D" : [["B"], 5],
"E" : [["B"], 6],
"F" : [["C"], 8],
"G" : [["C", "D"], 10],
"H" : [["E"], 10],
}
```
* Returns an ActivityNetwork object, which is an instance of a graph
* You can show the model of the activity network using the aforementioned `.show(output_filename)` method

## To create an event dictionary
`event_dict = net.event_dict()`

* Returns a dictionary with all the nodes with their associated precursor and follower activity sets
* Contains all the necessary dummies
* The dictionary is of the following format:
`{node : [{Precursor set}, {Follower set}]}`

## Calculate the early and late event times
`early_late_times = net.calculate_early_late_event_times()`

* Performs a forward and backward pass to calculate the early and late times for each event (node)
* Returns a dictionary of the following format:
`{node : [early_event_times, late_event_time], ...}`

## Find the float of an activity
`num = net.float_of_activity(activity)`

* Returns the float of an activity
* Total float of an activity is the amount of time that its start may be delayed without affecting the duration of the project

## Find the total duration of the project
`num = net.total_project_duration()`

* Returns the total duration of the project

# What I learned

* Representing graphs in python
* Using the `pyvis` library
* Writing graph algorithms