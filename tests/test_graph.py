"""
    graph tests
"""
# pylint: disable=missing-docstring, no-member

from decimal import Decimal

import unittest

import gitdata


class GraphTests(unittest.TestCase):
    """Graph Tests"""

    def setUp(self):
        store = gitdata.stores.memory.MemoryStore()
        self.graph = gitdata.Graph(store)

    def test_set(self):
        g = self.graph
        g.set(1)
        g.set('1234')
        g.set(dict(name='joe'))
        g.set([1, 'x', Decimal('2.22')])
        g.set([dict(name='Joe', age=20), dict(name='Pat', age=24)])
