"""
    gitdata digester tests
"""

import unittest
import datetime

from gitdata.digester import digested, Digester
from gitdata.utils import new_test_uid

class TestDigester(unittest.TestCase):

    def setUp(self):
        self.digester = Digester(new_uid=new_test_uid(0))
        self.digester.known = []

    def test_dict(self):
        uid = self.digester.digest(dict(name='Joe', age=12))
        self.assertEqual(uid, '1')
        self.assertEqual(
            self.digester.known,
            [('1', 'name', 'Joe'), ('1', 'age', 12)],
        )

    def test_list_of_dict(self):
        uid = self.digester.digest([dict(name='Joe', age=12), dict(name='Sally')])
        self.assertEqual(uid, '1')

        print(self.digester.known)
        self.assertEqual(
            self.digester.known,
            [
                ('2', 'name', 'Joe'),
                ('2', 'age', 12),
                ('1', 'includes', '2'),
                ('3', 'name', 'Sally'),
                ('1', 'includes', '3'),
            ],
        )

    def test_single_value_ignored(self):
        data = self.digester.digest(10)
        self.assertEqual(data, 10)
        self.assertEqual(
            self.digester.known,
            [],
        )

    def test_list_of_values(self):
        uid = self.digester.digest(['one', 2, 'three'])
        self.assertEqual(uid, '1')
        self.assertEqual(
            self.digester.known,
            [
                ('1', 'includes', 'one'),
                ('1', 'includes', 2),
                ('1', 'includes', 'three')
            ],
        )

    def test_dict_with_subdict(self):
        uid = self.digester.digest(
            dict(name='Joe', age=12, friend=dict(name='Adam', age=12))
        )
        self.assertEqual(
            self.digester.known,
            [
                ('1', 'name', 'Joe'),
                ('1', 'age', 12),
                ('2', 'name', 'Adam'),
                ('2', 'age', 12),
                ('1', 'friend', '2')
            ]
        )

    def test_dict_with_list(self):
        uid = self.digester.digest(
            dict(
                name='Joe',
                age=12,
                friend=[
                    dict(name='Adam', age=12),
                    dict(name='Jim', age=22),
                ]
            ),
        )
        self.assertEqual(
            self.digester.known,
            [
                ('1', 'name', 'Joe'),
                ('1', 'age', 12),
                ('3', 'name', 'Adam'),
                ('3', 'age', 12),
                ('2', 'includes', '3'),
                ('4', 'name', 'Jim'),
                ('4', 'age', 22),
                ('2', 'includes', '4'),
                ('1', 'friend', '2')
            ]
        )
