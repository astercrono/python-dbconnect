from context import dbconnect

def mockup_data(connection):
	Query = dbconnect.models.Query

	create_sql = "create table mockdata(id integer primary key, name text not null, value integer not null)"
	insert_sql = "insert into mockdata(id, name, value) values (?, ?, ?)"
	queries = []
	queries.append(Query(create_sql, ()))
	queries.append(Query(insert_sql, (0, "A", 3)))
	queries.append(Query(insert_sql, (1, "A", 2)))
	queries.append(Query(insert_sql, (2, "B", 6)))
	queries.append(Query(insert_sql, (3, "B", 5)))
	queries.append(Query(insert_sql, (4, "C", 9)))

	connection.batch_update(queries, lambda res, num, c: None)

def setup():
	c = dbconnect.connection.create_connection(dbconnect.connection.SQLITE3_ID, ":memory:")
	mockup_data(c)
	return c

def test_select():
	connection = setup()
	try:
		name = "Get_A"
		sql = "select id, name from mockdata where name = ? "
		params = ("A",)
		query = dbconnect.models.NamedQuery(name, sql, params)

		result = connection.select(query)

		assert result.rowcount == 2
		assert len(result.rows) == result.rowcount
		assert result.query.sql == sql
		assert result.query.params == params
		assert result.query.name == name
		assert result.start_time is not None
		assert result.end_time is not None
		assert result.duration is not None
	finally:
		connection.close()

def test_update():
	connection = setup()
	try:
		name = "Update_2"
		sql = "update mockdata set value = 33 where name = ? "
		params = ("C",)
		query = dbconnect.models.NamedQuery(name, sql, params)

		result = connection.update(query)

		assert result.rowcount == 1
		assert len(result.rows) == 0
		assert result.query.sql == sql
		assert result.query.params == params
		assert result.query.name == name
		assert result.start_time is not None
		assert result.end_time is not None
		assert result.duration is not None

		check_value(connection, 4, 33)
	finally:
		connection.close()

def check_value(connection, mockid, expected_value):
	sql = "select value from mockdata where id = ?"
	params = (mockid,)
	query = dbconnect.models.Query(sql, params)

	result = connection.select(query)
	print(result.rows)
	actual_value = result.get_value(0, 0)

	assert expected_value == actual_value
