import datetime

class TimedOperation(object):
	def start_timer(self):
		self.start_time = datetime.datetime.now()

	def end_timer(self):
		self.end_time = datetime.datetime.now()

	def reset_times(self):
		self.start_time = datetime.datetime.now()
		self.end_time = datetime.datetime.now()

	def format_duration(self):
		ms = self.duration_ms()
		secs = self.duration_seconds()
		mins = self.duration_minutes()

		if mins != 0:
			return "%sm" % mins
		elif secs != 0:
			return "%sm" % secs
		else:
			return "%sms" % ms

	def duration_ms(self):
		diff = self.end_time - self.start_time
		return int((diff.seconds * 1000) + (diff.microseconds / 1000))

	def duration_seconds(self):
		return int(self.duration_ms() / 1000)

	def duration_minutes(self):
		return int(self.duration_seconds() / 60)

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

class QueryResult(TimedOperation):
	def __init__(self, query):
		self.query = query

		self.rowcount = 0
		self.rows = []

	def clear_rows(self):
		self.rows[:] = []
	
	def forEach(self, handler):
		for r in self.rows:
			handler(r)
	
	def add_count(self, count):
		self.rowcount += count

class QueryResultSet(TimedOperation):
	def __init__(self, title):
		self.title = title
		self._results = []
	
	def add_result(self, result):
		self._results.append(result)
	
	def add_results(self, results):
		self._results.extend(results)
	
	def results(self):
		return self._results
	
	def first(self):
		return self._results[0]
	
	def last(self):
		return self._results[len(self._results)-1]
	
	def total_count(self):
		count = 0

		for res in self._results:
			count += res.rowcount

		return count

def create_query(sql, params):
	return Query(sql, params)

def create_named_query(name, sql, params):
	return NamedQuery(name, sql, params)

def create_query_result(query):
	return QueryResult(query)