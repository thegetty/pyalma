import os
# external imports
import requests
# internal import
from . import records

# imports for coroutines
import asyncio
import aiohttp
from aiohttp import ClientSession, web, errors
import time
from ratelimiter import RateLimiter


__version__ = '0.1.0'
__api_version__ = 'v1'
__apikey__ = os.getenv('ALMA_API_KEY')
__region__ = os.getenv('ALMA_API_REGION')
__circ_desk__ = os.getenv('ALMA_API_CIRC_DESK')
__library__ = os.getenv('ALMA_API_LIBRARY')

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
    'loan': 'bibs/{mms_id}/holdings/{holding_id}/items/{item_pid}/loans',
    'requested_resources': 'task-lists/requested-resources'
}

MAX_CALLS_PER_SEC = 25
SEMAPHORE_LIM = 500

class Alma(object):

    def __init__(self, apikey=__apikey__, region=__region__):
        if apikey is None:
            raise Exception("Please supply an API key")
        if region not in ENDPOINTS:
            msg = 'Invalid Region. Must be one of {}'.format(list(ENDPOINTS))
            raise Exception(msg)
        self.apikey = apikey
        self.endpoint = ENDPOINTS[region]
        self.max_calls = MAX_CALLS_PER_SEC
        self.semaphore_limit = SEMAPHORE_LIM

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

    def request(self, httpmethod, resource, ids={}, params={}, data=None,
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

    def get_bib(self, mms_id, accept='xml'):
        response = self.request('GET', 'bib', {'mms_id': mms_id},
                                accept=accept)
        return self.extract_content(response)

    def put_bib(self, mms_id, data, content_type='xml', accept='xml'):
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

    def get_requested_resources(self, library=__library__,
            circ_desk = __circ_desk__):
        params = {'library': library, 'circ_desk': circ_desk}
        response = self.request('GET', 'requested_resources', params=params)
        return self.extract_content(response)

    '''
    Below are coroutine methods.
    Note that they currently all default to xml input and output,
    for ease of use in receiving data in a GET and sending it back as a PUT.
    '''

    async def cor_request(self, httpmethod, resource, ids, session, params={},
                              data=None, accept='xml', content_type=None, max_attempts=5):
        """
        Asynchronous request method
        Uses session.request, an aiohttp method

        To set rate limit:
        - max_attempts is the maximum number of times you want to repeat a
        call before giving up.
        - set maximum calls per second in global variable MAX_CALLS_PER_SEC
        """
        attempts_left = max_attempts
        rate_limiter = RateLimiter(max_calls=self.max_calls,
                                   period=(6-attempts_left),
                                   callback=self.cor_limited)

        async with session.request(method=httpmethod,
                                   headers=self.headers(accept='xml', content_type='xml'),
                                   url=self.fullurl(resource, ids),
                                   params=params,
                                   data=data) as response:
            try:
                try:
                    ctype = response.headers['Content-Type']
                except:
                    ctype = ''
                status = response.status
                method = response.method
                url = response.url_obj
                async with rate_limiter:
                    response.raise_for_status()
                if 'json' in ctype:
                    body = await response.json()
                else:
                    body = await response.text(encoding='utf-8')
                return (ids, status, body)
            except aiohttp.errors.HttpProcessingError:
                body = await response.text()
                msg = "\nError in {} \n  HTTP Status: {}\n  Method: {}\n  URL: {}\n  Response: {}".format(ids, status, method, url, body)

                if status == 429:
                    attempts_left -= 1
                    if attempts_left < 0:
                        print(msg)
                        return (ids, status, msg)
                    else:
                        until = time.time() + (rate_limiter.period)
                        asyncio.ensure_future(self.cor_limited(until))
                        await asyncio.sleep(rate_limiter.period)
                        async with rate_limiter:
                            result = await self.cor_request(httpmethod, resource, ids, session, params=params, data=data, accept=accept, content_type=content_type, max_attempts=attempts_left)
                            return result
                else:
                    return (ids, status, msg)


    async def cor_bound_request(self, sem, httpmethod, resource, ids, session, params={},
                                data=None, accept='xml', content_type='xml'):
        """
        Bounds request, so that no more than x connections can be
        open at once (set inside self.cor_run)
        """
        async with sem:
            request = await self.cor_request(httpmethod, resource, ids, session, data=data, accept=accept, content_type=content_type)
            return request

    async def cor_limited(self, until):
        """
        Rate limits calls to the server (set in cor_run)
        """
        duration = int(round(until - time.time()))
        print("Rate limited, sleeping for {:d} seconds".format(duration))

    async def cor_run(self, httpmethod, resource, input_params, accept='xml', content_type=None):
        """
        Takes a list of input_params, makes requests, returns responses
        """
        tasks = []

        # set the simultaneous connection limit here
        sem = asyncio.Semaphore(self.semaphore_limit)

        # set the rate limit here
        rate_limiter = RateLimiter(max_calls=self.max_calls,
                                   period=1,
                                   callback=self.cor_limited)

        async with ClientSession() as session:
            for input_param in input_params:

                task = asyncio.ensure_future(self.cor_bound_request(sem,
                                                                    httpmethod,
                                                                    resource,
                                                                    input_param['ids'],
                                                                    session,
                                                                    data=input_param['data'],
                                                                    accept=accept,
                                                                    content_type=content_type))
                # create a delay of between calls
                # to help prevent API rate errors
                await asyncio.sleep(1/self.max_calls)
                tasks.append(task)
            async with rate_limiter:
                responses = await asyncio.gather(*tasks)
            return responses

    """
    Each of the below asynchronous methods takes input_params as a variable,
    and returns a list of tuples.

    input_params is a list of dictionaries in the following form:
        [{
            'data': data,
            'ids':  {
                    'mms_id': mms_id,
                    'holding_id': holding_id,
                    'item_pid': item_pid,
                    'request_id': request_id
                    }
          },
          ...
          ]

    Returns a list of tuples in form
        [(ids, status, response),
        ...
        ]
    """

    def cor_get_bib(self, input_params, accept='xml'):
        # input_params includes mms_id
        loop = asyncio.get_event_loop()
        try:
            responses = loop.run_until_complete(self.cor_run('GET',
                                                             'bib',
                                                             input_params,
                                                             accept=accept))
        finally:
            loop.close()
        return responses

    def cor_put_bib(self, input_params, content_type='xml', accept='xml'):
        # input_params includes mms_id, data
        loop = asyncio.get_event_loop()
        try:
            responses = loop.run_until_complete(self.cor_run('PUT',
                                                             'bib',
                                                             input_params,
                                                             content_type=content_type,
                                                             accept=accept))
        finally:
            loop.close()
        return responses

    def cor_get_holdings(self, input_params, accept='xml'):
        # input_params includes mms_id
        loop = asyncio.get_event_loop()
        try:
            responses = loop.run_until_complete(self.cor_run('GET',
                                                             'holdings',
                                                             input_params,
                                                             accept=accept))
        finally:
            loop.close()
        return responses

    def cor_get_holding(self, input_params, accept='xml'):
        # input_params includes mms_id, holding_id
        loop = asyncio.get_event_loop()
        try:
            responses = loop.run_until_complete(self.cor_run('GET',
                                                             'holding',
                                                             input_params,
                                                             accept=accept))
        finally:
            loop.close()
        return responses

    def cor_put_holding(self, input_params, content_type='xml',
                    accept='xml'):
        # input_params includes mms_id, holding_id, data
        loop = asyncio.get_event_loop()
        try:
            responses = loop.run_until_complete(self.cor_run('PUT',
                                                             'holding',
                                                             input_params,
                                                             content_type=content_type,
                                                             accept=accept))
        finally:
            loop.close()
        return responses

    def cor_get_items(self, input_params, accept='xml'):
        # input_params includes mms_id, holding_id
        loop = asyncio.get_event_loop()
        try:
            responses = loop.run_until_complete(self.cor_run('GET',
                                                             'items',
                                                             input_params,
                                                             accept=accept))
        finally:
            loop.close()
        return responses

    def cor_get_item(self, input_params, accept='xml'):
        # input_params includes mms_id, holding_id, item_pid
        loop = asyncio.get_event_loop()
        try:
            responses = loop.run_until_complete(self.cor_run('GET',
                                                             'item',
                                                             input_params,
                                                             accept=accept))
        finally:
            loop.close()
        return responses

    def cor_put_item(self, input_params, content_type='xml',
                 accept='xml'):
        # input_params includes mms_id, holding_id, item_pid, data
        loop = asyncio.get_event_loop()
        try:
            responses = loop.run_until_complete(self.cor_run('PUT',
                                                             'item',
                                                             input_params,
                                                             content_type=content_type,
                                                             accept=accept))
        finally:
            loop.close()
        return responses



    def cor_get_bib_requests(self, input_params, accept='xml'):
        # input_params includes mms_id
        loop = asyncio.get_event_loop()
        try:
            responses = loop.run_until_complete(self.cor_run('GET',
                                                             'bib_requests',
                                                             input_params,
                                                             accept=accept))
        finally:
            loop.close()
        return responses

    def cor_get_item_requests(self, input_params, accept='xml'):
        # input_params includes mms_id, holding_id, item_pid
        loop = asyncio.get_event_loop()
        try:
            responses = loop.run_until_complete(self.cor_run('GET',
                                                             'item_requests',
                                                             input_params,
                                                             accept=accept))
        finally:
            loop.close()
        return responses

    def cor_del_item_request(self, input_params):
        # input_params includes mms_id, holding_id, item_pid, request_id
        loop = asyncio.get_event_loop()
        try:
            responses = loop.run_until_complete(self.cor_run('DELETE',
                                                             'item_request',
                                                             input_params))
        finally:
            loop.close()
        return responses

    def cor_del_bib_request(self, input_params):
        # input_params includes mms_id, request_id
        loop = asyncio.get_event_loop()
        try:
            responses = loop.run_until_complete(self.cor_run('DELETE',
                                                             'bib_request',
                                                             input_params))
        finally:
            loop.close()
        return responses

    '''
    WARNING: below methods have not been fully implemented or
    been tested.  To be complete, tehse methods will require the
    appropriate query strings parameters to be passed into session.request
    within self.cor_request, which has not yet been implemented.
    '''
    def cor_del_item(self, input_params):
        pass

    def cor_post_loan(self, input_params,
                  content_type='xml', accept='xml'):
        # input_params includes mms_id, holding_id, item_pid, data
        loop = asyncio.get_event_loop()
        try:
            responses = loop.run_until_complete(self.cor_run('POST',
                                                             'loan',
                                                             input_params,
                                                             content_type=content_type,
                                                             accept=accept))
        finally:
            loop.close()
        return responses

    def cor_post_bib_request(self, input_params,
                         content_type='xml', accept='xml'):
        # input_params includes mms_id, data
        loop = asyncio.get_event_loop()
        try:
            responses = loop.run_until_complete(self.cor_run('POST',
                                                             'bib_requests',
                                                             input_params,
                                                             content_type=content_type,
                                                             accept=accept))
        finally:
            loop.close()
        return responses

    def cor_post_item_request(self, input_params,
                          content_type='xml', accept='xml'):
        # input_params includes mms_id, holding_id, item_pid, data
        loop = asyncio.get_event_loop()
        try:
            responses = loop.run_until_complete(self.cor_run('POST',
                                                             'item_requests',
                                                             input_params,
                                                             content_type=content_type,
                                                             accept=accept))
        finally:
            loop.close()
        return responses

    def cor_put_bib_request(self, input_params,
                            content_type='xml', accept='xml'):
        # input_params includes mms_id, request_id, data
        loop = asyncio.get_event_loop()
        try:
            responses = loop.run_until_complete(self.cor_run('PUT',
                                                             'bib_request',
                                                             input_params,
                                                             content_type=content_type,
                                                             accept=accept))
        finally:
            loop.close()
        return responses

    def cor_put_item_request(self, input_params,
                             content_type='xml', accept='xml'):
        # input_params includes mms_id, holding_id, item_pid, request_id, data
        loop = asyncio.get_event_loop()
        try:
            responses = loop.run_until_complete(self.cor_run('PUT',
                                                             'item_request',
                                                             input_params,
                                                             content_type=content_type,
                                                             accept=accept))
        finally:
            loop.close()
        return responses

    def cor_get_bib_booking_availability(self, input_params, accept='xml'):
        # input_params includes mms_id
        loop = asyncio.get_event_loop()
        try:
            responses = loop.run_until_complete(self.cor_run('GET',
                                                             'bib_booking_availability',
                                                             input_params,
                                                             accept=accept))
        finally:
            loop.close()
        return responses

    def cor_get_item_booking_availability(
            self, input_params, accept='xml'):
        # input_params includes mms_id, holding_id, item_pid
        loop = asyncio.get_event_loop()
        try:
            responses = loop.run_until_complete(self.cor_run('GET',
                                                             'item_booking_availability',
                                                             input_params,
                                                             accept=accept))
        finally:
            loop.close()
        return responses

    def cor_get_digreps(self, input_params, accept='json'):
        pass

    def cor_get_digrep(self, input_params, accept='json'):
        pass

    def cor_post_digrep(self, input_params, content_type='json', accept='json'):
        pass

    def cor_del_digrep(self, input_params, rep_id):
        pass

class HTTPError(Exception):

    def __init__(self, response):
        super().__init__(self.msg(response))

    def msg(self, response):
        msg = "\n  HTTP Status: {}\n  Method: {}\n  URL: {}\n  Response: {}"
        return msg.format(response.status_code, response.request.method,
                          response.url, response.text)
