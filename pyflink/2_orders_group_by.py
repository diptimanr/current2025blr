import os

from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings
from pyflink.table.expressions import col, lit
from pyflink.table.window import Tumble, Slide

def main():
    env = StreamExecutionEnvironment.get_execution_environment()
    settings = EnvironmentSettings.in_streaming_mode()
    tenv = StreamTableEnvironment.create(env, settings)

    env.add_jars("file:///Users/diptimanraichaudhuri/Downloads/flink-faker-0.5.3.jar")
    #env.add_jars("file:///<REPLACE_WITH_YOUR_FLINK_FAKER_JARFILE_PATH>/flink-faker-0.5.3.jar")

    orders_ddl = """
        CREATE TABLE `orders` (
          `order_id` VARCHAR(2147483647) NOT NULL,
          `customer_id` INT NOT NULL,
          `product_id` VARCHAR(2147483647) NOT NULL,
          `price` DOUBLE NOT NULL,
          log_time AS PROCTIME()
        )
        WITH (
          'changelog.mode' = 'upsert',
          'connector' = 'faker',
          'fields.customer_id.expression' = '#{Number.numberBetween ''3000'',''3250''}',
          'fields.order_id.expression' = '#{Internet.UUID}',
          'fields.price.expression' = '#{Number.randomDouble ''2'',''10'',''100''}',
          'fields.product_id.expression' = '#{Number.numberBetween ''1000'',''1500''}',
          'fields.log_time.expression' =  '#{date.past ''15'',''5'',''SECONDS''}',
          'rows-per-second' = '50'
        )
    """

    orders_group_by = """
        SELECT customer_id, SUM(price) AS total_sold
        FROM orders
        GROUP BY customer_id
        HAVING SUM(price) > 50
        LIMIT 10;
    """
    tenv.execute_sql(orders_ddl)
    tenv.execute_sql(orders_group_by).print()

if __name__ == '__main__':
    main()

