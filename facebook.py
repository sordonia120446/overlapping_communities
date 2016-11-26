from igraph import *
from nectar import *
# from custom_nectar import *
import random
import os
import time
"""
Runs on python3.5.  Requires igraph, cairo, and a CPU. 

Create social network graph based on Stanford's Facebook data. 
"""

# ---------------------------------------------------------------------------------------
# Creating the graph G<V,E>

# Reading in the input file 
# path = os.path.abspath("references/facebook/facebook_combined.txt")
path = os.path.abspath("references/facebook/weighted_graph.txt")

file = open(path, 'r')
my_graph = Graph.Read_Ncol(file, names=True, weights='if_present', directed = False)
my_graph = my_graph.simplify(multiple=True, loops=True, combine_edges=max) # remove duplicate edges

# Coming up with random ages, gender, and formal/informal relationships
# gender_types = ["m", "f"]
# is_formal_types = [True, False]
# for vertex in my_graph.vs:
# 	vertex["age"] = round(random.uniform(1, 65))
# 	vertex["gender"] = gender_types[round(random.uniform(0,1))]
# 	vertex["is_formal"] = is_formal_types[round(random.uniform(0,1))]

# Close input file
file.close()

# ---------------------------------------------------------------------------------------
# Running the entire NECTAR algorithm here!  

# Initial input parameters
# original_graph = my_graph.copy()
beta = 10000000
# plot_Kamada_Kawai(my_graph)

#Testing one vertex with nectar
# my_vertex_id = 0
# output = nectar(my_graph, beta, my_vertex_id)
# community_list = output[0]
# vertex = my_graph.vs[my_vertex_id]
# print( "\nFor vertex {} , it is part of the following communities".format(vertex["name"]) )
# for community in community_list:
# 	cluster_members = community.vs["name"]
# 	print('\n')
# 	print(cluster_members)
	# plot_Kamada_Kawai(community)

# # Testing the entire outer_nectar algorithm.  
start_time = time.time()
communities_per_node_from_nectar = outer_nectar(my_graph, beta)
print("\nHere's what we get from the nectar algorithm")
cntr = 0
for community_list in communities_per_node_from_nectar:
	# print(community_list)
	vertex = my_graph.vs[cntr]
	print( "\nFor vertex {} , it is part of the following communities".format(vertex["name"]) )
	for cluster in community_list:
		cluster_members = cluster.vs["name"]
		# print(   "It is part of this community".format(cluster_members)   )
		print(cluster_members)
	cntr += 1

end_time = time.time()
time_delta = end_time - start_time
print("\nDone")
print("The time required to run is {} seconds".format(time_delta))




















