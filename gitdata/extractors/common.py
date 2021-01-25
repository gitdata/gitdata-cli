"""
    extractor common functions
"""

class BaseExtractor:
    """BaseExtractor"""

    @property
    def name(self):
        return self.__class__.__name__


    # reads = []
    # writes = []

    # @classmethod
    # def get_edges(cls):
    #     """Return connector graph edges"""
    #     for a in cls.reads:
    #         for b in cls.writes:
    #             yield a, b

    # @property
    # def edges(self):
    #     """Connector graph edges"""
    #     return self.get_edges()


