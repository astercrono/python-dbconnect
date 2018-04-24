import PostgresDBConnection
import DBConnectionType

ConnectionMapper = {
	DBConnectionType.POSTGRESQL: PostgresDBConnection.create
}

def create(connection_type, connection_string):
	connector = ConnectionMapper.get(connection_type)

	if connector is not None:
		return connector().connect(connection_string)