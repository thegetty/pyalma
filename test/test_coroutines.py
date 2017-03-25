import json
import os
from importlib import reload

from pyalma import alma

import asyncio
import aiohttp
import asynctest
from aioresponses import aioresponses

from datetime import datetime


def setUpModule():
    os.environ['ALMA_API_KEY'] = 'my fake key'
    os.environ['ALMA_API_REGION'] = 'APAC'
    reload(alma)


class TestAsyncRequests(asynctest.TestCase):

    maxDiff = None

    def setUp(self):
        self.api = alma.Alma(apikey='unreal', region='US')

    def test_cor_run(self):
        loop = asyncio.get_event_loop()
        ids = {'mms_id': 9922405930001552}
        url = self.api.fullurl('bib', ids)
        fh = open('test/bib.dat', 'r')
        body = fh.read()
        fh.close()
        # session = aiohttp.ClientSession()
        with aioresponses() as m:
            m.get(url,
                   status=200,
                   content_type='application/json',
                   body=body)
            resp = loop.run_until_complete(self.api.cor_run('GET', 'bib', [{'ids': ids, 'data':None}], accept='json'))
            data = resp[0][2]
            self.assertEqual(data, json.loads(body))

    def test_cor_request(self):
        loop = asyncio.get_event_loop()
        ids = {'mms_id': 9922405930001552}
        url = self.api.fullurl('bib', ids)
        fh = open('test/bib.dat', 'r')
        body = fh.read()
        fh.close()
        session = aiohttp.ClientSession()
        # creating a session outside of a coroutine is not advised
        # and throws a warning.
        # but I could not figure out another way
        with aioresponses() as m:
            m.get(url,
                  status=200,
                  content_type='application/json',
                  body=body)
            resp = loop.run_until_complete(self.api.cor_request('GET', 'bib', ids, session, accept='json'))
            data = resp[2]
            self.assertEqual(data, json.loads(body))
        session.close()

    '''
    Below test is not working because searching the long list of
    mock objects slows it down so much that the program becomes too slow
    to test the semaphore limit
    '''

    # def test_semaphore(self):
    #     self.api.max_calls = 100000
    #     self.semaphore_limit = 2
    #     ids = {'mms_id': 9922405930001552}
    #     ids_in = {'ids': {'mms_id': 9922405930001552}, 'data': None}
    #     ids_list = [ids_in] * 100
    #     url = self.api.fullurl('bib', ids)
    #     fh = open('test/bib.dat', 'r')
    #     body = fh.read()
    #     fh.close()
    #     with aioresponses() as m:
    #         for i in enumerate(ids_list):
    #             m.get(url,
    #                   status=200,
    #                   content_type='application/json',
    #                   body=body)
    #         begin = datetime.now()
    #         resp = self.api.cor_get_bib(ids_list)
    #         end = datetime.now()
    #         time_to_finish = (end - begin).total_seconds()
    #         items_finished = len(resp)
    #     print(self.api.max_calls)
    #     print(items_finished/time_to_finish)
    #     self.assertTrue(self.api.max_calls >= items_finished/time_to_finish)

    def test_rate_limit(self):
        self.api.max_calls = 20
        # self.semaphore_limit = 500
        ids = {'mms_id': 9922405930001552}
        ids_in = {'ids': {'mms_id': 9922405930001552}, 'data': None}
        ids_list = [ids_in] * 40
        url = self.api.fullurl('bib', ids)
        fh = open('test/bib.dat', 'r')
        body = fh.read()
        fh.close()
        with aioresponses() as m:
            for i in enumerate(ids_list):
                m.get(url,
                      status=200,
                      content_type='application/json',
                      body=body)
            begin = datetime.now()
            resp = self.api.cor_get_bib(ids_list)
            end = datetime.now()
            time_to_finish = (end - begin).total_seconds()
            items_finished = len(resp)
        self.assertTrue(self.api.max_calls >= items_finished/time_to_finish)


    def test_cor_get_bib(self):
        ids = {'mms_id': 9922405930001552}
        url = self.api.fullurl('bib', ids)
        fh = open('test/bib.dat', 'r')
        body = fh.read()
        fh.close()
        # session = aiohttp.ClientSession()
        with aioresponses() as m:
            m.get(url,
                  status=200,
                  content_type='application/json',
                  body=body)
            resp = self.api.cor_get_bib([{'ids':ids,'data':None}])
            bib = resp[0][2]
            self.assertEqual(bib, json.loads(body))

    def test_cor_get_holdings(self):
        ids = {'mms_id': 99100383900121}
        url = self.api.fullurl('holdings', ids)
        fh = open('test/holds.dat', 'r')
        body = fh.read()
        fh.close()
        # session = aiohttp.ClientSession()
        with aioresponses() as m:
            m.get(url,
                  status=200,
                  content_type='application/json',
                  body=body)
            resp = self.api.cor_get_holdings([{'ids':ids,'data':None}])
            holdings = resp[0][2]
            self.assertEqual(holdings, json.loads(body))

    def test_cor_get_holding(self):
        ids = {'mms_id': 9922405930001552, 'holding_id': 22115858660001551}
        url = self.api.fullurl('holding', ids)
        fh = open('test/hold.dat', 'r')
        body = fh.read()
        fh.close()
        # session = aiohttp.ClientSession()
        with aioresponses() as m:
            m.get(url,
                  status=200,
                  content_type='application/json',
                  body=body)
            resp = self.api.cor_get_holding([{'ids':ids,'data':None}])
            holding_data = resp[0][2]
            self.assertEqual(holding_data, json.loads(body))

    def test_cor_get_items(self):
        ids = {'mms_id': 9922405930001552, 'holding_id': 22115858660001551}
        url = self.api.fullurl('items', ids)
        fh = open('test/items.dat', 'r')
        body = fh.read()
        fh.close()
        # session = aiohttp.ClientSession()
        with aioresponses() as m:
            m.get(url,
                  status=200,
                  content_type='application/json',
                  body=body)
            resp = self.api.cor_get_items([{'ids': ids, 'data':None}])
            items_data = resp[0][2]
            self.assertEqual(items_data, json.loads(body))

    def test_cor_get_bib_requests(self):
        ids = {'mms_id': 9922405930001552}
        url = self.api.fullurl('bib_requests', ids)
        fh = open('test/request.dat', 'r')
        body = fh.read()
        fh.close()
        # session = aiohttp.ClientSession()
        with aioresponses() as m:
            m.get(url,
                  status=200,
                  content_type='application/json',
                  body=body)
            resp = self.api.cor_get_bib_requests([{'ids': ids, 'data':None}])
            bib_requests_data = resp[0][2]
            self.assertEqual(bib_requests_data, json.loads(body))

    def test_cor_get_item_requests(self):
        ids = {'mms_id': 9922405930001552, 'holding_id': 22115858660001551, 'item_pid': 23115858650001551}
        url = self.api.fullurl('item_requests', ids)
        fh = open('test/request.dat', 'r')
        body = fh.read()
        fh.close()
        # session = aiohttp.ClientSession()
        with aioresponses() as m:
            m.get(url,
                  status=200,
                  content_type='application/json',
                  body=body)
            resp = self.api.cor_get_item_requests([{'ids': ids, 'data':None}])
            item_requests_data = resp[0][2]
            self.assertEqual(item_requests_data, json.loads(body))

    def test_cor_put_bib(self):
        ids = {'mms_id': 9922405930001552}
        url = self.api.fullurl('bib', ids)
        fh = open('test/bib2.dat', 'r')
        original_bib = fh.read()
        fh.close()
        # session = aiohttp.ClientSession()
        with aioresponses() as m:
            m.put(url,
                  status=200,
                  content_type='application/xml',
                  body=original_bib)
            resp = self.api.cor_put_bib([{'ids': ids, 'data': original_bib}])
            returned_bib = resp[0][2]
            self.assertEqual(original_bib, returned_bib)

    def test_cor_put_holding(self):
        ids = {'mms_id': 9922405930001552, 'holding_id': 22115858660001551}
        url = self.api.fullurl('holding', ids)
        fh = open('test/hold2.dat', 'r')
        original_holding = fh.read()
        fh.close()
        # session = aiohttp.ClientSession()
        with aioresponses() as m:
            m.put(url,
                  status=200,
                  content_type='application/xml',
                  body=original_holding)
            resp = self.api.cor_put_holding([{'ids': ids, 'data': original_holding}])
            returned_holding = resp[0][2]
            self.assertEqual(original_holding, returned_holding)

    def test_cor_put_item(self):
        ids = {'mms_id': 99110223950001020, 'holding_id': 22344156400001021, 'item_pid': 23344156380001021}
        url = self.api.fullurl('item', ids)
        fh = open('test/item2.dat', 'r')
        original_item = fh.read()
        fh.close()
        # session = aiohttp.ClientSession()
        with aioresponses() as m:
            m.put(url,
                  status=200,
                  content_type='application/xml',
                  body=original_item)
            resp = self.api.cor_put_item([{'ids': ids, 'data': original_item}])
            returned_item = resp[0][2]
            self.assertEqual(original_item, returned_item)

    def test_cor_del_bib_request(self):
        ids = {'mms_id': 9922405930001552, 'request_id': 83013520000121}
        url = self.api.fullurl('bib_request', ids)
        with aioresponses() as m:
            m.delete(url,
                     status=200,
                     content_type='application/xml',
                     body='')
            expected = ''
            resp = self.api.cor_del_bib_request([{'ids': ids, 'data': None}])
            bib_request_response = resp[0][2]
            self.assertEqual(expected, bib_request_response)

    def test_cor_del_item_request(self):
        ids = {'mms_id': 9922405930001552, 'holding_id': 22115858660001551, 'item_pid': 23115858650001551, 'request_id': 83013520000121}
        url = self.api.fullurl('item_request', ids)
        with aioresponses() as m:
            m.delete(url,
                     status=200,
                     content_type='application/xml',
                     body='')
            expected = ''
            resp = self.api.cor_del_item_request([{'ids': ids, 'data': None}])
            item_request_response = resp[0][2]
            self.assertEqual(expected, item_request_response)

if __name__ == '__main__':
    asynctest.main()
