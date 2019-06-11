"""
    gitdata graph
"""

import gitdata
from gitdata.utils import new_test_uid


class Graph(object):
    """Basic Graph"""

    def __init__(self, store):
        self.store = store
        self.digester = gitdata.digester.Digester(new_uid=new_test_uid(0))

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
        self.digester.digest(data)
        return self.store.add(self.digester.known)

    def get(self, uid):
        """Get a node of the graph"""
        node = self.store.get(uid)
        return node
