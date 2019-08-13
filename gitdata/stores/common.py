"""
    gitdata stores common
"""

import base64
import configparser
from datetime import datetime, date
from decimal import Decimal
import os
import uuid

import gitdata


def retype(value, value_type):
    """Convert a value back to its original type"""
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
    """
    converts facts back into an entity dict
    """
    if not facts:
        return None

    entity = {}
    for _, attribute, value_type, value in facts:
        value = retype(value, value_type)

        # if value_type == 'str':
        #     pass

        # elif value_type == "int":
        #     value = int(value)

        # elif value_type == 'float':
        #     value = float(value)

        # elif value_type == 'decimal.Decimal':
        #     value = Decimal(value)

        # elif value_type == "datetime.date":
        #     y = int(value[:4])
        #     m = int(value[5:7])
        #     d = int(value[8:10])
        #     value = date(y, m, d)

        # elif value_type == "datetime.datetime":
        #     y = int(value[:4])
        #     m = int(value[5:7])
        #     d = int(value[8:10])
        #     hr = int(value[11:13])
        #     mn = int(value[14:16])
        #     sc = int(value[17:19])
        #     value = datetime(y, m, d, hr, mn, sc)

        # elif value_type == 'bool':
        #     value = (value == '1' or value == 'True')

        # elif value_type == 'NoneType':
        #     value = None

        # elif value_type == 'bytes':
        #     value = base64.b64decode(value)

        # else:
        #     msg = 'unsupported data type: ' + repr(value_type)
        #     raise Exception(msg)

        entity[attribute] = value

    return entity


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

    def __len__(self):
        """return the number of facts stored"""
        return 0
