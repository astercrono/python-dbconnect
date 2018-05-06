import psycopg2
from .dbconnection import DBConnection

class PostgresDBConnection(DBConnection):
	def __init__(self):
		super().__init__(psycopg2)
