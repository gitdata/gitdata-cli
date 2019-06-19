"""
    digester

    digests data into facts
"""

import gitdata


class Digester(object):
    """Digest arbitrary data structures into triples"""

    def __init__(self, data=None, new_uid=gitdata.utils.new_uid):
        self.known = []
        self.new_uid = new_uid
        if data:
            self.digest(data)

    def _digest(self, known, data):
        """digest some data"""

        if isinstance(data, dict):
            s = self.new_uid()
            for p, o in data.items():
                known.append((s, p, self._digest(known, o)))
            return s

        elif isinstance(data, (list, tuple, set)):
            s = self.new_uid()
            for item in data:
                known.append((s, 'includes', self._digest(known, item)))
            return s

        else:
            return data

    def digest(self, data):
        """digest some data"""
        known = []
        uid = self._digest(known, data)
        self.known = known
        return uid


def digested(data):
    """Digest data retreived from a URL"""
    digester = Digester()
    digester.digest(data)
    return digester.known
