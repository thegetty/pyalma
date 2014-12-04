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
        self.assertEqual(bib.mms_id, 9922405930001552)
        self.assertEqual(bib.created_date, '2013-07-14Z')

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

    @responses.activate
    def test_alt_init(self):
        os.environ['ALMA_API_KEY'] = 'my fake key'
        os.environ['ALMA_API_REGION'] = 'APAC'
        reload(alma)
        biburl = 'https://api-ap.hosted.exlibrisgroup.com/almaws/v1/bibs/9922405930001552'
        responses.add(responses.GET, biburl, 
            status=200, 
            content_type='application/json',
            body=json.dumps(self.bibdata))
        api = alma.Alma()
        bib = records.Bib(api=api, mms_id=9922405930001552)
        self.assertBibEqual(bib)
