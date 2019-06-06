"""
    gitdata stores common
"""


class AbstractStore(object):
    """Abstract Entity Store"""

    def put(self, entity):
        """put assertions into the entity store"""

    def get(self, uid):
        """get assertions from the entity store"""

    def delete(self, uid):
        """delete assertions from the entity store"""

    def clear(self):
        """clear the entity store"""
