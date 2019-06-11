"""
    gitdata memory store
"""

import uuid

from . import common

class MemoryStore(common.AbstractStore):
    """Memory based Entity Store"""

    facts = []

    def setup(self):
        """Setup persistent store"""
        self.facts = []

    def add(self, facts):
        self.facts.extend(facts)

    def put(self, entity):
        """put assertions into the entity store"""
        uid = entity.get('uid', uuid.uuid4().hex)
        facts = ((uid, attribute, value) for attribute, value in entity.items())
        self.add(facts)
        return uid

    def get(self, uid):
        """get assertions from the entity store"""
        result = {}
        for entity, attribute, value in self.facts:
            if entity == uid:
                result[attribute] = value
        return result or None

    def delete(self, uid):
        """delete assertions from the entity store"""
        self.facts[:] = (fact for fact in self.facts if fact[0] != uid)

    def clear(self):
        """clear the entity store"""
        self.facts = []

    def triples(self, pattern):
        """Return triples matching pattern"""

        sub, pred, obj = pattern

        data = [
            (entity, attribute, value)
            for (entity, attribute, value) in self.facts
            if (
                (sub is None or sub == entity) and
                (pred is None or pred == attribute) and
                (obj is None or obj == value)
            )
        ]
        return data
