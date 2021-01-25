"""
    extractors
"""

import inspect
import importlib
import logging
import pkgutil


# import gitdata.extractors
from .common import BaseExtractor

logger = logging.getLogger(__name__)


class Result(object):
    """a handy bunch of variables"""
    tables = []
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def get_extractors():
    """generate connectors"""
    # path = __path__
    for _, name, _ in pkgutil.iter_modules(__path__):
        if name != 'common':
            module = importlib.import_module('gitdata.extractors.' + name)
            for _, obj in inspect.getmembers(module):
                if obj == BaseExtractor:
                    continue
                try:
                    found = issubclass(obj, BaseExtractor)
                except TypeError:
                    found = False
                if found:
                    yield obj


def extract(ref):
    """Extract a reference

    Extract data from a reference.
    """

    ref = dict(ref=ref)

    extractors = list(get_extractors())

    extracting = True
    while extracting:
        extracting = any(
            extractor().extract(ref)
            for extractor in get_extractors()
        )

    return Result(
        name=ref.get('name', ref['ref']),
        ref=ref['ref'],
        tables=ref['tables'],
        text=ref['text'],
    )

