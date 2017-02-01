import os
# external imports
import requests
# internal import
from . import records

# imports for coroutines
import asyncio
import aiohttp
from aiohttp import ClientSession, web

__version__ = '0.1.0'
__api_version__ = 'v1'
__apikey__ = os.getenv('ALMA_API_KEY')
__region__ = os.getenv('ALMA_API_REGION')

ENDPOINTS = {
    'US': 'https://api-na.hosted.exlibrisgroup.com',
    'EU': 'https://api-eu.hosted.exlibrisgroup.com',
    'APAC': 'https://api-ap.hosted.exlibrisgroup.com'
}

FORMATS = {
    'json': 'application/json',
    'xml': 'application/xml'
}

RESOURCES = {
    'bib': 'bibs/{mms_id}',
    'holdings': 'bibs/{mms_id}/holdings',
    'holding': 'bibs/{mms_id}/holdings/{holding_id}',
    'items': 'bibs/{mms_id}/holdings/{holding_id}/items',
    'item': 'bibs/{mms_id}/holdings/{holding_id}/items/{item_pid}',
    'bib_requests': 'bibs/{mms_id}/requests',
    'item_requests':
        'bibs/{mms_id}/holdings/{holding_id}/items/{item_pid}/requests',
    'bib_requests': 'bibs/{mms_id}/requests',
    'bib_request': 'bibs/{mms_id}/requests/{request_id}',
    'item_requests': 'bibs/{mms_id}/holdings/{holding_id}/items/{item_pid}/requests',
    'item_request': 'bibs/{mms_id}/holdings/{holding_id}/items/{item_pid}/requests/{request_id}',
    'bib_booking_availability': 'bibs/{mms_id}/booking-availability',
    'item_booking_availability':
        'bibs/{mms_id}/holdings/{holding_id}/items/' +
        '{item_pid}/booking-availability',
    'loan': 'bibs/{mms_id}/holdings/{holding_id}/items/{item_pid}/loans'
}


