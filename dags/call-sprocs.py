from airflow import DAG
from airflow.contrib.operators.snowflake_operator import SnowflakeOperator
from datetime import datetime, timedelta


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG('call_snowflake_sprocs',
         start_date=datetime(2020, 6, 1),
         max_active_runs=3,
         schedule_interval='@daily',
         default_args=default_args,
         template_searchpath='/usr/local/airflow/include',
         catchup=False
         ) as dag:

         opr_call_sproc1 = SnowflakeOperator(
             task_id='call_sproc1',
             snowflake_conn_id='snowflake',
             sql='call-sproc1.sql'
         )
         opr_call_sproc2 = SnowflakeOperator(
             task_id='call_sproc2',
             snowflake_conn_id='snowflake',
             sql='call-sproc2.sql'
         )

         opr_call_sproc1 >> opr_call_sproc2