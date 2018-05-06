def import_sqlite():
	from .sqlite import SqliteDBConnection
	return SqliteDBConnection

def import_postgres():
	from .postgres import PostgresDBConnection
	return PostgresDBConnection

SQLITE3_ID = "SQLITE3"
POSTGRESQL_ID = "POSTGRESQL"

CONNECTION_MAPPER = {
	SQLITE3_ID: import_sqlite,
	POSTGRESQL_ID: import_postgres
}

def create_connection(connection_id, connection_string):
	connection = CONNECTION_MAPPER.get(connection_id)()
	print(connection)
	if connection is not None:
		return connection().connect(connection_string)
	return connection
