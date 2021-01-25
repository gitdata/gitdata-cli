"""
    csv extractor
"""

import logging
import csv

from .common import BaseExtractor


logger = logging.getLogger(__name__)


class CSVExtractor(BaseExtractor):

    def extract(self, ref):
        cache = ref.setdefault(self.name, [])
        for blob in ref.setdefault('blob', []):
            if id(blob) not in cache:
                cache.append(id(blob))
                rows = []
                text = blob.decode('utf8')
                reader = csv.DictReader(text.splitlines())
                for row in reader:
                    rows.append(row)
                logger.info('parsing csv')
                ref.setdefault('tables', []).append(rows)
                ref.setdefault('text', []).append(text)
                return True
