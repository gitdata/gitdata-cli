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
            """0 facts\n0 remotes"""
        )

