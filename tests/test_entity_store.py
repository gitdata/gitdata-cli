"""
    entity store tests
"""
# pylint: disable=missing-docstring, no-member

from decimal import Decimal
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

    triples = [
        (2, 'name', 'Joe'),
        (2, 'age', 12),
        (1, 'includes', 2),
        (3, 'name', 'Sally'),
        (3, 'wage', 22.1),
        (1, 'includes', 3),
    ]

    def setUp(self):
        self.store = gitdata.stores.sqlite3.Sqlite3Store(':memory:')
        self.store.setup()

    def test_spo(self):
        store = self.store
        store.add(self.triples)
        self.assertEqual(
            list(self.store.triples((2, 'name', 'Joe'))),
            [(2, 'name', 'Joe')],
        )

    def test_spn(self):
        store = self.store
        store.add(self.triples)
        self.assertEqual(
            list(self.store.triples((3, 'name', None))),
            [
                (3, 'name', 'Sally')
            ],
        )

    def test_sno(self):
        store = self.store
        store.add(self.triples)
        self.assertEqual(
            list(self.store.triples((2, None, 'Joe'))),
            [
                (2, 'name', 'Joe')
            ],
        )

    def test_snn(self):
        store = self.store
        store.add(self.triples)
        self.assertEqual(
            list(self.store.triples((3, None, None))),
            [
                (3, 'name', 'Sally'),
                (3, 'wage', 22.1),
            ],
        )

    def test_npo(self):
        store = self.store
        store.add(self.triples)
        self.assertEqual(
            list(self.store.triples((None, 'name', 'Sally'))),
            [
                (3, 'name', 'Sally'),
            ],
        )

    def test_npn(self):
        store = self.store
        store.add(self.triples)
        self.assertEqual(
            list(self.store.triples((None, 'name', None))),
            [
                (2, 'name', 'Joe'),
                (3, 'name', 'Sally'),
            ],
        )

    def test_nno(self):
        store = self.store
        store.add(self.triples)
        self.assertEqual(
            list(self.store.triples((None, None, '12'))),
            [
                (2, 'age', '12'),
            ],
        )

    def test_nnn(self):
        store = self.store
        store.add(self.triples)
        self.assertEqual(
            list(self.store.triples((None, None, None))),
            [
                (2, 'name', 'Joe'),
                (2, 'age', 12),
                (1, 'includes', 2),
                (3, 'name', 'Sally'),
                (3, 'wage', 22.1),
                (1, 'includes', 3),
            ],
        )
