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

	def __init__(self, data={}):
		super().__init__('holding', data)

	@property
	def holding_id(self):
		return self.data.get('holding_id')

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


class Item(Record):
	
	def __init__(self, data={}):
		super().__init__('item', data)

	@property
	def item_link(self):
		return self.data.get('link')

	@property
	def mms_id(self):
		return self.data.get('bib_data').get('mms_id')

	@property
	def title(self):
		return self.data.get('bib_data').get('title')
	
	@property
	def author(self):
		return self.data.get('bib_data').get('author')

	@property
	def issn(self):
		return self.data.get('bib_data').get('issn')
	
	@property
	def isbn(self):
		return self.data.get('bib_data').get('isbn')
	
	@property
	def complete_edition(self):
		return self.data.get('bib_data').get('complete_edition')
	
	@property
	def network_number(self):
		return self.data.get('bib_data').get('network_number')
	
	@property
	def place_of_publication(self):
		return self.data.get('bib_data').get('place_of_publication')
	
	@property
	def publisher_const(self):
		return self.data.get('bib_data').get('publisher_const')

	@property
	def bib_link(self):
		return self.data.get('bib_data').get('link')
	
	@property
	def holding_id(self):
		return self.data.get('holding_data').get('holding_id')
	
	@property
	def call_number(self):
		return self.data.get('holding_data').get('call_number')
	
	@property
	def temp_library(self):
		return self.data.get('holding_data').get('temp_library')
	
	@property
	def temp_location(self):
		return self.data.get('holding_data').get('temp_location')
	
	@property
	def temp_call_number(self):
		return self.data.get('holding_data').get('temp_call_number')
	
	@property
	def accession_number(self):
		return self.data.get('holding_data').get('accession_number')
	
	@property
	def holding_link(self):
		return self.data.get('holding_data').get('link')
	
	@property
	def pid(self):
		return self.data.get('item_data').get('pid')
	
	@property
	def barcode(self):
		return self.data.get('item_data').get('barcode')
	
	@property
	def description(self):
		return self.data.get('item_data').get('description')
	
	@property
	def physical_material_type(self):
		return self.data.get('item_data').get('physical_material_type')
	
	@property
	def process_type(self):
		return self.data.get('item_data').get('process_type')
	
	@property
	def library(self):
		return self.data.get('item_data').get('library')
	
	@property
	def location(self):
		return self.data.get('item_data').get('location')
	
	@property
	def po_line(self):
		return self.data.get('item_data').get('po_line')
	
	@property
	def arrival_date(self):
		return self.data.get('item_data').get('arrival_date')
	
	@property
	def requested(self):
		return self.data.get('item_data').get('requested')
	
	@property
	def enumeration_a(self):
		return self.data.get('item_data').get('enumeration_a')
	
	@property
	def enumeration_b(self):
		return self.data.get('item_data').get('enumeration_b')
	
	@property
	def enumeration_c(self):
		return self.data.get('item_data').get('enumeration_c')
	
	@property
	def enumeration_d(self):
		return self.data.get('item_data').get('enumeration_d')
	
	@property
	def enumeration_e(self):
		return self.data.get('item_data').get('enumeration_e')
	
	@property
	def enumeration_f(self):
		return self.data.get('item_data').get('enumeration_f')
	
	@property
	def enumeration_g(self):
		return self.data.get('item_data').get('enumeration_g')
	
	@property
	def enumeration_h(self):
		return self.data.get('item_data').get('enumeration_h')
	
	@property
	def chronology_i(self):
		return self.data.get('item_data').get('chronology_i')
	
	@property
	def chronology_j(self):
		return self.data.get('item_data').get('chronology_j')
	
	@property
	def chronology_k(self):
		return self.data.get('item_data').get('chronology_k')
	
	@property
	def chronology_l(self):
		return self.data.get('item_data').get('chronology_l')
	
	@property
	def chronology_m(self):
		return self.data.get('item_data').get('chronology_m')


class Request(Record):
	
	def __init__(self, data={}):
		super().__init__('request', data)

	@property
	def title(self):
		return self.data.get('title')

	@property
	def author(self):
		return self.data.get('author')

	@property
	def description(self):
		return self.data.get('description')

	@property
	def comment(self):
		return self.data.get('comment')

	@property
	def request_id(self):
		return self.data.get('request_id')

	@property
	def request_type(self):
		return self.data.get('request_type')

	@property
	def pickup_location(self):
		return self.data.get('pickup_location')

	@property
	def pickup_location_type(self):
		return self.data.get('pickup_location_type')

	@property
	def pickup_location_library(self):
		return self.data.get('pickup_location_library')

	@property
	def material_type_value(self):
		return self.data.get('material_type').get('value')

	@property
	def request_status(self):
		return self.data.get('request_status')

	@property
	def place_in_queue(self):
		return self.data.get('place_in_queue')

	@property
	def request_date(self):
		return self.data.get('request_date')


	
	



