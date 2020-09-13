"""
    gitdata stores common
"""

import base64
from datetime import datetime, date
from decimal import Decimal


def retype(value, value_type):
    """convert a value back to its original type"""
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

    return value


def entify(facts):
    """convert facts back into an entity dict

    >>> entify([(1, 'name', 'str', 'Joe'), (1, 'age', 'int', 24)])
    {'name': 'Joe', 'age': 24}

    """
    if not facts:
        return None

    return {
        attribute: retype(value, value_type)
        for _, attribute, value_type, value
        in facts
    }


def fixval(value):
    """return string represetations for specific types

    >>> fixval(datetime(2019, 11, 14))
    '2019-11-14 00:00:00'

    """
    if isinstance(value, datetime):
        # avoids reliance on strftime that lacks support
        # for dates before 1900 in some databases
        return "%02d-%02d-%02d %02d:%02d:%02d" % (
            value.year,
            value.month,
            value.day,
            value.hour,
            value.minute,
            value.second
        )
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, bytes):
        return base64.b64encode(value)
    return value


def get_type_str(value):
    """return a string representation of the value type

    >>> get_type_str('test')
    'str'

    >>> class MyThing(object):
    ...    '''something'''

    >>> get_type_str(datetime(2019, 11, 14))
    'datetime.datetime'

    """
    t = repr(type(value))
    if 'type' in t:
        return t.strip('<type >').strip("'")
    elif 'class' in t:
        return t.strip('<class >').strip("'")
    else:
        return t


class AbstractStore(object):
    """Abstract Entity Store"""

    def add(self, facts):
        """add facts to the entity store"""

    def remove(self, facts):
        """remove facts from the entity store"""

    def triples(self, pattern):
        """return facts that match the pattern"""

    def put(self, entity):
        """put an entity into the entity store"""

    def get(self, uid):
        """get an entity from the entity store"""

    def delete(self, uid):
        """delete an entity from the entity store"""

    def clear(self):
        """delete all facts from the entity store"""

    def __len__(self):
        """return the number of facts stored"""

    def __repr__(self):
        pattern = (None, None, None)
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(
                repr(rec)
                for rec in self.triples(pattern)
            )
        )

    def __str__(self):
        pattern = (None, None, None)
        return '\n'.join(repr(triple) for triple in self.triples(pattern))
