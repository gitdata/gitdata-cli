"""
    gitdata repository tests
"""

import unittest
import gitdata.repositories

class TestRepository(unittest.TestCase):

    def setUp(self):
        self.repository = gitdata.repositories.Repository(':memory:')
        self.repository.open()

    def test_status(self):
        self.assertEqual(
            self.repository.status(),
            """0 local\n0 facts\n0 remotes"""
        )

    def test_fetch(self):
        self.repository.fetch('examples/miserables.json')
        self.assertEqual(
            self.repository.status(),
            """1 local\n4 facts\n0 remotes"""
        )

    def test_fetch_same(self):
        self.repository.fetch('examples/miserables.json')
        self.assertEqual(
            self.repository.status(),
            """1 local\n4 facts\n0 remotes"""
        )

        self.repository.fetch('examples/miserables.json')
        self.assertEqual(
            self.repository.status(),
            """1 local\n4 facts\n0 remotes"""
        )

    def test_clear(self):
        self.repository.fetch('examples/miserables.json')
        self.assertEqual(
            self.repository.status(),
            """1 local\n4 facts\n0 remotes"""
        )
        self.repository.clear({'<args>': '--all'})
        self.assertEqual(
            self.repository.status(),
            """0 local\n0 facts\n0 remotes"""
        )

