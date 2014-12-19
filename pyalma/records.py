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
	pass

class Request(Record):
	
	def __init__(self, data={}):
		super().__init__('request', data)

	@property
	def user_primary_id(self):
		return self.data.get('user_primary_id')

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
	def pickup_location_circulation_desk(self):
		return self.data.get('pickup_location_circulation_desk')

	@property
	def target_destination(self):
		return self.data.get('target_destination')

	@property
	def material_type(self):
		return self.data.get('material_type')

	@property
	def last_interest_date(self):
		return self.data.get('last_interest_date')

	@property
	def partial_digitization(self):
		return self.data.get('partial_digitization')

	@property
	def request_status(self):
		return self.data.get('request_status')

	@property
	def place_in_queue(self):
		return self.data.get('place_in_queue')

	@property
	def request_date(self):
		return self.data.get('request_date')

	@property
	def task_name(self):
		return self.data.get('task_name')

	@property
	def expiry_date(self):
		return self.data.get('expiry_date')

	@property
	def booking_start_date(self):
		return self.data.get('booking_start_date')

	@property
	def booking_end_date(self):
		return self.data.get('booking_end_date')

	@property
	def adjusted_booking_start_date(self):
		return self.data.get('adjusted_booking_start_date')

	@property
	def adjusted_booking_end_date(self):
		return self.data.get('adjusted_booking_end_date')

class Availability(Record):

	def __init__(self, data={}):
		super().__init__('availability', data)

	@property
	def from_time(self):
		return self.data.get('from_time')

	@property
	def to_time(self):
		return self.data.get('to_time')

	@property
	def user_id(self):
		return self.data.get('user_id')

	@property
	def user_full_name(self):
		return self.data.get('user_full_name')

	@property
	def reason(self):
		return self.data.get('reason')


	
	



