import sqlite3
from .dbconnection import DBConnection

class SqliteDBConnection(DBConnection):
	def __init__(self):
		super().__init__(sqlite3)
