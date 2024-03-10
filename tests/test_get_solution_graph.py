# This will work if ran from the root folder ensae-prog24
import sys 
sys.path.append("swap_puzzle/")

import unittest 
from grid import Grid
from solver import Solver
from graph import Graph

class Test_Get_Solution_Graph(unittest.TestCase):
    def test(self):
        s = Solver(2,2,[[2,4],[3,1]])
        self.assertEqual(s.get_solution_graph(),[((0, 1), (1, 1)), ((0, 0), (0, 1))])

if __name__ == '__main__':
    unittest.main()

