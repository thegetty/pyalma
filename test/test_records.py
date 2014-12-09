import os
from importlib import reload
import json
import unittest

import pymarc
import responses

from pyalma import alma, records


class TestBibRecord(unittest.TestCase):

    def setUp(self):
        with open('test/bib.dat', 'r') as f:
            self.bibdata = json.loads(f.read())

    def assertBibEqual(self, bib):
        self.assertEqual(bib.data['mms_id'], 9922405930001552)
        self.assertEqual(bib.data['created_date'], '2013-07-14Z')

    def test_bib_load(self):
        bib = records.Bib()
        bib.load(self.bibdata)
        self.assertBibEqual(bib)        

    def test_bib_init(self):
        bib = records.Bib(self.bibdata)
        self.assertBibEqual(bib)

    def test_bib_parse_marc(self):
        bib = records.Bib(self.bibdata)
        self.assertIsInstance(bib.marc, pymarc.record.Record)
        self.assertEqual(bib.marc.author(), 'Tufte, Edward R., 1942-')
