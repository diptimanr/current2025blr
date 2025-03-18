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

### Return all rows in the orders table in 15-seconds tumbling windows

SELECT * FROM TABLE( \
     TUMBLE(TABLE \`orders\`, DESCRIPTOR($rowtime), INTERVAL \'15\' SECONDS));

### Apply aggregation on the tumbling windowed table
### Compute the sum of the price column in the orders table within 15-seconds tumbling windows.

SELECT window_start, window_end, SUM(\`price\`) as \`sum\` \
  FROM TABLE( \
      TUMBLE(TABLE \`orders\`, DESCRIPTOR($rowtime), INTERVAL \'15\' SECONDS)) \
  GROUP BY window_start, window_end;


## Hop
The HOP function assigns elements to windows of fixed length. 
Like a TUMBLE windowing function, the size of the windows is configured by the window size parameter. 
An additional window slide parameter controls how frequently a hopping window is started. 
Hence, hopping windows can be overlapping if the slide is smaller than the window size. 
In this case, elements are assigned to multiple windows. 
Hopping windows are also known as “sliding windows”.

### Return all rows in the orders table in hopping windows with a 5 seconds slide and 30 seconds size.

SELECT * FROM TABLE( \
  HOP(TABLE \`orders\`, DESCRIPTOR($rowtime), INTERVAL '5' SECONDS, INTERVAL '30' SECONDS))

### Apply aggregation on the hopping windowed table
### Computes the sum of the price column in the orders table within hopping windows that have a 5-seconds slide and 30-seconds size.

SELECT window_start, window_end, SUM(price) as `hop_sum` \
  FROM TABLE( \
      HOP(TABLE \`orders\`, DESCRIPTOR($rowtime), INTERVAL '5' SECONDS, INTERVAL '30' SECONDS)) \
  GROUP BY window_start, window_end;


## Session
The SESSION function groups elements by sessions of activity. 
Unlike TUMBLE and HOP windows, session windows do not overlap and do not have a fixed start and end time. 
Instead, a session window closes when it doesn’t receive elements for a certain period of time, i.e., when a gap of inactivity occurs. 
A session window is configured with a static session gap that defines the duration of inactivity. 
When this period expires, the current session closes and subsequent elements are assigned to a new session window.

For example, you could have windows with a gap of 1 minute. 
With this configuration, when the interval between two events is less than 1 minute, these events will be grouped into the same session window. 
If there is no data for 1 minute following the latest event, then this session window will close and be sent downstream. 
Subsequent events will be assigned to a new session window.

### Returns all columns from the orders table within SESSION windows that have a 30-seconds gap, partitioned by product_id:

SELECT * FROM TABLE( \
  SESSION(TABLE \`orders\` PARTITION BY product_id, DESCRIPTOR($rowtime), INTERVAL '30' SECONDS));

### Compute the sum of the price column in the orders table within SESSION windows that have a 30-seconds gap.

SELECT window_start, window_end, customer_id, SUM(price) as `session_sum` \
  FROM TABLE( \
      SESSION(TABLE \`orders\` PARTITION BY customer_id, DESCRIPTOR($rowtime), INTERVAL '30' SECONDS)) \
  GROUP BY window_start, window_end, customer_id;



