Flink supports complex and flexible join operations over dynamic tables. 
There are a number of different types of joins to account for the wide variety of semantics that queries may require.

For streaming queries, the grammar of regular joins is the most flexible and enables any kind of updates (insert, update, delete) on the input table. 
But this operation has important implications: it requires keeping both sides of the join input in state forever, 
so the required state for computing the query result might grow indefinitely, 
depending on the number of distinct input rows of all input tables and intermediate join results.

Before running the queries given below, change the catalog and database to \`Use examples \` and \`Use marketplace\` respectively.
This would ensure that you do not need to write the fully qualified table name (catalog.database.table) every time

1. ### Inner Equi-join - Returns a simple Cartesian product restricted by the join condition.
   SELECT o.order_id, o.customer_id, p.name, p.brand \
   FROM orders o \
   INNER JOIN products p \
   ON o.product_id = p.product_id;
2. ### OUTER Equi-JOIN - Flink supports LEFT, RIGHT, and FULL outer joins.
   SELECT o.order_id, o.customer_id, p.name, p.brand \
   FROM orders o \
   FULL OUTER JOIN products p \
   ON o.product_id = p.product_id;
