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

    clicks_ddl = """
        CREATE TABLE `clicks` (
          `click_id` VARCHAR(2147483647) NOT NULL,
          `user_id` INT NOT NULL,
          `url` VARCHAR(2147483647) NOT NULL,
          `user_agent` VARCHAR(2147483647) NOT NULL,
          `view_time` INT NOT NULL
        )
        WITH (
          'changelog.mode' = 'append',
          'connector' = 'faker',
          'fields.click_id.expression' = '#{Internet.UUID}',
          'fields.url.expression' = '#{regexify ''https://www[.]acme[.]com/product/[a-z]{5}''}',
          'fields.user_agent.expression' = '#{Internet.UserAgent}',
          'fields.user_id.expression' = '#{Number.numberBetween ''3000'',''5000''}',
          'fields.view_time.expression' = '#{Number.numberBetween ''10'',''120''}',
          'rows-per-second' = '50'
        )
    """

    clicks_select_all = """
        SELECT * FROM clicks LIMIT 5;
    """
    tenv.execute_sql(clicks_ddl)
    tenv.execute_sql(clicks_select_all).print()

if __name__ == '__main__':
    main()

