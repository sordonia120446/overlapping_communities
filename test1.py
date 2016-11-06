from igraph import *
"""
Runs on python3.5.  Requires igraph, cairo, and a CPU. 
"""

# ---------------------------------------------------------------------------------------

def plot_Kamada_Kawai(graph_to_plot):
	# Kamada-Kawai plotting
	layout = graph_to_plot.layout("kk")
	color_dict = {"m": "blue", "f": "pink"}
	visual_style = {}
	visual_style["vertex_size"] = 20
	visual_style["vertex_color"] = [color_dict[gender] for gender in graph_to_plot.vs["gender"]]
	visual_style["vertex_label"] = graph_to_plot.vs["name"]
	visual_style["edge_label"] = graph_to_plot.es["weight"]
	#visual_style["edge_width"] = graph_to_plot.es["weight"]
	visual_style["layout"] = layout
	visual_style["bbox"] = (600, 600)
	visual_style["margin"] = 20
	plot(graph_to_plot, **visual_style)

# ---------------------------------------------------------------------------------------

def nectar(graph, vertex_ID):
	# Make new graph without vertex
	modified_graph = graph.copy() 
	vertex = graph.vs[vertex_ID]
	vertex_has_these_edges = []
	vertex_neighbors = []
	vertex_neighbors_ID = graph.neighbors(vertex, mode="out")
	for neighbor_index in graph.neighbors(vertex, mode="out"):
		"""
		Adds all neighbors of vertex
		"""
		vertex_neighbors.append(graph.vs[neighbor_index])
	for index, id in enumerate(vertex_neighbors_ID):
		"""
		Adds all incident edges to vertex into 	vertex_has_these_edges & adjusts indices of vertex_neighbors_id. 
		"""
		vertex_has_these_edges.append( graph.es[graph.get_eid(vertex, graph.vs[id])] )
		if (id > vertex_ID):
			vertex_neighbors_ID[index] -=1 
	modified_graph.delete_vertices(vertex_ID)
	# vertex_neighbors_names = modified_graph.vs[vertex_neighbors_ID]
	print("This is our vertex")
	print(vertex)
	print("And its incident edges are")
	for edge in vertex_has_these_edges:
		print(edge)


	# Compute Sv, the set of communities each containing at least one instance of v's neighbors
	# Sv --> vertex_neighbors_clusters
	louvian_output = modified_graph.community_multilevel(weights=modified_graph.es["weight"]) # returns a list of VertexClusters
	print("\nHere's some graph cluster info")
	print("The entire graph has modularity")
	print(louvian_output.modularity)
	print("The clusters are")
	print(louvian_output)
	modified_clusters = louvian_output.subgraphs() # breaks up the louvian output into the individual sub-graphs (aka, the clusters)
	cluster_membership = louvian_output.membership # an array of all vertices' cluster_IDs; corresponds to pos' in modified_graph
	vertex_neighbors_clusters = [] # keeps track of the cluster ID's that contain at least one instance of v's neighbors
	for ind, node in enumerate(cluster_membership):
		if (ind in vertex_neighbors_ID):
			vertex_neighbors_clusters.append(node)
	# print(vertex_neighbors_clusters)


	# TODO:  Finish compute_gain
	# Compute the "gain" when adding v to each neighboring community. 
	# Iterate through vertex_neighbors_clusters to do so. 
	# Higher modularity --> stronger community structure. Values > 0.3 indicate "strong" community. 
	# 1) modularity for each cluster
	# 2) create a tmp cluster
	# 3) add in vertex into the cluster
	# 4) recompute modularity for the modified cluster

	gain_exp = compute_gain(modified_clusters[1], cluster_membership, vertex, 
		vertex_has_these_edges, vertex_neighbors, graph)
	print("\nmodularity stuff")
	print(gain_exp)


	# TODO
	# Add v to the community maximizing gain

	# TODO 
	# 6.	Check if this “new” community set Cv’ is equal to the original 
	# one found in Step 1.  If so, increment the stable node counter by one 
	# (initialized to zero upon start of the larger algorithm).  
	return modified_graph

def compute_gain(cluster, cluster_membership, vertex, incident_edges, vertex_neighbors, original_graph):
	# TODO: finish!
	initial_modularity = cluster.modularity(cluster_membership, weights=cluster.es["weight"]) 
	final_modularity = 0
	gain = final_modularity - initial_modularity
	# plot_Kamada_Kawai(cluster)
	return gain

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

# TODO
# Eventually want to do this for all vertices.  
my_vertex = 0 # Alice vertex
my_graph = nectar(my_graph, my_vertex)

# ---------------------------------------------------------------------------------------
# Plotting stuff



# plot_Kamada_Kawai(my_graph)

# # Kamada-Kawai plotting
# layout = my_graph.layout("kk")
# color_dict = {"m": "blue", "f": "pink"}
# visual_style = {}
# visual_style["vertex_size"] = 20
# visual_style["vertex_color"] = [color_dict[gender] for gender in my_graph.vs["gender"]]
# visual_style["vertex_label"] = my_graph.vs["name"]
# visual_style["edge_label"] = my_graph.es["weight"]
# #visual_style["edge_width"] = my_graph.es["weight"]
# visual_style["layout"] = layout
# visual_style["bbox"] = (600, 600)
# visual_style["margin"] = 20


# plot(my_graph, **visual_style)














