from igraph import *
import time
from nectar import *
# from custom_nectar import *
import sys
"""
Runs on python3.5.  Requires igraph, cairo, and a CPU. 
"""

# ---------------------------------------------------------------------------------------
# Create graph of 7 vertices and 9 edges.
my_graph = Graph([(0,1), (0,2), (2,3), (3,4), (4,2), (2,5), (5,0), (6,3), (5,6)])
my_graph.vs["name"] = ["Alice", "Bob", "Claire", "Dennis", "Esther", "Frank", "George"]
my_graph.vs["age"] = [25, 31, 18, 47, 22, 23, 50]
my_graph.vs["gender"] = ["f", "m", "f", "m", "f", "m", "m"]
my_graph.es["is_formal"] = [False, False, True, True, True, False, True, False, False]

# Adding weights to these edges.  Weights are determined by age deltas b/w nodes. 
weights = list();
for edge in my_graph.es:
	source_vertex = my_graph.vs[edge.source]["age"]
	target_vertex = my_graph.vs[edge.target]["age"]
	weights.append( abs(source_vertex - target_vertex) )
my_graph.es["weight"] = weights

# ---------------------------------------------------------------------------------------
# Running the entire NECTAR algorithm here!  

original_graph = my_graph.copy()
beta = 10000000
run(my_graph, beta)

# # my_vertex_id = 4
# plot_Kamada_Kawai(my_graph)

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
# 		# TODO:  add in modularity aggregation
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
items = list(range(0,1))
i = 0
l = len(items)

# Initial call to print 0% progress
printProgress(i, l, prefix = 'Progress:', suffix = 'Complete', barLength = 50)
for item in items:
    # Do stuff...
    # run(my_graph, beta)
    sleep(0.1)
    # Update Progress Bar
    i += 1
    printProgress(i, l, prefix = 'Progress:', suffix = 'Complete', barLength = 50)

# Sample Output
# Progress: |█████████████████████████████████████████████-----| 90.0% Complete




# ---------------------------------------------------------------------------------------
# Modularity deprecated
# my_graph_membership = my_graph.clusters().membership
# print(membership_of_cluster)
# print("The modularity is {}".format(my_graph.modularity(my_graph_membership)))

# For testing individual node Alice
# my_vertex_id = 0 # Alice vertex
# my_vertex = my_graph.vs[my_vertex_id]
# # alice_communities =  nectar(my_graph, beta, my_vertex_id)
# alice_communities = determine_community_set(my_graph, my_vertex)

# for cluster in alice_communities:
# 	print(cluster)
# 	# plot_Kamada_Kawai(cluster)








