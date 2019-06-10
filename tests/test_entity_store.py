"""
    entity store tests
"""
# pylint: disable=missing-docstring, no-member

import unittest

import gitdata
from gitdata.testing.stores import EntityStoreSuite


class MemoryStoreTests(EntityStoreSuite, unittest.TestCase):
    """Memory Store Tests"""

    def setUp(self):
        self.store = gitdata.stores.memory.MemoryStore()
        self.store.setup()


class Sqlite3StoreTests(EntityStoreSuite, unittest.TestCase):
    """Sqlite3 Store Tests"""

    def setUp(self):
        self.store = gitdata.stores.sqlite3.Sqlite3Store(':memory:')
        self.store.setup()