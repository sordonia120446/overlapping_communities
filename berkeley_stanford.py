from igraph import *
from nectar import *
# from custom_nectar import *
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

# Reading in the input file 
path = os.path.abspath("references/Berkeley_and_Stanford/web_BerkStan.txt")

file = open(path, 'r')
my_graph = Graph.Read_Ncol(file, names=True, weights='if_present', directed = False)
my_graph = my_graph.simplify(multiple=True, loops=True, combine_edges=max) # remove duplicate edges
# my_graph = Graph.Read_Ncol(file, weights='if_present', directed = False)

# Close input file
file.close()

print(len(my_graph.vs))
print(len(my_graph.es))

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
original_graph = my_graph.copy()
beta = 10000000
# plot(my_graph)
run(my_graph, beta)























