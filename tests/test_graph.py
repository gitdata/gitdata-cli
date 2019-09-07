"""
    graph tests
"""
# pylint: disable=missing-docstring, no-member

import datetime
from decimal import Decimal

import unittest

import gitdata
from gitdata.utils import new_test_uid


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
        self.graph = gitdata.Graph(store, new_uid=new_test_uid(0))
        self.graph.store.clear()

    def test_set(self):
        g = self.graph
        g.set(1)
        g.set('1234')
        g.set(dict(name='joe'))
        g.set([1, 'x', Decimal('2.22')])
        g.set([dict(name='Joe', age=20), dict(name='Pat', age=24)])

    def test_empty_graph(self):
        g = self.graph
        self.assertEqual(g.triples(), [])

    def test_add(self):
        g = self.graph
        g.add([dict(name='Joe', age=20), dict(name='Pat', wage=Decimal('12.1'))])
        person = g.get('3')
        self.assertEqual(person['wage'], Decimal('12.1'))

    def test_add_none(self):
        g = self.graph
        g.add(None)
        self.assertEqual(g.triples(), [])
        # self.assertEqual(person['wage'], Decimal('12.1'))

    def test_add_value(self):
        g = self.graph
        g.add('test')
        self.assertEqual(g.triples(), [])

    def test_add_dict(self):
        g = self.graph
        g.add(dict(value=2))
        self.assertEqual(g.triples(), [('1', 'value', 2)])

    def test_add_list(self):
        g = self.graph
        g.add([1, 2, 3])
        self.assertEqual(g.triples(), [
            ('1', 'includes', 1),
            ('1', 'includes', 2),
            ('1', 'includes', 3)
        ])

    def test_add_project(self):
        g = self.graph
        project_attributes = dict(
            name='Sample',
            kind='project',
            created=datetime.datetime(2019, 6, 10),
            created_by=1,
        )
        g.add(project_attributes)
        self.assertEqual(g.triples(), [
            ('1', 'name', 'Sample'),
            ('1', 'kind', 'project'),
            ('1', 'created', datetime.datetime(2019, 6, 10)),
            ('1', 'created_by', 1)
        ])

    def test_add_project_attribute(self):
        g = self.graph
        project_attributes = dict(
            name='Sample',
            kind='project',
            created=datetime.datetime(2019, 6, 10),
            created_by=1,
        )
        g.add(project_attributes)
        node = g.first(name='Sample')
        self.assertEqual(node['kind'], 'project')

        node.add('status', 'draft')
        self.assertEqual(g.triples(), [
            ('1', 'name', 'Sample'),
            ('1', 'kind', 'project'),
            ('1', 'created', datetime.datetime(2019, 6, 10)),
            ('1', 'created_by', 1),
            ('1', 'status', 'draft'),
        ])

    def test_add_project_attribute_as_list(self):
        g = self.graph
        project_attributes = dict(
            name='Sample',
            kind='project',
            created=datetime.datetime(2019, 6, 10),
            created_by=1,
        )
        g.add(project_attributes)
        node = g.first(name='Sample')

        node.add('cities', ['Vancouver', 'Victoria'])
        self.assertEqual(g.triples(), [
            ('1', 'name', 'Sample'),
            ('1', 'kind', 'project'),
            ('1', 'created', datetime.datetime(2019, 6, 10)),
            ('1', 'created_by', 1),
            ('2', 'includes', 'Vancouver'),
            ('2', 'includes', 'Victoria'),
            ('1', 'cities', '2'),
        ])

    def test_add_project_attribute_as_list_of_objects(self):
        g = self.graph
        project_attributes = dict(
            name='Sample',
            kind='project',
            created=datetime.datetime(2019, 6, 10),
            created_by=1,
        )
        g.add(project_attributes)
        node = g.first(name='Sample')

        uid = g.add([
            dict(name='Vancouver'),
            dict(name='Victoria'),
        ])

        attribute = (node.uid, 'cities', uid)
        g.store.add([attribute])
        self.assertEqual(g.triples(), [
            ('1', 'name', 'Sample'),
            ('1', 'kind', 'project'),
            ('1', 'created', datetime.datetime(2019, 6, 10)),
            ('1', 'created_by', 1),
            ('3', 'name', 'Vancouver'),
            ('2', 'includes', '3'),
            ('4', 'name', 'Victoria'),
            ('2', 'includes', '4'),
            ('1', 'cities', '2'),
        ])

    def test_add_list_of_objects_to_node(self):
        g = self.graph
        project_attributes = dict(
            name='Sample',
            kind='project',
            created=datetime.datetime(2019, 6, 10),
            created_by=1,
        )
        g.add(project_attributes)
        node = g.first(name='Sample')

        node.add('cities', [
            dict(name='Vancouver'),
            dict(name='Victoria'),
        ])

        self.assertEqual(g.triples(), [
            ('1', 'name', 'Sample'),
            ('1', 'kind', 'project'),
            ('1', 'created', datetime.datetime(2019, 6, 10)),
            ('1', 'created_by', 1),
            ('3', 'name', 'Vancouver'),
            ('2', 'includes', '3'),
            ('4', 'name', 'Victoria'),
            ('2', 'includes', '4'),
            ('1', 'cities', '2'),
        ])

    def test_query(self):
        g = self.graph
        g.add(self.data)
        answer = g.query([
            ('?uid', 'name', '?name'),
            ('?uid', 'kind', 'user'),
        ])
        self.assertEqual(answer, [
            {'uid': '4', 'name': 'Joe'},
            {'uid': '5', 'name': 'Sally'}
        ])

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

    def test_delete(self):
        g = self.graph
        g.add(self.data)

        self.assertEqual(g.query([
            ('?uid', 'name', '?name'),
            ('?uid', 'kind', 'user'),
        ]), [
            {'uid': '4', 'name': 'Joe'},
            {'uid': '5', 'name': 'Sally'}
        ])

        g.delete((None, 'name', 'Joe'))

        self.assertEqual(g.query([
            ('?uid', 'name', '?name'),
            ('?uid', 'kind', 'user'),
        ]), [
            {'uid': '5', 'name': 'Sally'}
        ])

    def test_len(self):
        g = self.graph
        g.add(self.data)
        self.assertEqual(len(g), 20)
