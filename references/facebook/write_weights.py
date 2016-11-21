# ---------------------------------------------------------------------------------------
# Creating the graph G<V,E>

# Reading in the input file 
path = os.path.abspath("./facebook_combined.txt")
file = open(path, 'r')
my_graph = Graph.Read_Ncol(file, directed = False)

# Coming up with random ages, gender, and formal/informal relationships
gender_types = ["m", "f"]
is_formal_types = [True, False]
for vertex in my_graph.vs:
	vertex["age"] = round(random.uniform(1, 65))
	vertex["gender"] = gender_types[round(random.uniform(0,1))]
	vertex["is_formal"] = is_formal_types[round(random.uniform(0,1))]

# Adding weights to these edges.  Weights are determined by age deltas b/w nodes. 
weights = list();
for edge in my_graph.es:
	source_vertex = my_graph.vs[edge.source]["age"]
	target_vertex = my_graph.vs[edge.target]["age"]
	weights.append( abs(source_vertex - target_vertex) )
my_graph.es["weight"] = weights

# Writing to file weighted_graph.txt
output_file = open("weighted_graph.txt", 'w')
for edge in my_graph.es:
	source_vertex = str(my_graph.vs[edge.source]["name"])
	target_vertex = str(my_graph.vs[edge.target]["name"])
	weight = str(edge["weight"])
	output_file.write(source_vertex + ' ' + target_vertex + ' ' + weight + '\n')
	# output_file.write( "{} {} {}".format( str(edge.source["name"]), str(edge.target["name"]), str(edge["weight"]) ) )

# Close file
file.close()
output_file.close()