"""
    console connector
"""


from .common import BaseConnector


class ConsoleConnector(BaseConnector):
    """Console Connector"""

    name = 'console'
    reads = ['text']
    writes = ['stdout']

    def explore(self, data):
        """Explore Text"""
        print('exploring', data)
