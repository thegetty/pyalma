import json
import os
import re
from importlib import reload
import unittest

import responses

from pyalma import alma

import asyncio
import aiohttp
import contextlib
import yarl
import asynctest
from asynctest import mock
from aioresponses import aioresponses


def setUpModule():
    os.environ['ALMA_API_KEY'] = 'my fake key'
    os.environ['ALMA_API_REGION'] = 'APAC'
    reload(alma)

# @contextlib.contextmanager
# def mock_session(response, session=None, mock_object=None):
#     """
#     :param aiohttp.ClientSession session:
#     :param aiohttp.ClientResponse|list[aiohttp.ClientResponse] response:
#     """
#     session = session or aiohttp.ClientSession()
#     request = session._request

#     session.mock = mock_object or mock.Mock()
#     if isinstance(response, (list, tuple)):
#         session.mock.side_effect = response
#     else:
#         session.mock.return_value = response

#     async def _request(*args, **kwargs):
#         return session.mock(*args, **kwargs)

#     session._request = _request

#     try:
#         yield session
#     finally:
#         session._request = request
#         delattr(session, 'mock')


# def create_response(method, url, content, loop=None):
#     loop = loop or asyncio.get_event_loop()

#     response = aiohttp.ClientResponse(method.lower(), yarl.URL(url))

#     def side_effect(*args, **kwargs):
#         fut = loop.create_future()
#         if isinstance(content, str):
#             fut.set_result(content.encode())
#         else:
#             fut.set_result(content)
#         return fut

#     response.content = mock.Mock()
#     response.status = 200
#     response.content.read.side_effect = side_effect

#     return response


class TestAsyncGETRequests(asynctest.TestCase):

    maxDiff = None

    def setUp(self):
        self.api = alma.Alma(apikey='unreal', region='EU')


    @aioresponses()
    def buildResponses(self, mocked):
        loop = asyncio.get_event_loop()
        biburl = 'https://api-na.hosted.exlibrisgroup.com/almaws/v1/bibs/9922405930001552'
        session = aiohttp.ClientSession()
        with open('test/bib.dat', 'r') as b:
            mocked.get(biburl,
                       status=200,
                       content_type='application/json',
                       body=b.read())
        resp = loop.run_until_complete(session.get(biburl))

    async def test_get_bib(self):
        self.buildResponses()
        resp = self.api.cor_get_bib([{'mms_id': 9922405930001552}])
        data = resp.json()
        bib_data = self.api.get_bib(9922405930001552)
        with open('test/bib.dat', 'r') as dat:
            self.assertEqual(bib_data, json.loads(dat.read()))


        # loop = asyncio.get_event_loop()
        # with open('test/bib.dat', 'r') as dat:
        #     b = dat.read()
        # mocked.get('https://api-na.hosted.exlibrisgroup.com/almaws/v1/bibs/9922405930001552', status=200, body=b)
        # session = aiohttp.ClientSession()
        # resp = loop.run_until_complete(session.get('https://api-na.hosted.exlibrisgroup.com/almaws/v1/bibs/9922405930001552'))
        # print(next(resp.text()))


if __name__ == '__main__':
    asynctest.main()
