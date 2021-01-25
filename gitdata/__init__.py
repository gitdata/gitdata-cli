"""
    gitdata
"""

import gitdata.utils
import gitdata.stores
from pprint import pprint

from .__version__ import __version__

from .graph import Graph, Node
from .repositories import Repository
from .extractors import extract

def fetch(ref):
    """Fetch Data"""
    return extract(ref)

def explore(ref):
    """Explore Data"""
    data = extract(ref)
    for table in data.tables:
        # for row in table:
        pprint(table, width=120)
