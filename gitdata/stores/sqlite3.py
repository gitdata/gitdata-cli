"""
    gitdata sqlite3 store
"""

import base64
from datetime import datetime, date
from decimal import Decimal
import sqlite3
import uuid

import gitdata
from . import common


def get_uid():
    """Get a unique id"""
    return uuid.uuid4().hex


def entify(facts):
    """
    converts facts back into an entity dict
    """
    if not facts:
        return None

    entity = {}
    for _, attribute, value_type, value in facts:

        if value_type == 'str':
            pass

        elif value_type == "int":
            value = int(value)

        elif value_type == 'float':
            value = float(value)

        elif value_type == 'decimal.Decimal':
            value = Decimal(value)

        elif value_type == "datetime.date":
            y = int(value[:4])
            m = int(value[5:7])
            d = int(value[8:10])
            value = date(y, m, d)

        elif value_type == "datetime.datetime":
            y = int(value[:4])
            m = int(value[5:7])
            d = int(value[8:10])
            hr = int(value[11:13])
            mn = int(value[14:16])
            sc = int(value[17:19])
            value = datetime(y, m, d, hr, mn, sc)

        elif value_type == 'bool':
            value = (value == '1' or value == 'True')

        elif value_type == 'NoneType':
            value = None

        elif value_type == 'bytes':
            value = base64.b64decode(value)

        else:
            msg = 'unsupported data type: ' + repr(value_type)
            raise Exception(msg)

        entity[attribute] = value

    return entity


class Sqlite3Store(common.AbstractStore):
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

        def fixval(d):
            if isinstance(d, datetime):
                # avoids reliance on strftime that lacks support
                # for dates before 1900 in some databases
                return "%02d-%02d-%02d %02d:%02d:%02d" % (
                    d.year,
                    d.month,
                    d.day,
                    d.hour,
                    d.minute,
                    d.second
                )
            if isinstance(d, Decimal):
                return str(d)
            if isinstance(d, bytes):
                return base64.b64encode(d)
            return d

        def get_type_str(v):
            t = repr(type(v))
            if 'type' in t:
                return t.strip('<type >').strip("'")
            elif 'class' in t:
                return t.strip('<class >').strip("'")
            else:
                return t

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
