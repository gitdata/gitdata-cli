"""
    common connector
"""

import inspect
import importlib
import pkgutil

import gitdata.connectors


def get_connectors():
    """generate connectors"""
    path = gitdata.connectors.__path__
    for _, name, _ in pkgutil.iter_modules(path):
        if name != 'common':
            module = importlib.import_module('gitdata.connectors.' + name)
            for _, obj in inspect.getmembers(module):
                if obj == BaseConnector:
                    continue
                try:
                    found = issubclass(obj, BaseConnector)
                except TypeError:
                    found = False
                if found:
                    yield obj


def get_connector_graph():
    """generate connector graph"""
    edges = []
    for connector in get_connectors():
        for reads, writes in connector.get_edges():
            edges.append((connector.name, reads, writes))
    return edges


class BaseConnector(object):
    """BaseConnector"""

    reads = []
    writes = []

    @classmethod
    def get_edges(cls):
        """Return connector graph edges"""
        for a in cls.reads:
            for b in cls.writes:
                yield a, b

    @property
    def edges(self):
        """Connector graph edges"""
        return self.get_edges()

    def explore(self, graph, receiver):
        """Explore a graph
        """
