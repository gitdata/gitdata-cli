"""
    abstract entity store tests
"""
# pylint: disable=missing-docstring, no-member


from decimal import Decimal


class EntityStoreSuite(object):
    """Standard Entity Store Test Suite"""

    entities = [
        dict(name='Pat', score=5, rate=Decimal('5')),
        dict(name='Sam', score=7, rate=Decimal('1')),
        dict(name='Terry', score=2, rate=Decimal('2')),
    ]

    triples = [
        ('2', 'name', 'Joe'),
        ('2', 'age', 12),
        ('1', 'includes', '2'),
        ('3', 'name', 'Sally'),
        ('3', 'wage', 22.1),
        ('1', 'includes', '3'),
    ]

    def test_add(self):
        joe = self.store.get('2')
        self.assertEqual(joe, None)
        self.store.add(self.triples)
        joe = self.store.get('2')
        self.assertEqual(joe['name'], 'Joe')

    def test_add_includes_none(self):
        four = self.store.get('4')
        self.assertEqual(four, None)
        self.store.add([
            ('4', 'name', 'Four'),
            ('4', 'age', None)
        ])
        four = self.store.get('4')
        self.assertEqual(four['name'], 'Four')
        with self.assertRaises(KeyError):
            four['age']  # pylint: disable=pointless-statement

    def test_add_only_none(self):
        four = self.store.get('4')
        self.assertEqual(four, None)
        self.store.add([
            ('4', 'name', 'Four'),
        ])
        self.store.add([
            ('4', 'age', None)
        ])
        four = self.store.get('4')
        self.assertEqual(four['name'], 'Four')
        with self.assertRaises(KeyError):
            four['age']  # pylint: disable=pointless-statement

    def test_remove(self):
        joe = self.store.get('2')
        self.assertEqual(joe, None)
        self.store.add(self.triples)
        joe = self.store.get('2')
        self.assertEqual(joe['name'], 'Joe')
        self.store.remove([('2', 'name', 'Joe')])
        joe = self.store.get('2')
        self.assertEqual(joe.get('name'), None)

    def test_put(self):
        ids = []
        for entity in self.entities:
            ids.append(self.store.put(entity))

        self.assertEqual(
            self.store.get(ids[1]),
            dict(name='Sam', score=7, rate=Decimal('1'))
        )

    def test_delete(self):
        ids = []
        for fact in self.entities:
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
        for fact in self.entities:
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

    def test_spo(self):
        store = self.store
        store.add(self.triples)
        self.assertEqual(
            list(self.store.triples(('2', 'name', 'Joe'))),
            [('2', 'name', 'Joe')],
        )

    def test_spn(self):
        store = self.store
        store.add(self.triples)
        self.assertEqual(
            list(self.store.triples(('3', 'name', None))),
            [
                ('3', 'name', 'Sally')
            ],
        )

    def test_sno(self):
        store = self.store
        store.add(self.triples)
        self.assertEqual(
            list(self.store.triples(('2', None, 'Joe'))),
            [
                ('2', 'name', 'Joe')
            ],
        )

    def test_snn(self):
        store = self.store
        store.add(self.triples)
        self.assertEqual(
            list(self.store.triples(('3', None, None))),
            [
                ('3', 'name', 'Sally'),
                ('3', 'wage', 22.1),
            ],
        )

    def test_npo(self):
        store = self.store
        store.add(self.triples)
        self.assertEqual(
            list(self.store.triples((None, 'name', 'Sally'))),
            [
                ('3', 'name', 'Sally'),
            ],
        )

    def test_npn(self):
        store = self.store
        store.add(self.triples)
        self.assertEqual(
            list(self.store.triples((None, 'name', None))),
            [
                ('2', 'name', 'Joe'),
                ('3', 'name', 'Sally'),
            ],
        )

    def test_nno(self):
        store = self.store
        store.add(self.triples)
        self.assertEqual(
            list(self.store.triples((None, None, 12))),
            [
                ('2', 'age', 12),
            ],
        )

    def test_nnn(self):
        store = self.store
        store.add(self.triples)
        self.assertEqual(
            list(self.store.triples((None, None, None))),
            [
                ('2', 'name', 'Joe'),
                ('2', 'age', 12),
                ('1', 'includes', '2'),
                ('3', 'name', 'Sally'),
                ('3', 'wage', 22.1),
                ('1', 'includes', '3'),
            ],
        )

    def test_len(self):
        store = self.store
        store.add(self.triples)
        self.assertEqual(len(store), 6)
