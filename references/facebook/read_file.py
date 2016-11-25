import random
from igraph import *
import os

# ---------------------------------------------------------------------------------------
# Creating the graph G<V,E>
vertex_attrs = list("age")

# Reading in the input file 
path = os.path.abspath("./facebook_combined.txt")
file = open(path, 'r')
my_graph = Graph.Read_Ncol(file, names=True, directed = False, vertex_attrs = vertex_attrs )

# Coming up with random ages, gender, and formal/informal relationships
# gender_types = ["m", "f"]
# is_formal_types = [True, False]
# for vertex in my_graph.vs:
# 	# vertex["age"] = round(random.uniform(1, 65))
# 	vertex["gender"] = gender_types[round(random.uniform(0,1))]
# 	vertex["is_formal"] = is_formal_types[round(random.uniform(0,1))]

plot(my_graph)


# Close file
file.close()