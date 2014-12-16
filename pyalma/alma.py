import os
# external imports
import requests
# internal import
from . import records


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
    'item': 'bibs/{mms_id}/holdings/{holding_id}/items/{item_pid}'
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
            return response.text

    '''
    Below are convenience methods that call request() and extract_content() and
    return the response data in json or xml
    '''

    def get_bib(self, mms_id, accept='json'):
        response = self.request('GET', 'bib', {'mms_id':mms_id}, accept=accept)
        return self.extract_content(response)

    def put_bib(self, mms_id, data, content_type='json', accept='json'):
        pass

    def get_holdings(self, mms_id, accept='json'):
        pass

    def get_holding(self, mms_id, holding_id, accept='json'):
        pass

    def put_holding(self, mms_id, holding_id, data, content_type='json',
                    accept='json'):
        pass

    def get_items(self, mms_id, holding_id, accept='json'):
        pass

    def get_item(self, mms_id, holding_id, item_pid, accept='json'):
        pass

    def del_item(self, mms_id, holding_id, item_pid):
        pass

    def post_loan(self, mms_id, holding_id, item_pid, data,
                  content_type='json', accept='json'):
        pass

    def get_bib_requests(self, mms_id, accept='json'):
        pass

    def get_item_requests(self, mms_id, holding_id, item_pid, accept='json'):
        pass

    def post_bib_request(self, mms_id, data, content_type='json',
                         accept='json'):
        pass

    def post_item_request(self, mms_id, holding_id, item_pid, data,
                          content_type='json', accept='json'):
        pass

    def put_item_request(self, mms_id, holding_id, item_pid, data,
                         content_type='json', accept='json'):
        pass

    def del_item_request(self, mms_id, holding_id, item_pid, request_id):
        pass

    def del_bib_request(self, mms_id, request_id):
        pass

    def get_bib_booking_availability(self, mms_id, accept='json'):
        pass

    def get_item_booking_availability(
            self, mms_id, holding_id, item_pid, accept='json'):
        pass

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
        pass

    def holding(self, mms_id, holding_id):
        pass

    def items(self, mms_id, holding_id=None):
        pass

    def item(self, mms_id, holding_id, item_pid):
        pass


class HTTPError(Exception):
    
    def __init__(self, response):
        super().__init__(self.msg(response))

    def msg(self, response):
        msg = "\n  HTTP Status: {}\n  Method: {}\n  URL: {}\n  Response: {}"
        return  msg.format(response.status_code, response.request.method,
            response.url, response.text)