"""
    gitdata utils
"""

import uuid
import os.path


def new_uid():
    """returns a unique id"""
    return uuid.uuid4().int


def lib_path(pathname):
    """return a path relative to this repository"""
    location = os.path.dirname(__file__)
    return os.path.join(location, pathname)


def load(pathname):
    """load file contents"""
    with open(pathname) as source:
        return source.read()

