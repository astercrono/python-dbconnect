from ..models import QueryResult
from .abstract import AbstractDBConnection

class DBConnection(AbstractDBConnection):
	def __init__(self, driver):
		self.transaction_size = 1
		self._commit_enabled = True
		self.connection_string = None
		self.driver = driver
		self.conn = None
		self.open = False

	def connect(self, connection_string):
		self.connection_string = connection_string
		self.conn = self.driver.connect(connection_string)
		self.open = True
		return self

	def close(self):
		if self.is_open() and not self.commit_enabled():
			self.rollback()
		self.conn.close()
		self.open = False

	def is_open(self):
		return self.open

	def rollback(self):
		self.conn.rollback()

	def commit_enabled(self):
		return self._commit_enabled

	def commit(self):
		if self.commit_enabled():
			self.conn.commit()

	def cursor(self):
		return self.conn.cursor()

	def update(self, query):
		cursor = self.cursor()
		query_result = QueryResult(query)

		try:
			query_result.start_timer()
			cursor.execute(query.sql, query.params)
			query_result.end_timer(True)

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
		query_result = QueryResult(query)

		try:
			query_result.start_timer()
			cursor.execute(query.sql, query.params)
			query_result.end_timer(True)

			query_result.rows = cursor.fetchall()
			query_result.rowcount = len(query_result.rows)
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

		return False
