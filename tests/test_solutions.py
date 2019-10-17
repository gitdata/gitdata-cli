"""
    gitdata.solutions tests
"""

import unittest
import datetime

import gitdata.solutions

edges = [
    (1, 2), (1, 3), (1, 4),
    (2, 5), (2, 6),
    (3, 9), (3, 11),
    (4, 7), (4, 8),
    (5, 11),
    (6, 9),
    (7, 9), (7, 10),
    (8, 10),
    (9, 11),
    (10, 11),
]

class TestPathfinder(unittest.TestCase):

    def setUp(self):
        def cost(*_):
            return 1
        self.solver = gitdata.solutions.Pathfinder(edges, cost)

    def test_solve_first_branch(self):
        self.assertEqual(self.solver.find(1, 2), [((1, 2, 1),)])

    def test_solve_second_branch(self):
        self.assertEqual(self.solver.find(1, 3), [((1, 3, 1),)])

    def test_solve_first_sub_of_first_branch(self):
        self.assertEqual(self.solver.find(1, 5), [((1, 2, 1), (2, 5, 1))])

    def test_solve_second_sub_of_third_branch(self):
        self.assertEqual(self.solver.find(1, 8), [((1, 4, 1), (4, 8, 1))])

    def test_solution_size_three(self):
        self.assertEqual(
            self.solver.find(1, 10)[0],
            ((1, 4, 1), (4, 7, 1), (7, 10, 1))
        )

    def test_multiple_solutions(self):
        self.assertEqual(
            self.solver.find(1, 10),
            [
                ((1, 4, 1), (4, 7, 1), (7, 10, 1)),
                ((1, 4, 1), (4, 8, 1), (8, 10, 1)),
            ]
        )

    def test_solution_multiple_with_size_varying(self):
        self.assertEqual(
            self.solver.find(1, 11),
            [
                ((1, 2, 1), (2, 5, 1), (5, 11, 1)),
                ((1, 2, 1), (2, 6, 1), (6, 9, 1), (9, 11, 1)),
                ((1, 3, 1), (3, 11, 1)),
                ((1, 4, 1), (4, 7, 1), (7, 10, 1), (10, 11, 1)),
            ]
        )
