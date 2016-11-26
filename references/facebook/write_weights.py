import random
from igraph import *
import os

# ---------------------------------------------------------------------------------------
# Creating the graph G<V,E>

# Reading in the input file 
path = os.path.abspath("./facebook_combined.txt")
file = open(path, 'r')
my_graph = Graph.Read_Ncol(file, names=True, directed = False)

# Coming up with random ages, gender, and formal/informal relationships
age_variance = 1*round(random.uniform(1,2))
gender_types = ["m", "f"]
is_formal_types = [True, False]
for vertex in my_graph.vs:
	vertex["age"] = round(random.uniform(1, 65))
	vertex["gender"] = gender_types[round(random.uniform(0,1))]

# Adding weights to these edges.  Weights are determined by age deltas b/w nodes. Also adding in formal/informal relationships. 
weights = list();
for edge in my_graph.es:
	source_vertex = my_graph.vs[edge.source]["age"]
	target_vertex = my_graph.vs[edge.target]["age"]
	edge["is_formal"] = is_formal_types[round(random.uniform(0,1))]
	weights.append( abs(source_vertex - target_vertex) + age_variance)
my_graph.es["weight"] = weights

# ---------------------------------------------------------------------------------------
# Writing data to txt files

# Writing to file weighted_graph.txt
output_file = open("weighted_graph.txt", "w")
edge_attr_file = open("edge_attr_file.txt", "w")
for edge in my_graph.es:
	source_vertex = str(my_graph.vs[edge.source]["name"])
	target_vertex = str(my_graph.vs[edge.target]["name"])
	weight = str(edge["weight"])
	is_formal = str(edge["is_formal"])
	output_file.write(source_vertex + ' ' + target_vertex + ' ' + weight + '\n')
	edge_attr_file.write(is_formal + '\n')
	# output_file.write(source_vertex + ' ' + target_vertex + ' ' + weight + ' ' + source_vertex_age + ' ' + target_vertex_age + '\n')

# Writing supplementary vertex attributes
vertex_attr_file = open("vertex_attr_file.txt", "w")
for vertex in my_graph.vs:
	age = str(vertex["age"])
	gender = str(vertex["gender"])
	vertex_attr_file.write(age + ' ' + gender + '\n')

# Close files
file.close()
output_file.close()
edge_attr_file.close()
vertex_attr_file.close()



















