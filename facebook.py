from igraph import *
from nectar import *
import random
import os
"""
Runs on python3.5.  Requires igraph, cairo, and a CPU. 

Create social network graph based on Stanford's Facebook data. 
"""

# ---------------------------------------------------------------------------------------
# Creating the graph G<V,E>

# Reading in the input file 
path = os.path.abspath("references/facebook/facebook_combined.txt")
print(path)
file = open(path, 'r')
my_graph = Graph.Read_Ncol(file, directed = False)
# print(my_graph.vs["name"])

# Coming up with random ages
for vertex in my_graph.vs:
	vertex["age"] = round(random.uniform(1, 65))
	print(vertex["age"])

# my_graph = Graph([(0,1), (0,2), (2,3), (3,4), (4,2), (2,5), (5,0), (6,3), (5,6)])
# my_graph.vs["age"] = [25, 31, 18, 47, 22, 23, 50]
# my_graph.vs["gender"] = ["f", "m", "f", "m", "f", "m", "m"]
# my_graph.es["is_formal"] = [False, False, True, True, True, False, True, False, False]

# Adding weights to these edges.  Weights are determined by age deltas b/w nodes. 
# weights = list();
# for edge in my_graph.es:
# 	source_vertex = my_graph.vs[edge.source]["age"]
# 	target_vertex = my_graph.vs[edge.target]["age"]
# 	weights.append( abs(source_vertex - target_vertex) )
# my_graph.es["weight"] = weights

# ---------------------------------------------------------------------------------------
# Running the entire NECTAR algorithm here!  

# original_graph = my_graph.copy()
# beta = 1

# # my_vertex_id = 4
# # plot_Kamada_Kawai(my_graph)

# # Testing the entire outer_nectar algorithm.  
# communities_per_node_from_nectar = outer_nectar(my_graph, beta)
# print("\nHere's what we get from the nectar algorithm")
# for item in communities_per_node_from_nectar:
# 	print(item)
# 	for cluster in item:
# 		print(cluster.vs["name"])























