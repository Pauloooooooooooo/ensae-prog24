from grid import Grid
from solver import Solver
from graph import Graph

#g = Grid(2, 3)
#print(g)
"""
data_path = "../input/"
file_name = data_path + "graph1.in"

print(file_name)

a = Grid.grid_from_file(graph1)
"""
#S0 = Solver(2,2,[[2,4],[3,1]])
#print(S0.get_solution())

#S1 = Solver(4,2,[[5,2],[3,8],[1,6],[4,7]])
#print(S1.get_solution())

#S2 = Solver(3,3,[[7,5,3],[1,8,6],[4,2,9]])
#print(S2.get_solution())

#S3 = Solver(4,4,[[5,2,7,4],[1,6,3,8],[9,14,15,12],[13,10,11,16]])
#print(S3.get_solution())

#S4 = Solver(4,4,[[5,14,7,16],[1,10,15,4],[13,2,3,12],[9,6,11,8]])
#print(S4.get_solution())

g = Graph.graph_from_file("input/graph1.in")
print(g)
