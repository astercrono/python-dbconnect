from .sqlite import SqliteDBConnection
from .postgres import PostgresDBConnection

SQLITE3_ID = "SQLITE3"
POSTGRESQL_ID = "SQLITE3"

CONNECTION_MAPPER = {
	SQLITE3_ID: SqliteDBConnection,
	POSTGRESQL_ID: PostgresDBConnection
}

def create_connection(connection_id, connection_string):
	connection = CONNECTION_MAPPER.get(connection_id)
	if connection is not None:
		return connection().connect(connection_string)
	return connection
