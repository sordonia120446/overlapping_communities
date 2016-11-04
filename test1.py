from igraph import *
"""
Runs on python3.5.  Requires igraph, cairo, and a CPU. 
"""

# ---------------------------------------------------------------------------------------

def nectar(graph, vertex_ID):
	# Make new graph without vertex
	modified_graph = graph.copy() 
	vertex = graph.vs[vertex_ID]
	vertex_neighbors_ID = graph.neighbors(vertex, mode="out")
	for index, id in enumerate(vertex_neighbors_ID):
		if (id > vertex_ID):
			vertex_neighbors_ID[index] -=1
	modified_graph.delete_vertices(vertex_ID)


	# TODO
	# Compute Sv, the set of communities each containing at least one instance of v's neighbors
	louvian_output = modified_graph.community_multilevel(weights=modified_graph.es["weight"])
	print("Here's some graph cluster info")
	# print(louvian_output)
	modified_clusters = louvian_output.subgraphs()
	vertex_neighbors_clusters = []
	for cluster in modified_clusters:
		print(cluster.vs)
		if ( vertex_neighbors_ID in cluster.vs):
			vertex_neighbors_clusters.append(cluster)


	# TODO
	# Compute the "gain" when adding v to each neighboring community. 


	# TODO
	# Add v to the community maximizing gain

	# TODO 
	return modified_graph


# ---------------------------------------------------------------------------------------
# Creating the graph G<V,E>

# g = Graph.GRG(10, 0.2)
# #summary(g)
# print(g)

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

# calculate dendrogram
my_dendrogram = my_graph.community_edge_betweenness(weights = my_graph.es["weight"])
# convert it into a flat clustering
my_clusters = my_dendrogram.as_clustering()
# get the membership vector
my_membership = my_clusters.membership

modie = my_graph.modularity(my_membership)
optModie = my_graph.community_optimal_modularity(my_graph.es["weight"])
# print("Here's some graph cluster info")
# print(my_membership)
# print(modie)
# print(optModie)
# print(my_graph.es["weight"])


# Finding neighbors
# print("Let's find all neighbors to Alice")
# neis = my_graph.neighbors("Alice", mode="out")
# print(my_graph.vs[neis]["name"])
#print(my_graph.incident("Alice", mode="out")) # returns all incidnet edges to Alice


# ---------------------------------------------------------------------------------------

my_vertex = 0
my_graph = nectar(my_graph, my_vertex)

# ---------------------------------------------------------------------------------------

louvian_output = my_graph.community_multilevel(weights=my_graph.es["weight"])

# print("Here's some graph cluster info")
# print(louvian_output)
# print(my_graph.es["weight"])

# ---------------------------------------------------------------------------------------
# Plotting stuff

# Kamada-Kawai plotting
layout = my_graph.layout("kk")
color_dict = {"m": "blue", "f": "pink"}
visual_style = {}
visual_style["vertex_size"] = 20
visual_style["vertex_color"] = [color_dict[gender] for gender in my_graph.vs["gender"]]
visual_style["vertex_label"] = my_graph.vs["name"]
visual_style["edge_label"] = my_graph.es["weight"]
#visual_style["edge_width"] = my_graph.es["weight"]
visual_style["layout"] = layout
visual_style["bbox"] = (600, 600)
visual_style["margin"] = 20


plot(my_graph, **visual_style)