class Alma(object):

    def __init__(self, apikey=__apikey__, region=__region__):
        if apikey is None:
            raise Exception("Please supply an API key")
        if region not in ENDPOINTS:
            msg = 'Invalid Region. Must be one of {}'.format(list(ENDPOINTS))
            raise Exception(msg)
        self.apikey = apikey
        self.endpoint = ENDPOINTS[region]

    @property
    def baseurl(self):
        return '{}/almaws/{}/'.format(self.endpoint, __api_version__)

    def fullurl(self, resource, ids={}):
        return self.baseurl + RESOURCES[resource].format(**ids)

    def headers(self, accept='json', content_type=None):
        headers = {
            "User-Agent": "pyalma/{}".format(__version__),
            "Authorization": "apikey {}".format(self.apikey),
            "Accept": FORMATS[accept]
        }
        if content_type is not None:
            headers['Content-Type'] = FORMATS[content_type]
        return headers

    def request(self, httpmethod, resource, ids, params={}, data=None,
                accept='json', content_type=None):
        response = requests.request(
            method=httpmethod,
            headers=self.headers(accept=accept, content_type=content_type),
            url=self.fullurl(resource, ids),
            params=params,
            data=data)
        try:
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError:
            raise HTTPError(response)

    def extract_content(self, response):
        ctype = response.headers['Content-Type']
        if 'json' in ctype:
            return response.json()
        else:
            return response.content.decode('utf-8')

    '''
    Below are convenience methods that call request() and extract_content() and
    return the response data in json or xml
    '''

    def get_bib(self, mms_id, accept='json'):
        response = self.request('GET', 'bib', {'mms_id': mms_id},
                                accept=accept)
        return self.extract_content(response)

    def put_bib(self, mms_id, data, content_type='json', accept='json'):
        response = self.request('PUT', 'bib', {'mms_id': mms_id},
                                data=data, content_type=content_type, accept=accept)
        return self.extract_content(response)

    def get_holdings(self, mms_id, accept='json'):
        response = self.request('GET', 'holdings', {'mms_id': mms_id},
                                accept=accept)
        return self.extract_content(response)

    def get_holding(self, mms_id, holding_id, accept='json'):
        response = self.request('GET', 'holding',
                                {'mms_id': mms_id, 'holding_id': holding_id},
                                accept=accept)
        return self.extract_content(response)

    def put_holding(self, mms_id, holding_id, data, content_type='json',
                    accept='json'):
        response = self.request('PUT', 'holding',
                                {'mms_id': mms_id, 'holding_id': holding_id},
                                data=data, content_type=content_type, accept=accept)
        return self.extract_content(response)

    def get_items(self, mms_id, holding_id, accept='json'):
        response = self.request('GET', 'items',
                                {'mms_id': mms_id,
                                 'holding_id': holding_id},
                                accept=accept)
        return self.extract_content(response)

    def get_item(self, mms_id, holding_id, item_pid, accept='json'):
        response = self.request('GET', 'item',
                                {'mms_id': mms_id,
                                 'holding_id': holding_id,
                                 'item_pid': item_pid},
                                accept=accept)
        return self.extract_content(response)

    def put_item(self, mms_id, holding_id, item_pid, data, content_type='json',
                 accept='json'):
        response = self.request('PUT', 'item',
                                {'mms_id': mms_id,
                                 'holding_id': holding_id,
                                 'item_pid': item_pid},
                                data=data, content_type=content_type, accept=accept)
        return self.extract_content(response)

    def del_item(self, mms_id, holding_id, item_pid):
        pass

    def post_loan(self, mms_id, holding_id, item_pid, data,
                  content_type='json', accept='json'):
        response = self.request('POST', 'loan',
                                {'mms_id': mms_id,
                                 'holding_id': holding_id,
                                 'item_pid': item_pid},
                                data=data, content_type=content_type, accept=accept)
        return self.extract_content(response)

    def get_bib_requests(self, mms_id, accept='json'):
        response = self.request('GET', 'bib_requests', {'mms_id': mms_id},
                                accept=accept)
        return self.extract_content(response)

    def get_item_requests(self, mms_id, holding_id, item_pid, accept='json'):
        response = self.request('GET', 'item_requests',
                                {'mms_id': mms_id,
                                 'holding_id': holding_id,
                                 'item_pid': item_pid},
                                accept=accept)
        return self.extract_content(response)

    def post_bib_request(self, mms_id, data, content_type='json', accept='json'):
        response = self.request('POST', 'bib_requests',
                                {'mms_id': mms_id},
                                data=data, content_type=content_type, accept=accept)
        return self.extract_content(response)


    def post_item_request(self, mms_id, holding_id, item_pid, data,
                          content_type='json', accept='json'):
        response = self.request('POST', 'item_requests',
                                {'mms_id': mms_id,
                                 'holding_id': holding_id,
                                 'item_pid': item_pid},
                                 data=data, content_type=content_type, accept=accept)
        return self.extract_content(response)

    def put_bib_request(self, mms_id, request_id, data, content_type='json', accept='json'):
        response = self.request('PUT', 'bib_request',
                                {'mms_id': mms_id,
                                 'request_id': request_id},
                                  data=data, content_type=content_type, accept=accept)
        return self.extract_content(response)

    def put_item_request(self, mms_id, holding_id, item_pid, request_id,
                         data, content_type='json', accept='json'):
        response = self.request('PUT', 'item_request',
                                {'mms_id': mms_id,
                                 'holding_id': holding_id,
                                 'item_pid': item_pid,
                                 'request_id': request_id},
                                  data=data, content_type=content_type, accept=accept)
        return self.extract_content(response)

    def del_item_request(self, mms_id, holding_id, item_pid, request_id):
        response = self.request('DELETE', 'item_request',
                                            {'mms_id': mms_id,
                                             'holding_id': holding_id,
                                             'item_pid': item_pid,
                                             'request_id': request_id},)
        return self.extract_content(response)

    def del_bib_request(self, mms_id, request_id):
        response = self.request('DELETE', 'bib_request',
                                            {'mms_id': mms_id,
                                             'request_id': request_id},)
        return self.extract_content(response)

    def get_bib_booking_availability(self, mms_id, accept='json'):
        response = self.request('GET', 'bib_booking_availability',
                                {'mms_id': mms_id}, accept=accept)
        return self.extract_content(response)

    def get_item_booking_availability(
            self, mms_id, holding_id, item_pid, accept='json'):
        response = self.request('GET', 'item_booking_availability',
                                {'mms_id': mms_id,
                                 'holding_id': holding_id,
                                 'item_pid': item_pid},
                                accept=accept)
        return self.extract_content(response)

    def get_digreps(self, mms_id, accept='json'):
        pass

    def get_digrep(self, mms_id, rep_id, accept='json'):
        pass

    def post_digrep(self, mms_id, data, content_type='json', accept='json'):
        pass

    def del_digrep(self, mms_id, rep_id):
        pass

    '''
    Below are convenience methods that return Record objects instead of
    response data
    '''

    def bib(self, mms_id):
        data = self.get_bib(mms_id)
        return records.Bib(data)

    def holdings(self, mms_id):
        data = self.get_holdings(mms_id)
        return records.Holdings(data)

    def holding(self, mms_id, holding_id):
        data = self.get_holding(mms_id, holding_id)
        return records.Holding(data)

    def items(self, mms_id, holding_id=None):
        data = self.get_items(mms_id, holding_id)
        return records.Items(data)

    def item(self, mms_id, holding_id, item_pid):
        data = self.get_item(mms_id, holding_id, item_pid)
        return records.Item(data)

    '''
    Below are coroutine methods
    '''

    # general method to open request, and return content body
    async def cor_request(self, httpmethod, resource, ids, session, params={},
                              data=None, accept='json', content_type=None):
        async with session.request(method=httpmethod,
                                   headers=self.headers(accept=accept, content_type=content_type),
                                   url=self.fullurl(resource, ids),
                                   params=params,
                                   data=data) as response:
            try:
                response.raise_for_status()
                ctype = response.headers['Content-Type']
                if 'json' in ctype:
                    body = await response.json()
                else:
                    body = await response.read(encoding='utf-8')
                return body
            except:
                # this needs to be fixed to properly raise HTTPError
                # HTTPError class herein will also need to be rewritten for coro
                # the below errors will not result in coro terminating, it keeps retrying
                body = await response.text(encoding='utf-8')
                print("Raise for status failed: {}".format(body))
                pass

    # bounds request, so that no more than x connections can be
    # open at once (currently set at 1000)
    async def cor_bound_request(self, sem, httpmethod, resource, ids, session, params={},
                                data=None, accept='json', content_type=None):
        async with sem:
            request = await self.cor_request(httpmethod, resource, ids, session)
            return request

    async def cor_run(self, httpmethod, resource, mms_ids, accept='json'):
        tasks = []
        sem = asyncio.Semaphore(1000)

        # Fetch all responses within one Client session
        # keep connection alive for all requests

        async with ClientSession() as session:
            for mms_id in mms_ids:
                task = asyncio.ensure_future(self.cor_bound_request(sem,
                                                                    httpmethod,
                                                                    resource,
                                                                    {'mms_id': mms_id},
                                                                    session,
                                                                    accept=accept))
                tasks.append(task)
            responses = await asyncio.gather(*tasks)
            return responses

    # method to request a list of mms_ids asynchronously
    def get_bibs(self, mms_ids, accept='json'):
        loop = asyncio.get_event_loop()
        try:
            responses = loop.run_until_complete(self.cor_run('GET', 'bib', mms_ids))
        finally:
            loop.close()
        return responses

class HTTPError(Exception):

    def __init__(self, response):
        super().__init__(self.msg(response))

    def msg(self, response):
        msg = "\n  HTTP Status: {}\n  Method: {}\n  URL: {}\n  Response: {}"
        return msg.format(response.status_code, response.request.method,
                          response.url, response.text)
