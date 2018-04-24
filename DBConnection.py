import abc

class DBConnection(object):
	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def connect(self, connection_string):
		pass

	@abc.abstractmethod
	def close(self):
		pass
	
	@abc.abstractmethod
	def is_open(self):
		pass

	@abc.abstractmethod
	def rollback(self):
		pass

	@abc.abstractmethod
	def commit(self):
		pass

	@abc.abstractmethod
	def update(self, query):
		pass

	@abc.abstractmethod
	def select(self, query):
		pass

	@abc.abstractmethod
	def batch_update(self, queries, notify):
		pass

	@abc.abstractmethod
	def set_transaction_size(self, size):
		pass

	@abc.abstractmethod
	def get_transaction_size(self):
		pass

	@abc.abstractmethod
	def enable_commit(self):
		pass

	@abc.abstractmethod
	def disable_commit(self):
		pass
	
	@abc.abstractmethod
	def commit_enabled(self):
		pass