import json
import unittest

import pymarc

from pyalma import records


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


class TestItemRecord(unittest.TestCase):

    def setUp(self):
        with open('test/item.dat', 'r') as f:
            self.itemdata = json.loads(f.read())

    def assertItemEqual(self, item):
        self.assertEqual(item.data['link'],
                         'https://api-na.hosted.exlibrisgroup.com/almaws/v1/' +
                         'bibs/9922405930001551/holdings/22115858660001551/' +
                         'items/23115858650001551')
        self.assertEqual(item.data['item_data']['pid'], '23115858650001551')
        self.assertEqual(item.data['holding_data']['holding_id'],
                         '22115858660001551')
        self.assertEqual(item.data['bib_data']['mms_id'], 9922405930001552)
        self.assertEqual(item.data['bib_data']['network_number'],
                         ["(CMalG)333281-gettydb-Voyager",
                          "(OCoLC)28384525", "333281"])

    def test_item_load(self):
        item = records.Item()
        item.load(self.itemdata)
        self.assertItemEqual(item)

    def test_item_init(self):
        item = records.Item(self.itemdata)
        self.assertItemEqual(item)


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


class TestAvailabilityRecord(unittest.TestCase):

    def setUp(self):
        with open('test/availability.dat', 'r') as f:
            self.availabilitydata = json.loads(f.read())

    def assertAvailabilityEqual(self, availability):
        self.assertEqual(availability.data['from_time'], 1401691527672)
        self.assertEqual(availability.data['to_time'], 1401691527672)

    def test_availability_load(self):
        availability = records.Availability()
        availability.load(self.availabilitydata)
        self.assertAvailabilityEqual(availability)

    def test_availability_init(self):
        availability = records.Availability(self.availabilitydata)
        self.assertAvailabilityEqual(availability)
