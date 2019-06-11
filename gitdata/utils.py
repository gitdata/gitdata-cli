"""
    gitdata utils
"""

import uuid
import os.path
import platform


def new_uid():
    """returns a unique id"""
    return uuid.uuid4().int


def new_test_uid(start=0):
    """a simple id generator for testing

    Returns a simple id generator that with a given integer
    and increments by one ech time its called which allows
    predictable uid values for testing.
    """
    n = [start]
    def _new_id():
        n[0] += 1
        return n[0]
    return _new_id


def lib_path(pathname):
    """return a path relative to this repository"""
    location = os.path.dirname(__file__)
    return os.path.join(location, pathname)


def load(pathname):
    """load file contents"""
    with open(pathname) as source:
        return source.read()


def space(items):
    """Space items evenly into columns"""
    items = list(items)
    max_len = max(map(len, items))
    lengths = [max([len(item[i]) for r, item in enumerate(items)]) for i in range(max_len)]
    fmt ='  '.join(('{:%s.%s}' % (length,length)) for length in lengths)
    return '\n'.join(fmt.format(*item) for item in items)


def as_uri(location):
    """Returns a local file system location as a file URI (rfc8089)"""
    return 'file://{}{}'.format(platform.node(), os.path.realpath(location))

