# This will work if ran from the root folder ensae-prog24
import sys 
sys.path.append("swap_puzzle/")

import unittest 
from grid import Grid

class Test_Swap(unittest.TestCase):
    def test_grid1(self):
        grid = Grid.grid_from_file("input/grid1.in")
        grid.swap((3,0), (3,1))
        self.assertEqual(grid.state, [[1, 2], [3, 4], [5, 6], [7, 8]])

    def test_grid2(self):
        grid = Grid.grid_from_file("input/grid2.in")
        grid.swap((1,0), (1,1))
        self.assertEqual(grid.state, [[7,5,3],[8,1,6],[4,2,9]])

    def test_grid1_seq(self):
        grid = Grid.grid_from_file("input/grid1.in")
        grid.swap_seq([((3,0), (3,1)), ((3,0), (3,1))])        
        self.assertEqual(grid.state, [[1, 2], [3, 4], [5, 6], [8, 7]])

    def test_grid2_seq(self):
        grid = Grid.grid_from_file("input/grid2.in")
        grid.swap_seq([((2,0), (2,1)), ((2,1), (2,2)),((2,2),(1,2))])        
        self.assertEqual(grid.state, [[7,5,3],[1,8,4],[2,9,6]])

if __name__ == '__main__':
    unittest.main()
