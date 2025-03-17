## Windowing Table Valued Fucntions(TVF)s
Windows are central to processing infinite streams. 
Windows split the stream into “buckets” of finite size, over which you can apply computations. 
This document focuses on how windowing is performed in Confluent Cloud for Apache Flink and how you can benefit from windowed functions.

Flink provides several window table-valued functions (TVF) to divide the elements of your table into windows, including:

Tumble Windows
Hop Windows
Cumulate Windows
Session Windows

These are frequently-used computations based on windowing TVF:

Window Aggregation
Window TopN
Window Join
Window Deduplication

Before running the queries given below, change the catalog and database to \`Use examples \` and \`Use marketplace\` respectively.
This would ensure that you do not need to write the fully qualified table name (catalog.database.table) every time

## Tumble
The TUMBLE function assigns each element to a window of specified window size. 
Tumbling windows have a fixed size and do not overlap.
For example, suppose you specify a tumbling window with a size of 5 minutes. 
In that case, Flink will evaluate the current window, and a new window started every five minutes.

### Return All rows

SELECT *
   FROM \`orders\`;

### Return all rows in the orders table in 10-minute tumbling windows
SELECT * FROM TABLE(
   TUMBLE(TABLE \`orders\`, DESCRIPTOR($rowtime), INTERVAL \'10\' MINUTES))

### Apply aggregation on the tumbling windowed table
SELECT window_start, window_end, SUM(\`price\`) as \`sum\`
  FROM TABLE(
    TUMBLE(TABLE \`orders\`, DESCRIPTOR($rowtime), INTERVAL \'10\' MINUTES))
  GROUP BY window_start, window_end;

