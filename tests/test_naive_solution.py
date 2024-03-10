# This will work if ran from the root folder ensae-prog24
import sys 
sys.path.append("swap_puzzle/")

import unittest 
from grid import Grid
from solver import Solver

class Test_Naive_Solution(unittest.TestCase):
    def test_grid1(self):
        grid = Solver.grid_from_file("input/grid1.in")
        grid.get_solution()
        self.assertEqual(grid.state, [[1, 2], [3, 4], [5, 6], [7, 8]])

    def test_grid2(self):
        grid = Solver.grid_from_file("input/grid2.in")
        grid.get_solution()
        self.assertEqual(grid.state, [[j for j in range(i,i+3)] for i in range(1,10,3)])

    def test_grid3(self):
        grid = Solver.grid_from_file("input/grid3.in")
        grid.get_solution()
        self.assertEqual(grid.state, [[j for j in range(i,i+4)] for i in range(1,17,4)])

    def test_grid4(self):
        grid = Solver.grid_from_file("input/grid4.in")
        grid.get_solution()
        self.assertEqual(grid.state, [[j for j in range(i,i+4)] for i in range(1,17,4)])
    
if __name__ == '__main__':
    unittest.main()
