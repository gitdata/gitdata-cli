"""
    digester

    digests data into facts
"""

import gitdata


class Digester(object):

    known = []

    def __init__(self, data=None, new_uid=gitdata.utils.new_uid):
        if data:
            self.digest(data)
        self.new_uid = new_uid

    def digest(self, data):
        """digest some data"""
        known = self.known

        if isinstance(data, dict):
            s = self.new_uid()
            for p, o in data.items():
                known.append((s, p, self.digest(o)))
            return s

        elif isinstance(data, (list, tuple, set)):
            s = self.new_uid()
            for item in data:
                known.append((s, 'includes', self.digest(item)))
            return s

        else:
            return data

    # def __str__(self):
    #     labels = 'Subject', 'Predicate', 'Object'
    #     return str(zoom.utils.ItemList(self.known, labels=labels))


def digested(data):
    """Digest data retreived from a URL"""
    digester = Digester()
    return digester.digest(data).known
