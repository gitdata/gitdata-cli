"""
    gitdata sqlite3 store
"""

import sqlite3

import gitdata
from .common import fixval, get_type_str, AbstractStore, get_uid, entify, retype

valid_types = [
    'str', 'bytes', 'int', 'float', 'decimal.Decimal',
    'datetime.date', 'datetime.datetime', 'bool', 'NoneType',
]

insert = (
    'insert into facts ('
    '    entity, attribute, value_type, value'
    ') values (?, ?, ?, ?)'
)


def get_db(connection):
    def query(cmd, *args, **kwargs):
        cursor = connection.cursor()
        cursor.execute(cmd, *args, **kwargs)
        return cursor.fetchall()
    return query


class Sqlite3Store(AbstractStore):
    """Sqlite3 based Entity Store"""

    def __init__(self, *args, **kwargs):
        self.connection = sqlite3.Connection(*args, **kwargs)

    def setup(self):
        """Set up the persistent data store"""
        with self.connection:
            cursor = self.connection.cursor()

            filename = 'sql/create_repository_sqlite3.sql'
            pathname = gitdata.utils.lib_path(filename)
            sql = gitdata.utils.load(pathname)
            commands = list(filter(bool, sql.split(';\n')))

            for command in commands:
                cursor.execute(command)

    def add(self, facts):
        """add facts"""
        records = []
        for entity, attribute, value in facts:
            value_type = get_type_str(value)
            if value_type in valid_types:
                records.append((entity, attribute, value_type, value))
            else:
                msg = 'unsupported type <type %s> in value %r'
                raise Exception(msg % (value_type, value))

        with self.connection:
            cursor = self.connection.cursor()
            cursor.executemany(insert, records)

    def triples(self, pattern):
        """Return triples matching pattern"""

        sub, pred, obj = pattern

        spn = 'select value, value_type from facts where entity=? and attribute=?'
        sno = 'select attribute from facts where entity=? and value=?'
        snn = 'select attribute, value, value_type from facts where entity=?'
        npo = 'select entity from facts where attribute=? and value=?'
        npn = 'select entity, value, value_type from facts where attribute=?'
        nno = 'select entity, attribute from facts where value=?'
        nnn = 'select entity, attribute, value, value_type from facts'

        with self.connection:
            cursor = self.connection.cursor()
            db = cursor.execute

            db = get_db(self.connection)
            if sub != None:
                if pred != None:
                    q = [retype(*a) for a in db(spn, (sub, pred))]
                    # subj pred obj
                    if obj != None:
                        if obj in q:
                            yield (sub, pred, obj)
                    # subj pred None
                    else:
                        for r in q:
                            yield (sub, pred, r)
                else:
                    # subj None obj
                    if obj != None:
                        q = [a[0] for a in db(sno, (sub, obj))]
                        for r in q:
                            yield (sub, r, obj)
                    # sub None None
                    else:
                        q = db(snn, (sub,))
                        for r, value, value_type in q:
                            yield (sub, r, retype(value, value_type))
            else:
                if pred != None:
                    # None pred obj
                    if obj != None:
                        q = db(npo, (pred, obj))
                        for s, in q:
                            yield (int(s), pred, obj)
                    # None pred None
                    else:
                        q = db(npn, (pred,))
                        for r, value, value_type in q:
                            yield (int(r), pred, retype(value, value_type))
                else:
                    # None None obj
                    if obj != None:
                        q = [(row_id, attribute) for row_id, attribute in db(nno, (obj,))]
                        for r, s in q:
                            yield (int(r), s, obj)
                    # None None None
                    else:
                        # q = [(row_id, attribute, value, value_type) for row_id, attribute, value in db(nnn)]
                        q = db(nnn)
                        for r, s, value, value_type in q:
                            yield (int(r), s, retype(value, value_type))

    def put(self, entity):
        """stores an entity"""

        keys = [k.lower() for k in entity.keys()]
        values = [entity[k] for k in keys]
        value_types = [get_type_str(v) for v in values]
        values = [fixval(i) for i in values]  # same fix as above

        for n, atype in enumerate(value_types):
            if atype not in valid_types:
                msg = 'unsupported type <type %s> in value %r'
                raise Exception(msg % (atype, keys[n]))

        uid = entity.get('uid', get_uid())

        n = len(keys)
        param_list = list(zip([uid]*n, keys, value_types, values))
        with self.connection:
            cursor = self.connection.cursor()
            cursor.executemany(insert, param_list)

        return uid

    def get(self, uid):
        """get assertions from the entity store"""
        select = 'select * from facts where entity=?'
        cursor = self.connection.cursor()
        cursor.execute(select, (uid,))
        facts = cursor.fetchall()
        result = entify(facts)
        return result

    def delete(self, uid):
        """delete assertions from the entity store"""
        select = 'delete from facts where entity=?'
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(select, (uid,))

    def clear(self):
        """clear the entity store"""
        select = 'delete from facts'
        cursor = self.connection.cursor()
        cursor.execute(select)
