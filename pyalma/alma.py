import os
# external imports
import requests
# internal import
from pyalma.records import Bib


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


class HTTPError(Exception):
    
    def __init__(self, response):
        super().__init__(self.msg(response))

    def msg(self, response):
        msg = "\n  HTTP Status: {}\n  Method: {}\n  URL: {}\n  Response: {}"
        return  msg.format(response.status_code, response.request.method,
            response.url, response.text)

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

    def bib(self, mms_id):
        response = self.request('GET', 'bib', ids={'mms_id':mms_id})
        return Bib(response.json())