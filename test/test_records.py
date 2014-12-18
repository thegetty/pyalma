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


class TestHoldingRecord(unittest.TestCase):

    def setUp(self):
        with open('test/hold.dat', 'r') as f:
            self.holdingdata = json.loads(f.read())

    def assertHoldingEqual(self, holding):
        self.assertEqual(holding.data['holding_id'], '22115858660001551')
        self.assertEqual(holding.data['created_date'], '2013-07-14Z')

    def test_holding_load(self):
        holding = records.Holding()
        holding.load(self.holdingdata)
        self.assertHoldingEqual(holding)        

    def test_holding_init(self):
        holding = records.Holding(self.holdingdata)
        self.assertHoldingEqual(holding)

    def test_holding_parse_marc(self):
        holding = records.Holding(self.holdingdata)
        self.assertIsInstance(holding.marc, pymarc.record.Record)
        self.assertEqual(holding.marc['014']['a'], '94-B3418')


class TestRequestRecord(unittest.TestCase):

    def setUp(self):
        with open('test/request.dat', 'r') as f:
            self.requestdata = json.loads(f.read())

    def assertRequestEqual(self, request):
        self.assertEqual(request.data['title'], 'Test title')
        self.assertEqual(request.data['request_type'], 'HOLD')

    def test_request_load(self):
        request = records.Request()
        request.load(self.requestdata)
        self.assertRequestEqual(request)        

    def test_request_init(self):
        request = records.Request(self.requestdata)
        self.assertRequestEqual(request)
