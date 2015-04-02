import json
import os
import re
from importlib import reload
import unittest

import responses

from pyalma import alma, records


def setUpModule():
    os.environ['ALMA_API_KEY'] = 'my fake key'
    os.environ['ALMA_API_REGION'] = 'APAC'
    reload(alma)


class TestAlmaSetup(unittest.TestCase):

    def test_init(self):
        api = alma.Alma(apikey='unreal', region='EU')
        self.assertEqual(api.apikey, 'unreal')
        self.assertEqual(api.endpoint, alma.ENDPOINTS['EU'])

    def test_init_errors(self):
        self.assertRaises(Exception, alma.Alma, **{'apikey': None})
        self.assertRaises(Exception, alma.Alma, **{'region': None})
        self.assertRaises(Exception, alma.Alma, **{'region': 'XX'})

    def test_init_env_vars(self):
        api = alma.Alma()
        self.assertEqual(api.apikey, 'my fake key')
        self.assertEqual(api.endpoint, alma.ENDPOINTS['APAC'])

    def test_baseurl(self):
        api = alma.Alma()
        url = 'https://api-ap.hosted.exlibrisgroup.com/almaws/v1/'
        self.assertEqual(api.baseurl, url)

    def test_fullurl(self):
        ids = {'mms_id': 7777777, 'holding_id': 55555, 'item_pid': 333}
        expect = 'https://api-ap.hosted.exlibrisgroup.com/almaws/v1/'
        expect += 'bibs/7777777/holdings/55555/items/333'
        url = alma.Alma().fullurl('item', ids)
        self.assertEqual(url, expect)

    def test_headers(self):
        expect = {
            'User-Agent': 'pyalma/0.1.0',
            'Authorization': 'apikey my fake key',
            'Accept': 'application/json',
            'Content-Type': 'application/xml'
        }
        headers = alma.Alma().headers(content_type='xml')
        self.assertEqual(headers, expect)


