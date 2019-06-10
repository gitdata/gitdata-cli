"""
    abstract entity store tests
"""
# pylint: disable=missing-docstring, no-member


from decimal import Decimal


class EntityStoreSuite(object):
    """Standard Entity Store Test Suite"""

    facts = [
        dict(name='Pat', score=5, rate=Decimal('5')),
        dict(name='Sam', score=7, rate=Decimal('1')),
        dict(name='Terry', score=2, rate=Decimal('2')),
    ]

    def test_put(self):
        ids = []
        for fact in self.facts:
            ids.append(self.store.put(fact))

        self.assertEqual(
            self.store.get(ids[1]),
            dict(name='Sam', score=7, rate=Decimal('1'))
        )

    def test_delete(self):
        ids = []
        for fact in self.facts:
            ids.append(self.store.put(fact))

        self.store.delete(ids[1])

        self.assertEqual(
            self.store.get(ids[1]),
            None
        )

        self.assertEqual(
            self.store.get(ids[2]),
            {'name': 'Terry', 'score': 2, 'rate': Decimal('2')}
        )

    def test_clear(self):
        ids = []
        for fact in self.facts:
            ids.append(self.store.put(fact))

        self.store.clear()

        self.assertEqual(
            self.store.get(ids[1]),
            None
        )

        self.assertEqual(
            self.store.get(ids[2]),
            None
        )

    def test_store_text(self):
        new_id = self.store.put(dict(value='test'))
        entity = self.store.get(new_id)
        self.assertEqual(entity['value'], 'test')

    def test_store_integer(self):
        value = 1
        new_id = self.store.put(dict(value=value))
        entity = self.store.get(new_id)
        self.assertEqual(entity['value'], value)

    def test_supported_values(self):
        values = ['test', 1, Decimal('2.1')]
        for value in values:
            new_id = self.store.put(dict(value=value))
            entity = self.store.get(new_id)
            self.assertEqual(entity['value'], value)
