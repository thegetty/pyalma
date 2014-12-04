from io import StringIO

import pymarc


class Bib(object):

	def __init__(self, data=None, api=None, mms_id=None):
		self._api = api
		if data is not None:
			self.load(data)
		elif mms_id is not None:
			self.mms_id = mms_id
			self.load()

	def load(self, data=None):
		if data is None:
			res = self._api.request('GET', 'bib', ids={'mms_id':self.mms_id})
			data = res.json()
		for field, value in data.items():
			if field == 'anies':
				self.parse_marc(value[0])
			elif field == 'holdings':
				self.holdingslink = value['link']
			else:
				setattr(self, field, value)

	def parse_marc(self, marcxml):
		handler = pymarc.XmlHandler()
		stream = StringIO(marcxml)
		pymarc.parse_xml(stream, handler)
		self.marc = handler.records[0]
