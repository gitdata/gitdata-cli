"""
    file system extractors
"""

import logging
import os

from .common import BaseExtractor


logger = logging.getLogger(__name__)


class FileExtractor(BaseExtractor):

    def extract(self, ref):
        filename = ref['ref']
        if os.path.isfile(filename):
            cache = ref.setdefault(self.name, [])
            if filename not in cache:
                cache.append(filename)
                logger.info('reading file %s', filename)
                with open(filename, 'rb') as f:
                    ref.setdefault('blob', []).append(f.read())
                    return True
