import Query
from DBConnection import DBConnection

class PostgresDBConnection(DBConnection):
	def __init__(self, driver):
		self.driver = driver
		self.transaction_size = 1
		self._commit_enabled = True

	def connect(self, connection_string):
		if not connection_string:
			raise TypeError("connection_string")

		self.connection_string = connection_string
		self.psyconn = self.driver.connect(connection_string)

		return self

	def close(self):
		if self.is_open() and not self.commit_enabled():
			self.rollback()
		self.psyconn.close()
	
	def is_open(self):
		if self.psyconn.closed == 0:
			return True
		else:
			return False

	def rollback(self):
		self.psyconn.rollback()

	def commit_enabled(self):
		return self._commit_enabled

	def commit(self):
		if self.commit_enabled():
			self.psyconn.commit()

	def cursor(self):
		return self.psyconn.cursor()
	
	def update(self, query):
		cursor = self.cursor()
		query_result = Query.create_query_result(query)
		sql = query.sql
		params = query.params

		try:
			query_result.start_timer()
			cursor.execute(sql, params)
			query_result.end_timer()

			query_result.rowcount = cursor.rowcount

			self.commit()
		except Exception as ex:
			self.rollback()
			raise ex
		else:
			cursor.close()
		
		return query_result

	def select(self, query):
		cursor = self.cursor()
		query_result = Query.create_query_result(query)
		sql = query.sql
		params = query.params

		try:
			query_result.start_timer()
			cursor.execute(sql, params)
			query_result.end_timer()

			query_result.rowcount = cursor.rowcount
			query_result.rows = cursor.fetchall()
		except Exception as ex:
			self.rollback()
			raise ex
		else:
			cursor.close()

		return query_result

	def batch_update(self, queries, notify):
		cursor = self.cursor()
		query_results = []

		try:
			total_count = len(queries)
			query_number = 1

			for q in queries:
				should_commit = self._should_commit_batch(total_count, query_number)

				qr = self.update(q)
				query_results.append(qr)

				if should_commit: 
					self.commit()

				if notify is not None:
					notify(qr, query_number, should_commit)

				query_number += 1
		except Exception as ex:
			self.rollback()
			raise ex
		else:
			cursor.close()
		
		return query_results
	
	def set_transaction_size(self, size):
		self.transaction_size = size

	def get_transaction_size(self):
		return self.transaction_size
	
	def enable_commit(self):
		self._commit_enabled = True

	def disable_commit(self):
		self._commit_enabled = False

	def _should_commit_batch(self, total_count, query_number):
		transaction_size = self.get_transaction_size()

		if transaction_size <= 0:
			return False
		elif query_number % transaction_size == 0:
			return True
		elif query_number >= total_count:
			return True
		else:
			return False

def create():
	import psycopg2
	return PostgresDBConnection(psycopg2)
