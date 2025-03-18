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

    customers_ddl = """
        CREATE TABLE `customers` (
          `customer_id` INT NOT NULL,
          `name` VARCHAR(2147483647) NOT NULL,
          `address` VARCHAR(2147483647) NOT NULL,
          `postcode` VARCHAR(2147483647) NOT NULL,
          `city` VARCHAR(2147483647) NOT NULL,
          `email` VARCHAR(2147483647) NOT NULL,
          CONSTRAINT `PK_customer_id` PRIMARY KEY (`customer_id`) NOT ENFORCED
        )
        WITH (
          'changelog.mode' = 'upsert',
          'connector' = 'faker',
          'fields.address.expression' = '#{Address.streetAddress}',
          'fields.city.expression' = '#{Address.city}',
          'fields.customer_id.expression' = '#{Number.numberBetween ''3000'',''3250''}',
          'fields.email.expression' = '#{Internet.emailAddress}',
          'fields.name.expression' = '#{Name.fullName}',
          'fields.postcode.expression' = '#{Address.postcode}',
          'rows-per-second' = '50'
        )
    """

    customers_select_all = """
        SELECT * FROM customers LIMIT 5;
    """
    tenv.execute_sql(customers_ddl)
    tenv.execute_sql(customers_select_all).print()

if __name__ == '__main__':
    main()

