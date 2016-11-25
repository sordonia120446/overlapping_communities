from igraph import *
from nectar import *
# from custom_nectar import *
import random
import os
"""
Runs on python3.5.  Requires igraph, cairo, and a CPU. 

Create social network graph based on Stanford's Facebook data. 
"""

# ---------------------------------------------------------------------------------------
# Creating the graph G<V,E>

# Reading in the input file 
path = os.path.abspath("references/power_grid/unweighted_data.txt")

file = open(path, 'r')
my_graph = Graph.Read_Ncol(file, names=True, weights='if_present', directed = False)
my_graph = my_graph.simplify(multiple=True, loops=True, combine_edges=max) # remove duplicate edges
# my_graph = Graph.Read_Ncol(file, weights='if_present', directed = False)

# Close input file
file.close()

# ---------------------------------------------------------------------------------------
# Running the entire NECTAR algorithm here!  

# Initial input parameters
original_graph = my_graph.copy()
beta = 10000000
# plot(my_graph)

# Testing one vertex with nectar
# my_vertex_id = 0
# output = nectar(my_graph, beta, my_vertex_id)
# community_list = output[0]
# vertex = my_graph.vs[my_vertex_id]
# print( "\nFor vertex {} , it is part of the following communities".format(vertex["name"]) )
# for community in community_list:
# 	cluster_members = community.vs["name"]
# 	print('\n')
# 	print(cluster_members)

# Testing the entire outer_nectar algorithm.  
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

print("\nDone")

# ---------------------------------------------------------------------------------------
# Troubleshooting community detection of vertex v

# community_list = determine_community_set(my_graph, vertex)
# clique_list = my_graph.maximal_cliques()
# print(len(clique_list))

# for clique in clique_list:
# 	if (307 in clique):
# 		vertices = list(clique)
# 		community_list.append(my_graph.subgraph(vertices))

# for community in community_list:
# 	cluster_members = community.vs["name"]
# 	print('\n')
# 	print(cluster_members)
# 	plot(community)
















