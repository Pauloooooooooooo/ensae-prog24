import unittest 
from solver import Solver

class Test_Swap(unittest.TestCase):
    def test_grid1(self):
        grid = Solver.grid_from_file("input/grid1.in")
        grid.Astar()
        self.assertEqual(grid.state, [[1, 2], [3, 4], [5, 6], [7, 8]])

    def test_grid2(self):
        grid = Solver.grid_from_file("input/grid2.in")
        grid.Astar()
        self.assertEqual(grid.state,  [[j for j in range(i,i+3)] for i in range(1,10,3)])

if __name__ == '__main__':
    unittest.main()