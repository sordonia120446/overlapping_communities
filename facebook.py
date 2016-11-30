from igraph import *
# from nectar import *
from custom_nectar import *
import random
import os
import time
import sys
"""
Runs on python3.5.  Requires igraph, cairo, and a CPU. 

Create social network graph based on Stanford's Facebook data. 
"""

# ---------------------------------------------------------------------------------------
# Creating the graph G<V,E>

# Reading in the input files
# path = os.path.abspath("references/facebook/facebook_combined.txt")
path_edge_list = os.path.abspath("references/facebook/weighted_graph.txt")
path_vertex_attr = os.path.abspath("references/facebook/vertex_attr_file.txt")
path_edge_attr = os.path.abspath("references/facebook/edge_attr_file.txt")

weighted_graph_file = open(path_edge_list, 'r')
my_graph = Graph.Read_Ncol(weighted_graph_file, names=True, weights='if_present', directed = False)
my_graph = my_graph.simplify(multiple=True, loops=True, combine_edges=max) # remove duplicate edges

# Adding the vertex and edge attributes
# print("Adding the vertex attributes")
# with open(path_vertex_attr, 'r') as vertex_attr_file:
# 	vertex_attr_data = vertex_attr_file.readlines()
# 	for row in vertex_attr_data:
# 		vertex_attr_all = row.split()
# 		my_graph.vs["age"] = vertex_attr_all[0]
# 		my_graph.vs["gender"] = vertex_attr_all[1]

# print("Adding the edge attributes")
# with open(path_edge_attr, 'r') as edge_attr_file:
# 	edge_attr_data = edge_attr_file.readlines()
# 	for row in edge_attr_data:
# 		# edge_attr_all = row.split()
# 		my_graph.es["is_formal"] = row
# 		# my_graph.es["is_formal"] = edge_attr_all[0]

# Coming up with random ages, gender, and formal/informal relationships
# gender_types = ["m", "f"]
# is_formal_types = [True, False]
# for vertex in my_graph.vs:
# 	vertex["age"] = round(random.uniform(1, 65))
# 	vertex["gender"] = gender_types[round(random.uniform(0,1))]
# 	vertex["is_formal"] = is_formal_types[round(random.uniform(0,1))]

# Close input files
weighted_graph_file.close()
# vertex_attr_file.close()
# edge_attr_file.close()

# ---------------------------------------------------------------------------------------
# Running the entire NECTAR algorithm here!  

def run(my_graph, beta):
	"""
	Testing the entire outer_nectar algorithm.  
	"""
	start_time = time.time()
	communities_per_node_from_nectar, modularities_per_node = outer_nectar(my_graph, beta)
	end_time = time.time()
	time_delta = end_time - start_time
	print("\nHere's what we get from the nectar algorithm")
	for ind, community_list in enumerate(communities_per_node_from_nectar):
		# print(community_list)
		vertex = my_graph.vs[ind]
		print( "\nFor vertex {} , it is originally of the community".format(vertex["name"]) )
		for cntr, cluster in enumerate(community_list):
			# TODO:  add in modularity aggregation
			cluster_members = cluster.vs["name"]
			if (cntr == 0):
				print("It is ORIGINALLY part of this community:  {}".format(cluster_members))
			elif (cntr > 0):
				print("It is ALSO part of this community:  {}".format(cluster_members))
				if ( len(modularities_per_node[ind]) > 0 ):
					print(modularities_per_node[ind])
		# if ( len(modularities_per_node[ind]) > 0 ):
		# 	print(modularities_per_node[ind])
	print("\nDone")
	print("The time required to run is {} seconds".format(time_delta))

# Initial input parameters
# original_graph = my_graph.copy()
beta = 10000000
# plot_Kamada_Kawai(my_graph)
run(my_graph, beta)



# ---------------------------------------------------------------------------------------
# Deprecated


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

# # # Testing the entire outer_nectar algorithm.  
# start_time = time.time()
# communities_per_node_from_nectar, modularities_per_node = outer_nectar(my_graph, beta)
# end_time = time.time()
# time_delta = end_time - start_time
# print("\nHere's what we get from the nectar algorithm")
# cntr = 0
# for community_list in communities_per_node_from_nectar:
# 	# print(community_list)
# 	vertex = my_graph.vs[cntr]
# 	print( "\nFor vertex {} , it is part of the following communities".format(vertex["name"]) )
# 	for cluster in community_list:
# 		cluster_members = cluster.vs["name"]
# 		# print(   "It is part of this community".format(cluster_members)   )
# 		print(cluster_members)
# 	cntr += 1

# print("\nDone")
# print("The time required to run is {} seconds".format(time_delta))




















