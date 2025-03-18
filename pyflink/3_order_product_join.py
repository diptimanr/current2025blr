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
              'changelog.mode' = 'append',
              'connector' = 'faker',
              'fields.customer_id.expression' = '#{Number.numberBetween ''3000'',''3250''}',
              'fields.order_id.expression' = '#{Internet.UUID}',
              'fields.price.expression' = '#{Number.randomDouble ''2'',''10'',''100''}',
              'fields.product_id.expression' = '#{Number.numberBetween ''1000'',''1500''}',
              'fields.log_time.expression' =  '#{date.past ''15'',''5'',''SECONDS''}',
              'rows-per-second' = '50'
            )
        """

    products_ddl = """
            CREATE TABLE `products` (
              `product_id` VARCHAR(2147483647) NOT NULL,
              `name` VARCHAR(2147483647) NOT NULL,
              `brand` VARCHAR(2147483647) NOT NULL,
              `vendor` VARCHAR(2147483647) NOT NULL,
              `department` VARCHAR(2147483647) NOT NULL,
              CONSTRAINT `PK_product_id` PRIMARY KEY (`product_id`) NOT ENFORCED
            )
            WITH (
              'changelog.mode' = 'append',
              'connector' = 'faker',
              'fields.brand.expression' = '#{Commerce.brand}',
              'fields.department.expression' = '#{Commerce.department}',
              'fields.name.expression' = '#{Commerce.productName}',
              'fields.product_id.expression' = '#{Number.numberBetween ''1000'',''1500''}',
              'fields.vendor.expression' = '#{Commerce.vendor}',
              'rows-per-second' = '50'
            )
        """

    order_product_equi_join = """
        SELECT o.order_id, o.customer_id, p.name, p.brand
        FROM orders o
        INNER JOIN products p
        ON o.product_id = p.product_id;
    """

    tenv.execute_sql(orders_ddl)
    tenv.execute_sql(products_ddl)
    tenv.execute_sql(order_product_equi_join).print()

if __name__ == '__main__':
    main()

