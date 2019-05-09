"""
    gitdata stores common
"""


class AbstractStore(object):

    def put(self, entity):
        """put assertions into the entity store"""
        pass

    def get(self, entity_id):
        """get assertions from the entity store"""
        pass

    def delete(self, entity):
        """delete assertions from the entity store"""
        pass

    def clear(self):
        """clear the entity store"""
        pass
