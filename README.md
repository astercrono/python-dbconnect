**Overview**

A light abstraction layer for database connections that wraps up modules that utilize the dbapi interface.

Build a connection from one of the supported drivers, construct a query object with parameters and then execute it with the connection. When a connection executes a query, it returns a result object that contains row count and duration.

This library is useful for situations where it is desirable to track stats on queries. For example, for a bulk overnight database job that runs multiple queries, it is useful to track affected row counts and how long each query ran for. These stats are helpful for understanding performance bottlenecks. 

**Prerequisites**

 - python3
 - pip
 - virtualenv

**Building**

```bash
make init
make test
```

**Usage**

Import the required modules:

```python
from dbconnect import connection, models
```

Setup a connection:

```python
conn = connection.create_connection(connection.SQLITE3_ID, ":memory:")
```

Build up a query:

```python
name = "Get_A"
sql = "select id, name from mockdata where name = ? "
params = ("A",)
query = models.NamedQuery(name, sql, params)
```

Now run the query:

```python
result = conn.select(query)
print(result)
```

Updates are supported:

```python
name = "Update_2"
sql = "update mockdata set value = 33 where name = ? "
params = ("C",)
query = models.NamedQuery(name, sql, params)
result = conn.update(query)
```

Batch updates are also supported:

```python
Query = models.Query

create_sql = "create table mockdata(id integer primary key, name text not null, value integer not null)"
insert_sql = "insert into mockdata(id, name, value) values (?, ?, ?)"

queries = []
queries.append(Query(create_sql, ()))
queries.append(Query(insert_sql, (0, "A", 3)))
queries.append(Query(insert_sql, (1, "A", 2)))
queries.append(Query(insert_sql, (2, "B", 6)))
queries.append(Query(insert_sql, (3, "B", 5)))
queries.append(Query(insert_sql, (4, "C", 9)))

conn.batch_update(queries, lambda res, num, c: None)
```
