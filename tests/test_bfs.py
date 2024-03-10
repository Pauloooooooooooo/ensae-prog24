# This will work if ran from the root folder ensae-prog24
import sys 
sys.path.append("swap_puzzle/")

import unittest 
from grid import Grid
from solver import Solver
from graph import Graph

class Test_Swap(unittest.TestCase):
    def test_graph1(self):
        graph = Graph.graph_from_file("input/graph1.in")
        self.assertEqual(graph.bfs(1,15), [1,15])

    def test_graph1b(self):
        graph = Graph.graph_from_file("input/graph1.in")
        self.assertEqual(graph.bfs(1,3), [1,15,3])

    def test_graph1c(self):
        graph = Graph.graph_from_file("input/graph1.in")
        self.assertEqual(graph.bfs(7,16), [7, 3, 15, 16])

    def test_graph2(self):
        graph = Graph.graph_from_file("input/graph2.in")
        self.assertEqual(graph.bfs(1,5), None)

    def test_graph2a(self):
        graph = Graph.graph_from_file("input/graph2.in")
        self.assertEqual(graph.bfs(2,9), [2, 17, 7, 9])

if __name__ == '__main__':
    unittest.main()