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
run(my_graph, beta)

# # Testing the entire outer_nectar algorithm.  
# start_time = time.time()
# communities_per_node_from_nectar = outer_nectar(my_graph, beta)
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


def run(my_graph, beta):
	"""
	Testing the entire outer_nectar algorithm.  
	"""
	start_time = time.time()
	communities_per_node_from_nectar = outer_nectar(my_graph, beta)
	end_time = time.time()
	time_delta = end_time - start_time
	print("\nHere's what we get from the nectar algorithm")
	cntr = 0
	for community_list in communities_per_node_from_nectar:
		# print(community_list)
		vertex = my_graph.vs[cntr]
		print( "\nFor vertex {} , it is part of the following communities".format(vertex["name"]) )
		for cluster in community_list:
			# TODO:  add in modularity aggregation
			cluster_members = cluster.vs["name"]
			# print(   "It is part of this community".format(cluster_members)   )

			print(cluster_members)
		cntr += 1
	print("\nDone")
	print("The time required to run is {} seconds".format(time_delta))

# Print iterations progress
def printProgress (iteration, total, prefix = '', suffix = '', decimals = 1, barLength = 100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        barLength   - Optional  : character length of bar (Int)
    """
    formatStr = "{0:." + str(decimals) + "f}"
    percent = formatStr.format(100 * (iteration / float(total)))
    filledLength = int(round(barLength * iteration / float(total)))
    bar = '█' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percent, '%', suffix)),
    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()

# 
# Sample Usage
# 

from time import sleep

# make a list
# items = list(range(0, 100))
items = list(range(0,len(my_graph.vs)))
i = 0
l = len(items)

# Initial call to print 0% progress
printProgress(i, l, prefix = 'Progress:', suffix = 'Complete', barLength = 50)
for item in items:
	# Do stuff...
	# run(my_graph, beta)
	communities_per_node_from_nectar = outer_nectar(my_graph, beta)
	sleep(0.1)
	# Update Progress Bar
	i += 1
	printProgress(i, l, prefix = 'Progress:', suffix = 'Complete', barLength = 50)

# Sample Output
# Progress: |█████████████████████████████████████████████-----| 90.0% Complete

# my_graph_membership = my_graph.clusters().membership
# print("The modularity is {}".format(my_graph.modularity(my_graph_membership)))

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


# ---------------------------------------------------------------------------------------
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












