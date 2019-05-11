"""
    gitdata digester tests
"""

import unittest
import datetime

from gitdata.digester import digested, Digester


def new_uid(start=0):
    """a simple id generator

    Returns a simple id generator that starts where ever we
    want and increments by one ech time its called.  Allows
    easy predictable testing.
    """
    n = [start]
    def _new_id():
        n[0] += 1
        return n[0]
    return _new_id


class TestDigester(unittest.TestCase):

    def setUp(self):
        self.digester = Digester(new_uid=new_uid(0))
        self.digester.known = []

    def test_dict(self):
        uid = self.digester.digest(dict(name='Joe', age=12))
        self.assertEqual(uid, 1)
        self.assertEqual(
            self.digester.known,
            [(1, 'name', 'Joe'), (1, 'age', 12)],
        )

    def test_list_of_dict(self):
        uid = self.digester.digest([dict(name='Joe', age=12), dict(name='Sally')])
        self.assertEqual(uid, 1)

        print(self.digester.known)
        self.assertEqual(
            self.digester.known,
            [
                (2, 'name', 'Joe'),
                (2, 'age', 12),
                (1, 'includes', 2),
                (3, 'name', 'Sally'),
                (1, 'includes', 3),
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
        self.assertEqual(uid, 1)
        self.assertEqual(
            self.digester.known,
            [
                (1, 'includes', 'one'),
                (1, 'includes', 2),
                (1, 'includes', 'three')
            ],
        )

