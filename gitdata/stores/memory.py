"""
    gitdata memory store
"""

import uuid

import gitdata

class MemoryStore(gitdata.stores.common.AbstractStore):

    storage = {}

    def put(self, entity):
        """put assertions into the entity store"""
        uid = entity.get('uid', uuid.uuid4().hex)
        self.storage.setdefault(uid, {}).update(entity)
        return uid

    def get(self, uid):
        """get assertions from the entity store"""
        return self.storage.get(uid)

    def delete(self, uid):
        """delete assertions from the entity store"""
        self.storage.pop(uid)

    def clear(self):
        """clear the entity store"""
        self.storage = {}

