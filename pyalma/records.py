from io import StringIO

import pymarc


class Record(object):

	def __init__(self, rectype, data={}):
		self._rectype = rectype
		self.load(data)

	def load(self, data):
		self.data = {}
		for field, value in data.items():
			if field == 'anies':
				self.parse_marc(value[0])
			else:
				self.data[field] = value

	def parse_marc(self, marcxml):
		handler = pymarc.XmlHandler()
		stream = StringIO(marcxml)
		pymarc.parse_xml(stream, handler)
		self.marc = handler.records[0]


class Bib(Record):

	def __init__(self, data={}):
		super().__init__('bib', data)

	@property
	def mms_id(self):
		return self.data.get('mms_id')

	@property
	def created_by(self):
		return self.data.get('created_by')

	@property
	def created_date(self):
		return self.data.get('created_date')

	@property
	def last_modified_by(self):
		return self.data.get('last_modified_by')

	@property
	def last_modified_date(self):
		return self.data.get('last_modified_date')

	@property
	def holdings_link(self):
		return self.data.get('holdings').get('link')


class Holding(Record):
	pass


class Item(Record):
	pass



