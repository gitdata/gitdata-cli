"""
    gitdata sqlite3 store
"""

import sqlite3

import gitdata
from .common import fixval, get_type_str, AbstractStore, get_uid, entify


class Sqlite3Store(AbstractStore):
    """Sqlite3 based Entity Store"""

    def __init__(self, *args, **kwargs):
        self.connection = sqlite3.Connection(*args, **kwargs)
        with self.connection:
            cursor = self.connection.cursor()

            filename = 'sql/create_repository_sqlite3.sql'
            pathname = gitdata.utils.lib_path(filename)
            sql = gitdata.utils.load(pathname)
            commands = list(filter(bool, sql.split(';\n')))

            for command in commands:
                cursor.execute(command)

    def put(self, entity):
        """stores an entity"""

        keys = [k.lower() for k in entity.keys()]
        values = [entity[k] for k in keys]
        value_types = [get_type_str(v) for v in values]
        values = [fixval(i) for i in values]  # same fix as above
        valid_types = [
            'str', 'bytes', 'int', 'float', 'decimal.Decimal',
            'datetime.date', 'datetime.datetime', 'bool', 'NoneType',
        ]

        for n, atype in enumerate(value_types):
            if atype not in valid_types:
                msg = 'unsupported type <type %s> in value %r'
                raise Exception(msg % (atype, keys[n]))

        uid = entity.get('uid', get_uid())

        n = len(keys)
        param_list = list(zip([uid]*n, keys, value_types, values))
        insert = (
            'insert into facts ('
            '    entity, attribute, value_type, value'
            ') values (?, ?, ?, ?)'
        )
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
