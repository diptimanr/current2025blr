### Aggregations
Compute a single result from multiple input rows in a table.

Like most data systems, Apache Flink® supports aggregate functions. 
An aggregate function computes a single result from multiple input rows. 
For example, there are aggregates to compute the COUNT, SUM, AVG (average), MAX (maximum) and MIN (minimum) values over a set of rows.

Before running the queries given below, change the catalog and database to \`Use examples \` and \`Use marketplace\` respectively.
This would ensure that you do not need to write the fully qualified table name (catalog.database.table) every time

1. SELECT COUNT(\*) AS \`order_count\` FROM \`orders\`; -- notice how the COUNT(*) increases with time
2. SELECT COUNT(\*) AS \`order_count\` \
   FROM \`orders\` \
   GROUP BY \`order_id\`;
3. 
