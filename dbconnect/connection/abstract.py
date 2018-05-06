from abc import ABC, abstractmethod

class AbstractDBConnection(ABC):
	@abstractmethod
	def connect(self, connection_string):
		pass

	@abstractmethod
	def close(self):
		pass

	@abstractmethod
	def is_open(self):
		pass

	@abstractmethod
	def rollback(self):
		pass

	@abstractmethod
	def commit(self):
		pass

	@abstractmethod
	def update(self, query):
		pass

	@abstractmethod
	def select(self, query):
		pass

	@abstractmethod
	def batch_update(self, queries, notify):
		pass

	@abstractmethod
	def set_transaction_size(self, size):
		pass

	@abstractmethod
	def get_transaction_size(self):
		pass

	@abstractmethod
	def enable_commit(self):
		pass

	@abstractmethod
	def disable_commit(self):
		pass

	@abstractmethod
	def commit_enabled(self):
		pass
