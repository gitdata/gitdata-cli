"""
    gitdata graph
"""

import gitdata
import gitdata.digester


class Node(object):
    """Graph Node"""

    def __init__(self, graph, uid):
        self.graph = graph
        self.uid = uid

    def add(self, relation, data):
        """Add a related data to a node"""
        uid = self.graph.add(data)
        self.graph.store.add([(self.uid, relation, uid)])
        return uid

    def delete(self):
        """Delete all facts related to a node"""
        self.graph.store.remove(
            self.graph.triples((self.uid, None, None))
        )

    def __getitem__(self, name):
        values = self.graph.triples((self.uid, name, None))
        return values[0][-1] if values else None

    def __str__(self):
        pattern = (self.uid, None, None)

        name = '{}({})'.format(
            self.__class__.__name__,
            self.uid
        )
        t = []

        for _, key, value in self.graph.triples(pattern):
            t.append('  {} {}: {!r}'.format(
                key,
                '.'*(20-len(key[:20])),
                value
            ))
        return '\n'.join([name] + t)

    def __repr__(self):
        pattern = (self.uid, None, None)
        return 'Node({})'.format(
            ', '.join(
                '{}: {!r}'.format(*rec[1:])
                for rec in self.graph.triples(pattern)
            )
        )


class Graph(object):
    """Basic Graph"""

    def __init__(self, store, new_uid=gitdata.utils.new_uid):
        self.store = store
        self.digester = gitdata.digester.Digester(new_uid=new_uid)

    def set(self, value):
        """set one or more entity values"""
        try:
            values = iter(value)
        except TypeError:
            values = iter([value])
        for value in values:
            pass

    def add(self, data):
        """Add arbitrary data to the graph"""
        self.digester.store = []
        uid = self.digester.digest(data)
        self.store.add(self.digester.known)
        return uid

    def delete(self, pattern):
        """Delete all triples matching the pattern"""
        facts = self.triples(pattern)
        self.store.remove(facts)
        return 1

    def get(self, uid):
        """Get a node of the graph"""
        return Node(self, uid)

    def triples(self, pattern=(None, None, None)):
        """Find graph triples that match a pattern"""
        return self.store.triples(pattern)

    def clear(self):
        """Clear the graph"""
        return self.store.clear()

    def query(self, clauses):
        """Query the graph"""
        bindings = None
        for clause in clauses:
            bpos = {}
            qc = []
            for pos, x in enumerate(clause):
                if type(x) == str and (x.startswith('?') or x.startswith('_')):
                    qc.append(None)
                    bpos[x] = pos
                else:
                    qc.append(x)
            rows = list(self.triples((qc[0], qc[1], qc[2])))
            if bindings == None:
                # This is the first pass, everything matches
                bindings = []
                for row in rows:
                    binding = {}
                    for var, pos in bpos.items():
                        binding[var] = row[pos]
                    bindings.append(binding)
            else:
                # in subsequent passes, eliminate bindings that dont work
                newb = []
                for binding in bindings:
                    for row in rows:
                        validmatch = True
                        tempbinding = binding.copy()
                        for var, pos in bpos.items():
                            if var in tempbinding:
                                if tempbinding[var] != row[pos]:
                                    validmatch = False
                            else:
                                tempbinding[var] = row[pos]
                        if validmatch:
                            newb.append(tempbinding)
                bindings = newb
        return [
            dict(
                (k[1:], v)
                for k, v in b.items()
                if k[0] == '?'
            ) for b in bindings
        ]

    def find(self, *args, **kwargs):
        """Find nodes"""
        query = []
        for i in args:
            query.append(('?subject', i, '?'+i))
        for k, v in kwargs.items():
            query.append(('?subject', k, v))
        return [
            self.get(record['subject'])
            for record in self.query(query)
        ]

    def first(self, *args, **kwargs):
        """Find first node"""
        result = self.find(*args, **kwargs)
        if result:
            return result[0]

    def exists(self, *args, **kwargs):
        """Return True if specified nodes exist else return False"""
        return bool(self.first(*args, **kwargs))

    def __str__(self):
        """Human friendly string representation"""
        return '\n'.join(repr(triple) for triple in self.triples())

    def __len__(self):
        return len(self.store)
