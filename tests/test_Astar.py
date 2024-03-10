import unittest 
from grid import Grid
from solver import Solver

class Test_Swap(unittest.TestCase):
    def test_grid1(self):
        grid = Solver.grid_from_file("input/grid1.in")
        grid.Astar_improved()
        self.assertEqual(grid.state, [[1, 2], [3, 4], [5, 6], [7, 8]])

    def test_grid2(self):
        grid = Solver.grid_from_file("input/grid2.in")
        grid.Astar_improved()
        self.assertEqual(grid.state,  [[j for j in range(i,i+3)] for i in range(1,10,3)])

    def test_grid3(self):
        grid = Solver.grid_from_file("input/grid3.in")
        grid.Astar_improved()
        self.assertEqual(grid.state, [[j for j in range(i,i+4)] for i in range(1,17,4)])

    def test_grid4(self):
        grid = Solver.grid_from_file("input/grid4.in")
        grid.Astar_improved()
        self.assertEqual(grid.state, [[j for j in range(i,i+4)] for i in range(1,17,4)])
    
    def test(self):
        grid = Solver(5,5,[[20,17,19,18,21],[5,2,7,4,25],[1,6,3,22,8],[9,14,24,15,12],[23,13,10,11,16]])
        grid.Astar_improved()
        self.assertEqual(grid.state, [[j for j in range(i,i+5)] for i in range(1,26,5)])

if __name__ == '__main__':
    unittest.main()