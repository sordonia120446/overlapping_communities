from igraph import *
# from nectar import *
from heuristic_nectar import *
"""
Runs on python3.5.  Requires igraph, cairo, and a CPU. 
"""

# ---------------------------------------------------------------------------------------
# Creating the graph G<V,E>

# Generate a famous graph
# my_graph = Famous("Tutte")
# num_of_vertices = 50
# fw_prob = 0.8
# my_graph = Forest_Fire(n, fw_prob, bw_factor=0.1, ambs=2, directed=False)

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
beta = 1

# my_vertex_id = 4
plot_Kamada_Kawai(my_graph)

# Testing the entire outer_nectar algorithm.  
communities_per_node_from_nectar = outer_nectar(my_graph, beta)
print("\nHere's what we get from the nectar algorithm")
for community_list in communities_per_node_from_nectar:
	# print(community_list)
	for cluster in community_list:
		print(cluster.vs["name"])

# For testing individual node Alice
# my_vertex_id = 0 # Alice vertex
# my_vertex = my_graph.vs[my_vertex_id]
# alice_communities =  nectar(my_graph, beta, my_vertex_id)

# for cluster in alice_communities:
# 	print(cluster)
# 	plot_Kamada_Kawai(cluster)

















