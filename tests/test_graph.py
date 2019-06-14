"""
    graph tests
"""
# pylint: disable=missing-docstring, no-member

import datetime
from decimal import Decimal

import unittest

import gitdata


class GraphTests(unittest.TestCase):
    """Graph Tests"""

    data = [
        dict(
            users=[
                dict(
                    kind='user',
                    name='Joe',
                    birthdate=datetime.date(1991, 1, 2)
                ),
                dict(
                    kind='user',
                    name='Sally',
                    birthdate=datetime.date(1991, 1, 2),
                ),
            ]
        ),
        dict(
            projects=[
                dict(
                    kind='project',
                    name='Project One',
                    created=datetime.datetime(2019, 5, 2)
                ),
                dict(
                    kind='project',
                    name='Project Two',
                    created=datetime.datetime(2019, 5, 3)
                ),
            ]
        ),
    ]

    def setUp(self):
        store = gitdata.stores.memory.MemoryStore()
        self.graph = gitdata.Graph(store)
        self.graph.store.clear()

    def test_set(self):
        g = self.graph
        g.set(1)
        g.set('1234')
        g.set(dict(name='joe'))
        g.set([1, 'x', Decimal('2.22')])
        g.set([dict(name='Joe', age=20), dict(name='Pat', age=24)])

    def test_add(self):
        g = self.graph
        g.add([dict(name='Joe', age=20), dict(name='Pat', wage=Decimal('12.1'))])
        person = g.get(3)
        self.assertEqual(person['wage'], Decimal('12.1'))

    # def test_query(self):
    #     g = self.graph
    #     g.add(self.data)
    #     answer = g.query([('?uid', 'name', '?name')])
    #     print(answer)
    #     self.assertEqual(answer, None)

    def test_find(self):
        g = self.graph
        g.add(self.data)
        answer = g.find(kind='project')
        self.assertEqual(len(answer), 2)
        self.assertEqual(answer[1]['name'], 'Project Two')

    def test_find_missing(self):
        g = self.graph
        g.add(self.data)
        answer = g.find(kind='animal')
        self.assertEqual(answer, [])

    def test_first(self):
        g = self.graph
        g.add(self.data)
        project1 = g.first(kind='project')
        self.assertEqual(project1['name'], 'Project One')

    def test_first_missing(self):
        g = self.graph
        g.add(self.data)
        answer = g.first(kind='animal')
        self.assertEqual(answer, None)