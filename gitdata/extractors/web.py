"""
    web extractors
"""

import logging
import requests

from .common import BaseExtractor


logger = logging.getLogger(__name__)


class HTTPExtractor(BaseExtractor):

    def extract(self, ref):
        url = ref['ref']
        if url.startswith('http://') or url.startswith('https://'):
            cache = ref.setdefault(self.name, [])
            if url not in cache:
                cache.append(url)
                r = requests.get(url)
                if r.status_code == 200:
                    logger.debug('%s successfully extracted %s', self.name, url)
                    ref.setdefault('blob', []).append(r.content)
                    return True
