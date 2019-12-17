import csv
import json
import logging

class CsvManager:
    def __init__(self, csvpath):
        self.logger = logging.getLogger(__name__)
        self._path = csvpath
        self.reload()
        self.logger.debug('CsvManager ready')

    def reload(self):
        self._d = {}
        with open(self._path, 'r') as fh:
            for line in csv.reader(fh):
                if len(line) > 0:
                    self._d[line[0]] = line[1:]
