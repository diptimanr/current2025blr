Flink supports complex and flexible join operations over dynamic tables. 
There are a number of different types of joins to account for the wide variety of semantics that queries may require.

For streaming queries, the grammar of regular joins is the most flexible and enables any kind of updates (insert, update, delete) on the input table. 
But this operation has important implications: it requires keeping both sides of the join input in state forever, 
so the required state for computing the query result might grow indefinitely, 
depending on the number of distinct input rows of all input tables and intermediate join results.

1. SELECT o.\`order_id\`, o.\`customer_id\`, p.\`name\`, p.\`brand\' \ -- INNER Equi-JOIN
   FROM \`orders\` o \
   INNER JOIN \`products\` p \
   ON o.\`product_id\` = p.\`product_id\`;
