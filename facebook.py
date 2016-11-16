from igraph import *
# from nectar import *
from heuristic_nectar import *
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
file = open(path, 'r')
my_graph = Graph.Read_Ncol(file, directed = False)

# Coming up with random ages, gender, and formal/informal relationships
gender_types = ["m", "f"]
is_formal_types = [True, False]
for vertex in my_graph.vs:
	vertex["age"] = round(random.uniform(1, 65))
	vertex["gender"] = gender_types[round(random.uniform(0,1))]
	vertex["is_formal"] = is_formal_types[round(random.uniform(0,1))]

# Adding weights to these edges.  Weights are determined by age deltas b/w nodes. 
weights = list();
for edge in my_graph.es:
	source_vertex = my_graph.vs[edge.source]["age"]
	target_vertex = my_graph.vs[edge.target]["age"]
	weights.append( abs(source_vertex - target_vertex) )
my_graph.es["weight"] = weights

# CLose file
file.close()

# ---------------------------------------------------------------------------------------
# Running the entire NECTAR algorithm here!  

my_vertex_id = 1337
original_graph = my_graph.copy()
beta = 1
# plot_Kamada_Kawai(my_graph)
output = nectar(my_graph, beta, my_vertex_id)
community_list = output[0]
# for community in community_list:
# 	for node in community.vs:
# 		print(node["name"])
# 	plot_Kamada_Kawai(community)

# # Testing the entire outer_nectar algorithm.  
# communities_per_node_from_nectar = outer_nectar(my_graph, beta)
# print("\nHere's what we get from the nectar algorithm")
# for item in communities_per_node_from_nectar:
# 	print(item)
# 	for cluster in item:
# 		print(cluster.vs["name"])























