import datetime

class Query(object):
	def __init__(self, sql, params):
		self.sql = sql
		self.params = params

		if sql is not None and params is not None:
			self.compiled_sql = sql % params

class NamedQuery(Query):
	def __init__(self, name, sql, params):
		super(NamedQuery, self).__init__(sql, params)
		self.name = name

class QueryResult(object):
	def __init__(self, query):
		self.query = query
		self.start_time = datetime.datetime.now()
		self.end_time = datetime.datetime.now()

		self.rowcount = 0
		self.rows = []

	def start_timer(self):
		self.start_time = datetime.datetime.now()

	def end_timer(self):
		self.end_time = datetime.datetime.now()

	def format_time(self):
		ms = self.timed_ms()
		secs = self.timed_seconds()
		mins = self.timed_minutes()

		if mins != 0:
			return "%sm" % mins
		elif secs != 0:
			return "%sm" % secs
		else:
			return "%sms" % ms

	def timed_ms(self):
		diff = self.end_time - self.start_time
		return int((diff.seconds * 1000) + (diff.microseconds / 1000))

	def timed_seconds(self):
		return int(self.timed_ms() / 1000)

	def timed_minutes(self):
		return int(self.timed_seconds() / 60)
	
	def clear_rows(self):
		self.rows[:] = []
	
	def reset_times(self):
		self.start_time = datetime.datetime.now()
		self.end_time = datetime.datetime.now()
	
	def forEach(self, handler):
		for r in self.rows:
			handler(r)

def create_query(sql, params):
	return Query(sql, params)

def create_named_query(name, sql, params):
	return NamedQuery(name, sql, params)

def create_query_result(query):
	return QueryResult(query)