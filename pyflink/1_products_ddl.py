import os

from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings
from pyflink.table.expressions import col, lit
from pyflink.table.window import Tumble, Slide

def main():
    env = StreamExecutionEnvironment.get_execution_environment()
    settings = EnvironmentSettings.in_streaming_mode()
    tenv = StreamTableEnvironment.create(env, settings)

    #env.add_jars("file:///D:\\sw\\flink-faker-0.5.3.jar")
    env.add_jars("file:///Users/diptimanraichaudhuri/Downloads/flink-faker-0.5.3.jar")

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
          'changelog.mode' = 'upsert',
          'connector' = 'faker',
          'fields.brand.expression' = '#{Commerce.brand}',
          'fields.department.expression' = '#{Commerce.department}',
          'fields.name.expression' = '#{Commerce.productName}',
          'fields.product_id.expression' = '#{Number.numberBetween ''1000'',''1500''}',
          'fields.vendor.expression' = '#{Commerce.vendor}',
          'rows-per-second' = '50'
        )
    """

    tenv.execute_sql(products_ddl)
    tenv.execute_sql("select * from products LIMIT 5").print()

if __name__ == '__main__':
    main()