class TestAlmaGETRequests(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.api = alma.Alma(apikey='unreal', region='EU')

    def buildResponses(self):
        # bib mock response
        biburl = self.api.baseurl + r'bibs/\d+$'
        bib_re = re.compile(biburl)
        with open('test/bib.dat', 'r') as b:
            responses.add(responses.GET, bib_re,
                          status=200,
                          content_type='application/json',
                          body=b.read())

        # holdings mock response
        holdsurl = self.api.baseurl + r'bibs/\d+/holdings$'
        holds_re = re.compile(holdsurl)
        with open('test/holds.dat', 'r') as hs:
            responses.add(responses.GET, holds_re,
                          status=200,
                          content_type='application/json',
                          body=hs.read())

        # holding mock response
        holdurl = self.api.baseurl + r'bibs/\d+/holdings/\d+$'
        hold_re = re.compile(holdurl)
        with open('test/hold.dat', 'r') as h:
            responses.add(responses.GET, hold_re,
                          status=200,
                          content_type='application/json',
                          body=h.read())

        #items mock response
        itemsurl = self.api.baseurl + r'bibs/\d+/holdings/\d+/items$'
        items_re = re.compile(itemsurl)
        with open('test/items.dat', 'r') as its:
            responses.add(responses.GET, items_re,
                          status=200,
                          content_type='application/json',
                          body=its.read())

        # item mock response
        itemurl = self.api.baseurl + r'bibs/\d+/holdings/\d+/items/\d+$'
        item_re = re.compile(itemurl)
        with open('test/item.dat', 'r') as i:
            responses.add(responses.GET, item_re,
                          status=200,
                          content_type='application/json',
                          body=i.read())

        # bib_requests mock response
        bib_requestsurl = self.api.baseurl + r'bibs/\d+/requests'
        bib_requests_re = re.compile(bib_requestsurl)
        with open('test/request.dat', 'r') as f:
            responses.add(responses.GET, bib_requests_re,
                          status=200,
                          content_type='application/json',
                          body=f.read())

        # item_requests mock response
        item_requestsurl = self.api.baseurl + \
            r'bibs/\d+/holdings/\d+/items/\d+/requests'
        item_requests_re = re.compile(item_requestsurl)
        with open('test/request.dat', 'r') as f:
            responses.add(responses.GET, item_requests_re,
                          status=200,
                          content_type='application/json',
                          body=f.read())

        # bib_booking_availability mock response
        bib_booking_availabilityurl = self.api.baseurl + \
            r'bibs/\d+/booking-availability'
        bib_booking_availability_re = re.compile(bib_booking_availabilityurl)
        with open('test/availability.dat', 'r') as f:
            responses.add(responses.GET, bib_booking_availability_re,
                          status=200,
                          content_type='application/json',
                          body=f.read())

        # item_booking_availability mock response
        item_booking_availabilityurl = self.api.baseurl + \
            r'bibs/\d+/holdings/\d+/items/\d+/booking-availability'
        item_booking_availability_re = re.compile(item_booking_availabilityurl)
        with open('test/availability.dat', 'r') as f:
            responses.add(responses.GET, item_booking_availability_re,
                          status=200,
                          content_type='application/json',
                          body=f.read())


    def buildXMLResponses(self):
        # bib mock response
        biburl = self.api.baseurl + r'bibs/\d+'
        bib_re = re.compile(biburl)
        with open('test/bib.dat.xml', 'r') as f:
            responses.add(responses.GET, bib_re,
                          status=200,
                          content_type='application/xml',
                          body=f.read())

    @responses.activate
    def test_alma_request(self):
        self.buildResponses()
        resp = self.api.request('GET', 'bib', {'mms_id': 9922405930001552})
        data = resp.json()
        self.assertEqual(data['created_date'], '2013-07-14Z')

    @responses.activate
    def test_extract_content_xml(self):
        self.buildXMLResponses()
        resp = self.api.request('GET', 'bib', {'mms_id': 9922405930001552})
        data = self.api.extract_content(resp)
        with open('test/bib.dat.xml', 'r') as dat:
            self.assertEqual(data, dat.read())

    @responses.activate
    def test_extract_content_json(self):
        self.buildResponses()
        resp = self.api.request('GET', 'bib', {'mms_id': 9922405930001552})
        data = self.api.extract_content(resp)
        with open('test/bib.dat', 'r') as dat:
            self.assertEqual(data, json.loads(dat.read()))

    @responses.activate
    def test_alma_get_bib(self):
        self.buildResponses()
        bib_data = self.api.get_bib(9922405930001552)
        with open('test/bib.dat', 'r') as dat:
            self.assertEqual(bib_data, json.loads(dat.read()))

    @responses.activate
    def test_alma_bib(self):
        self.buildResponses()
        bib = self.api.bib(9922405930001552)
        self.assertIsInstance(bib, records.Bib)

    @responses.activate
    def test_alma_get_holdings(self):
        self.buildResponses()
        holdings_data = self.api.get_holdings(99100383900121)
        with open('test/holds.dat', 'r') as dat:
            self.assertEqual(holdings_data, json.loads(dat.read()))

    @responses.activate
    def test_alma_holdings(self):
        self.buildResponses()
        holdings = self.api.holdings(99100383900121)
        self.assertIsInstance(holdings, records.Holdings)

    @responses.activate
    def test_alma_get_holding(self):
        self.buildResponses()
        holding_data = self.api.get_holding(
            9922405930001552,
            22115858660001551)
        with open('test/hold.dat', 'r') as dat:
            self.assertEqual(holding_data, json.loads(dat.read()))

    @responses.activate
    def test_alma_holding(self):
        self.buildResponses()
        holding = self.api.holding(9922405930001552, 22115858660001551)
        self.assertIsInstance(holding, records.Holding)

    @responses.activate
    def test_alma_get_items(self):
        self.buildResponses()
        items_data = self.api.get_items(99100383900121, 2221159990000121)
        with open('test/items.dat', 'r') as dat:
            self.assertEqual(items_data, json.loads(dat.read()))

    @responses.activate
    def test_alma_items(self):
        self.buildResponses()
        items = self.api.items(99100383900121, 2221159990000121)
        self.assertIsInstance(items, records.Items)

    @responses.activate
    def test_alma_get_item(self):
        self.buildResponses()
        item_data = self.api.get_item(
            9922405930001552,
            22115858660001551,
            23115858650001551)
        with open('test/item.dat', 'r') as dat:
            self.assertEqual(item_data, json.loads(dat.read()))

    @responses.activate
    def test_alma_item(self):
        self.buildResponses()
        item = self.api.item(
            9922405930001552,
            22115858660001551,
            23115858650001551)
        self.assertIsInstance(item, records.Item)

    @responses.activate
    def test_alma_get_bib_requests(self):
        self.buildResponses()
        bib_requests_data = self.api.get_bib_requests(9922405930001552)
        with open('test/request.dat', 'r') as dat:
            self.assertEqual(bib_requests_data, json.loads(dat.read()))

    @responses.activate
    def test_alma_get_item_requests(self):
        self.buildResponses()
        item_requests_data = self.api.get_item_requests(9922405930001552,
                                                        22115858660001551,
                                                        23115858650001551)
        with open('test/request.dat', 'r') as dat:
            self.assertEqual(item_requests_data, json.loads(dat.read()))

    @responses.activate
    def test_alma_get_bib_booking_availability(self):
        self.buildResponses()
        bib_booking_availability_data = self.api.get_bib_booking_availability(
            9922405930001552)
        with open('test/availability.dat', 'r') as dat:
            self.assertEqual(
                bib_booking_availability_data, json.loads(dat.read()))

    @responses.activate
    def test_alma_get_item_booking_availability(self):
        self.buildResponses()
        item_booking_availability_data = \
            self.api.get_item_booking_availability(9922405930001552,
                                                   22115858660001551,
                                                   23115858650001551)
        with open('test/availability.dat', 'r') as dat:
            self.assertEqual(
                item_booking_availability_data,
                json.loads(
                    dat.read()))


class TestAlmaPUTRequests(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.api = alma.Alma(apikey='unreal', region='EU')

    def buildResponses(self):

        def echo_body(request):
            return (200, {}, request.body)

        # bib mock response
        biburl = self.api.baseurl + r'bibs/\d+$'
        bib_re = re.compile(biburl)
        responses.add_callback(
            responses.PUT, bib_re,
            callback=echo_body,
            content_type='application/json',
        )

        # holding mock response
        holdurl = self.api.baseurl + r'bibs/\d+/holdings/\d+$'
        hold_re = re.compile(holdurl)
        responses.add_callback(
            responses.PUT, hold_re,
            callback=echo_body,
            content_type='application/json',
        )

        # item mock response
        itemurl = self.api.baseurl + r'bibs/\d+/holdings/\d+/items/\d+$'
        item_re = re.compile(itemurl)
        responses.add_callback(
            responses.PUT, item_re,
            callback=echo_body,
            content_type='application/json',
        )

        # bib_request mock response
        bib_requesturl = self.api.baseurl + r'bibs/\d+/requests/\d+$'
        bib_request_re = re.compile(bib_requesturl)
        responses.add_callback(
            responses.PUT, bib_request_re,
            callback=echo_body,
            content_type='application/json'
        )

        # item_request mock response
        item_requesturl = self.api.baseurl + r'bibs/\d+/holdings/\d+/items/\d+/requests/\d+$'
        item_request_re = re.compile(item_requesturl)
        responses.add_callback(
            responses.PUT, item_request_re,
            callback=echo_body,
            content_type='application/json',
        )

    @responses.activate
    def test_alma_put_bib(self):
        self.buildResponses()
        with open('test/bib2.dat', 'r') as dat:
            original_bib = dat.read()
            returned_bib = self.api.put_bib(9922405930001552, original_bib)
            self.assertEqual(len(responses.calls), 1)
            self.assertEqual(returned_bib, json.loads(original_bib))

    @responses.activate
    def test_alma_put_holding(self):
        self.buildResponses()
        with open('test/hold2.dat', 'r') as dat:
            original_holding = dat.read()
            returned_holding = self.api.put_holding(9922405930001552,
                                                    22115858660001551,
                                                    original_holding)
            self.assertEqual(len(responses.calls), 1)
            self.assertEqual(returned_holding, json.loads(original_holding))

    @responses.activate
    def test_alma_put_item(self):
        self.buildResponses()
        with open('test/item2.dat', 'r') as dat:
            original_item = dat.read()
            returned_item = self.api.put_item(99110223950001020,
                                              22344156400001021,
                                              23344156380001021,
                                              original_item)
            self.assertEqual(len(responses.calls), 1)
            self.assertEqual(returned_item, json.loads(original_item))

    @responses.activate
    def test_alma_put_bib_request(self):
        self.buildResponses()
        with open('test/request.dat', 'r') as dat:
            original_bib_request = dat.read()
            returned_bib_request = self.api.put_bib_request(9922405930001552,
                                                            83013520000121,
                                                            original_bib_request)
            self.assertEqual(len(responses.calls), 1)
            self.assertEqual(returned_bib_request, json.loads(original_bib_request))

    @responses.activate
    def test_alma_put_item_request(self):
        self.buildResponses()
        with open('test/request.dat', 'r') as dat:
            original_item_request = dat.read()
            returned_item_request = self.api.put_item_request(9922405930001552,
                                                              22115858660001551,
                                                              23115858650001551,
                                                              83013520000121,
                                                              original_item_request)
            self.assertEqual(len(responses.calls), 1)
            self.assertEqual(returned_item_request, json.loads(original_item_request))


class TestAlmaPOSTRequests(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.api = alma.Alma(apikey='unreal', region='EU')

    def buildResponses(self):

        def echo_body(request):
            return (200, {}, request.body)

        # bib_request mock responses
        bib_requesturl = self.api.baseurl + r'bibs/\d+/requests$'
        bib_request_re = re.compile(bib_requesturl)
        responses.add_callback(
            responses.POST, bib_request_re,
            callback=echo_body,
            content_type='application/json',
        )

        with open('test/request.dat', 'r') as r:
            responses.add(responses.POST, bib_request_re,
                          status=200,
                          content_type='application/json',
                          body=r.read())

        #item_request mock responses
        item_requesturl = self.api.baseurl + r'bibs/\d+/holdings/\d+/items/\d+/requests$'
        item_request_re = re.compile(item_requesturl)
        responses.add_callback(
            responses.POST, item_request_re,
            callback=echo_body,
            content_type='application/json',
        )

        with open('test/request.dat', 'r') as r:
            responses.add(responses.POST, item_request_re,
                          status=200,
                          content_type='application/json',
                          body=r.read())

        #loan mock responses
        loanurl = self.api.baseurl + r'bibs/\d+/holdings/\d+/items/\d+/loans'
        loan_re = re.compile(loanurl)
        responses.add_callback(
            responses.POST, loan_re,
            callback=echo_body,
            content_type='application/json',
        )
        
        with open('test/item_loan.dat', 'r') as r:
            responses.add(responses.POST, loan_re,
                          status=200,
                          content_type='application/json',
                          body=r.read())
                
    @responses.activate
    def test_alma_post_bib_request(self):
        self.buildResponses()
        with open ('test/request2.dat', 'r') as dat:
            original_bib_request = dat.read()
            returned_bib_request = self.api.post_bib_request(9922405930001552,
                                                            original_bib_request)
            self.assertEqual(len(responses.calls), 1)
            self.assertEqual(returned_bib_request, json.loads(original_bib_request))
        
        with open('test/request.dat', 'r') as dat:
            bib_request_return = dat.read()
            bib_request_response = self.api.post_bib_request(9922405930001552,
                                                            bib_request_return)
            self.assertEqual(bib_request_response, json.loads(bib_request_return))

    @responses.activate
    def test_alma_post_item_request(self):
        self.buildResponses()
        with open ('test/request2.dat', 'r') as dat:
            original_item_request = dat.read()
            returned_item_request = self.api.post_item_request(9922405930001552,
                                                              22115858660001551,
                                                              23115858650001551,
                                                              original_item_request)
            self.assertEqual(len(responses.calls), 1)
            self.assertEqual(returned_item_request, json.loads(original_item_request))

        with open('test/request.dat', 'r') as dat:
            item_request_return = dat.read()
            item_request_response = self.api.post_item_request(9922405930001552,
                                                              22115858660001551,
                                                              23115858650001551,
                                                              item_request_return)
            self.assertEqual(item_request_response, json.loads(item_request_return))

    @responses.activate
    def test_alma_post_loan(self):
        self.buildResponses()
        with open ('test/loan.dat', 'r') as dat:
            original_loan = dat.read()
            returned_loan = self.api.post_loan(9922405930001552,
                                              22115858660001551,
                                              23115858650001551,
                                              original_loan)
            self.assertEqual(len(responses.calls), 1)
            self.assertEqual(returned_loan, json.loads(original_loan))

        with open('test/item_loan.dat', 'r') as dat:
            loan_return = dat.read()
            loan_response = self.api.post_loan(9922405930001552,
                                              22115858660001551,
                                              23115858650001551,
                                              loan_return)
            self.assertEqual(loan_response, json.loads(loan_return))


class TestAlmaDELETERequests(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.api = alma.Alma(apikey='unreal', region='EU')

    def buildResponses(self):

        # bib_request mock response
        bib_requesturl = self.api.baseurl + r'bibs/\d+/requests/\d+$'
        bib_request_re = re.compile(bib_requesturl)
        responses.add(responses.DELETE, bib_request_re, body='', status=204,)

        #item_request mock response
        item_requesturl = self.api.baseurl + r'bibs/\d+/holdings/\d+/items/\d+/requests/\d+$'
        item_request_re = re.compile(item_requesturl)
        responses.add(responses.DELETE, item_request_re, body='', status=204,)

    @responses.activate
    def test_alma_delete_bib_request(self):
        self.buildResponses()
        expected = ''
        bib_request_response = self.api.del_bib_request(9922405930001552,
                                                        83013520000121,)
        self.assertEqual(expected, bib_request_response)

    @responses.activate
    def test_alma_delete_item_request(self):
        self.buildResponses()
        expected = ''
        item_request_response = self.api.del_item_request(9922405930001552,
                                                          22115858660001551,
                                                          23115858650001551,
                                                          83013520000121,)
        self.assertEqual(expected, item_request_response)

if __name__ == '__main__':
    unittest.main()
