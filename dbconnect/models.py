import datetime

class Duration(object):
	def __init__(self, delta=datetime.timedelta(0)):
		self.delta = delta

	def add(self, dur):
		self.delta += dur.delta

	def add_new(self, dur):
		new_dur = Duration(self.delta)
		new_dur.add(dur)
		return new_dur

	def sub(self, dur):
		self.delta -= dur.delta

	def sub_new(self, dur):
		new_dur = Duration(self.delta)
		new_dur.sub(dur)
		return new_dur

	def __eq__(self, other):
		return self.delta == other.delta

	def format(self):
		duration_fields = self._calculate_duration_fields()
		hours = duration_fields[0]
		minutes = duration_fields[1]
		seconds = duration_fields[2]

		params = {"hours": hours, "minutes": minutes, "seconds": seconds}

		return "{hours}h {minutes}m {seconds}s".format(**params)

	# Only show the highest value
	def format_rounded(self, minutes_threshold=50, seconds_threshold=50):
		duration_fields = self._calculate_duration_fields()
		hours = duration_fields[0]
		minutes = duration_fields[1]
		seconds = duration_fields[2]

		if seconds > seconds_threshold:
			seconds = 0
			minutes += 1

		if minutes > minutes_threshold:
			seconds = 0
			minutes = 0
			hours += 1

		if hours > 0:
			return "{}h".format(hours)
		elif minutes > 0:
			return "{}m".format(minutes)
		else:
			return "{}s".format(seconds)

	def _calculate_duration_fields(self):
		seconds = int(self.delta.total_seconds())
		hours = int(seconds/60/60)
		minutes = int((seconds/60)-(hours*60))
		seconds = int(seconds-(minutes*60)-(hours*60*60))
		return [hours, minutes, seconds]

class TimedOperation(object):
	def __init__(self):
		self.start_time = datetime.datetime.now()
		self.end_time = datetime.datetime.now()
		self.duration = Duration()

	def start_timer(self):
		self.reset_duration()
		self.start_time = datetime.datetime.now()

	def end_timer(self, calc_duration=False):
		self.end_time = datetime.datetime.now()

		if calc_duration:
			delta = self.calc_delta()
			dur = Duration(delta)
			self.add_duration(dur)

	def calc_delta(self):
		return self.end_time - self.start_time

	def reset(self):
		self.reset_times()
		self.reset_duration()

	def reset_times(self):
		self.start_time = datetime.datetime.now()
		self.end_time = datetime.datetime.now()

	def reset_duration(self):
		self.duration = Duration()

	def add_duration(self, duration):
		self.duration.add(duration)

	def sub_duration(self, duration):
		self.duration.sub(duration)

	def add_operation(self, operation):
		self.duration.add(operation.duration)

	def sub_operation(self, operation):
		self.duration.sub(operation.duration)

class Query(object):
	def __init__(self, sql, params):
		self.sql = sql
		self.params = params

class NamedQuery(Query):
	def __init__(self, name, sql, params):
		super().__init__(sql, params)
		self.name = name

class QueryResult(TimedOperation):
	def __init__(self, query):
		super().__init__()
		self.query = query
		self.rowcount = 0
		self.rows = []

	def clear_rows(self):
		self.rows[:] = []

	def get_row(self, i):
		return self.rows[i]
	
	def get_value(self, rownum, colnum):
		return self.rows[rownum][colnum]

	def for_each(self, handler):
		for r in self.rows:
			handler(r)

	def add_count(self, count):
		self.rowcount += count

class QueryResultSet(TimedOperation):
	def __init__(self, title):
		super().__init__()
		self.title = title
		self.total_count = 0
		self.results = []

	def add_result(self, r):
		self.results.append(r)
		self.total_count += r.rowcount
		self.add_operation(r)

	def add_results(self, new_results):
		self.results.extend(new_results)

		for r in new_results:
			self.total_count += r.rowcount
			self.add_operation(r)

	def first(self):
		return self.get(0)

	def get(self, i):
		return self.results[i]

	def length(self):
		return len(self.results)

	def last(self):
		return self.get(self.length()-1)
