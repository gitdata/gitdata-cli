"""
    gitdata graph
"""

class Graph(object):
    """Basic Graph"""

    def __init__(self, db):
        self.db = db

    def set(self, value):
        """set one or more entity values"""
        try:
            values = iter(value)
        except TypeError:
            values = iter([value])
        for value in values:
            pass
