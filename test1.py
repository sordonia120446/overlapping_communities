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

def determine_community_set(graph, vertex):
	"""
	Returns a list of graphs in which the input vertex belongs to.  
	"""
	vertex_communities = []
	communities = graph.community_multilevel(weights=graph.es["weight"])
	communities = communities.subgraphs()
	for community in communities:
		# print(community.vs)
		for node in community.vs:
			if (node["name"] == vertex["name"]):
				vertex_communities.append(community)
	return vertex_communities

def nectar(graph, beta, vertex_ID):
	"""
	Here's where the NECTAR magic happens.  See proposal.docx for details.  
	"""
	# 0) Initialize stuff
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

	# 1) Determine Cv, the set of communities the vertex belongs to. 
	vertex_communities = determine_community_set(graph, vertex)
	initial_cardinality_of_vertex_communities = len(vertex_communities)


	# 2) Remove vertex & its incident edges
	modified_graph.delete_vertices(vertex_ID)
	# vertex_neighbors_names = modified_graph.vs[vertex_neighbors_ID]

	print("Info on vertex removed, its neighbors, and the incident edges:") 
	print("This is our vertex")
	print(vertex)
	print("Its neighbors are ")
	for neighbor in vertex_neighbors:
		print(neighbor)
	print("And its incident edges are")
	for edge in vertex_has_these_edges:
		print(edge)


	# 3) Compute Sv, the set of communities each containing at least one instance of v's neighbors
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
	print("The cluster membership is")
	print(cluster_membership)
	for ind, node in enumerate(cluster_membership):
		if ( (ind in vertex_neighbors_ID) and (node not in vertex_neighbors_clusters) ):
			vertex_neighbors_clusters.append(node)


	# 4) Compute the "gain" when adding v to each neighboring community. 
	# Iterate through vertex_neighbors_clusters to do so. 
	# Higher modularity --> stronger community structure. Values > 0.3 indicate "strong" community. 
	print("The clusters of the neighbors are")
	print(vertex_neighbors_clusters)
	all_gains = []
	all_clusters_gained = []
	for ind, tmp in enumerate(vertex_neighbors_clusters):
		print(modified_clusters[ind]) # wrong
		print(modified_clusters[tmp]) # correct
		(gain, cluster) = compute_gain(modified_clusters[tmp], cluster_membership, vertex, 
			vertex_has_these_edges, vertex_neighbors, graph)
		all_gains.append(gain)
		all_clusters_gained.append(cluster)
	print("\nThese are the gains in modularity")
	max_gain = all_gains[0]
	max_gain_index = 0
	for ind, gain in enumerate(all_gains):
		print(gain)
		if (gain > max_gain):
			max_gain = gain
			max_gain_index = ind
	# TODO: This below line is probably not outputting the correct index...
	# max_gain = all_gains.index( max(all_gains) )
	print("The max gain and its index are")
	print(max_gain)
	print(max_gain_index)
	# max_gain_cluster = modified_clusters[all_gains.index(max(all_gains))]
	max_gain_cluster = all_clusters_gained[max_gain_index] # fix this

	# TODO: implement a loop that adds in beta-number of possible community clusters

	# 5) Add v to the community maximizing gain
	# Already done in the compute_gain function from Step 4). 
	plot_Kamada_Kawai(max_gain_cluster)
	# plot_Kamada_Kawai(modified_graph)

	# 6.	Check if this “new” community set Cv’ is equal to the original 
	# one found in Step 1.  If so, increment the stable node counter by one 
	# (initialized to zero upon start of the larger algorithm).  
	for Cv_element in vertex_communities:
		if (Cv_element.vs["name"] != max_gain_cluster.vs["name"]):
			vertex_communities.append(max_gain_cluster)
	# for cluster in vertex_communities:
	# 	plot_Kamada_Kawai(cluster)
	return vertex_communities

def merge(cluster_one, cluster_two, alpha=0.8):
	return 

def compute_gain(cluster, cluster_membership, vertex, incident_edges, vertex_neighbors, original_graph):
	"""
	Higher modularity --> stronger community structure. Values > 0.3 indicate "strong" community. 
	1) modularity for each cluster
	2) add in vertex into the cluster
	3) recompute modularity for the modified cluster
	4) return gain = the delta b/w final & initial modularity
	"""
	initial_modularity = cluster.modularity(cluster_membership, weights=cluster.es["weight"]) 
	neighbor_in_cluster = []
	for node in cluster.vs:
		for neighbor in vertex_neighbors:
			if (node["name"] == neighbor["name"]):
					neighbor_in_cluster.append(neighbor)
	cluster.add_vertex(**vertex.attributes())
	for neighbor in neighbor_in_cluster:
		for edge in incident_edges:
			if ( (edge.target == neighbor.index) or (edge.source == neighbor.index) ):
				cluster.add_edge(vertex["name"], neighbor["name"], **edge.attributes())
	final_modularity = cluster.modularity(cluster_membership, weights=cluster.es["weight"]) 
	gain = final_modularity - initial_modularity
	return (gain, cluster)

def outer_nectar(graph, beta):
	nodes_in_graph = graph.vs
	communities_per_node = []
	for node in nodes_in_graph:
		communities_per_node.append(nectar(my_graph, beta, node.index))
	return nodes_in_graph

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
# Some community detection tools.  Just messing around here. 

# # calculate dendrogram
# my_dendrogram = my_graph.community_edge_betweenness(weights = my_graph.es["weight"])
# # convert it into a flat clustering
# my_clusters = my_dendrogram.as_clustering()
# # get the membership vector
# my_membership = my_clusters.membership

# modie = my_graph.modularity(my_membership)
# optModie = my_graph.community_optimal_modularity(my_graph.es["weight"])
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

beta = 1
# my_vertex_id = 4
my_vertex_id = 0 # Alice vertex
my_vertex = my_graph.vs[my_vertex_id]
plot_Kamada_Kawai(my_graph)
# nectar(my_graph, beta, my_vertex_id)
outer_nectar(my_graph, beta)

# tmp testing code
# louvian_output = my_graph.community_multilevel(weights=my_graph.es["weight"]) # returns a list of VertexClusters
# print(louvian_output)


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















