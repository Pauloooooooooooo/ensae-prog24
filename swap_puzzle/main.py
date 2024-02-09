from grid import Grid


g = Grid(2, 3)
print(g)

data_path = "../input/"
file_name = data_path + "graph1.in"

print(file_name)

a = Grid.grid_from_file(graph1)

