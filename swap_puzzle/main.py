from grid import Grid
from solver import Solver
from graph import Graph
from game import Game
"""
g = Grid(2, 3)
print(g)

data_path = "input/"
file_name = data_path + "grid1.in"

print(file_name)



S0 = Solver(2,2,[[2,4],[3,1]])
"""

S1 = Solver(4,2,[[5,2],[3,8],[1,6],[4,7]])
#print(S1.get_solution())

S2 = Solver(3,3,[[7,5,3],[1,8,6],[4,2,9]])
#print(S2.get_solution())

S3 = Solver(4,4,[[5,2,7,4],[1,6,3,8],[9,14,15,12],[13,10,11,16]])
#print(S3.get_solution())

S4 = Solver(4,4,[[5,14,7,16],[1,10,15,4],[13,2,3,12],[9,6,11,8]])
#print(S4.get_solution())

S5 = Solver(5,5,[[20,17,19,18,21],[5,2,7,4,25],[1,6,3,22,8],[9,14,24,15,12],[23,13,10,11,16]])
#print(S3.get_solution())

"""
Pour la question 8, l'idée serait que lorsqu'on parourt le graphe, on ne choisisse uniquement les swaps qui intervertissent 
deux nombres de sorte à ce que le nombre le plus petit des deux se retrouve avant le plus grand, ceci se ferait en ajoutant
cette condition dans la fonction legal_move
mais ce n'est qu'une ébauche d'idée et je pense que l'on peut trouver un contre exemple facilement 
"""
#print(S4)
#print(S4.Astar_improved())

G = Game(3)
print(G.resolve())