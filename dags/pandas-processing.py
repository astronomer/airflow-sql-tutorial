from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.hooks.snowflake_hook import SnowflakeHook
from plugins.operators.s3_to_snowflake_operator import S3ToSnowflakeTransferOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from datetime import datetime, timedelta
import pandas as pd

filename = 'pivoted_data'
S3_CONN_ID = 'astro-s3-workshop'
BUCKET = 'astro-workshop-bucket'

def pivot_data(**kwargs):
    #Make connection to Snowflake
    hook = SnowflakeHook(snowflake_conn_id='snowflake')
    conn = hook.get_conn()

    #Define SQL query
    query = 'SELECT DATE, STATE, POSITIVE FROM STATE_DATA;'

    #Read data into pandas dataframe
    df = pd.read_sql(query, conn)

    #Pivot dataframe into new format
    pivot_df = df.pivot(index='DATE', columns='STATE', values='POSITIVE').reset_index()

    #Save dataframe to S3
    s3_hook = S3Hook(aws_conn_id=S3_CONN_ID)
    s3_hook.load_string(pivot_df.to_csv(index=False), 
                        '{0}.csv'.format(filename), 
                        bucket_name=BUCKET, 
                        replace=True)


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

with DAG('pandas_processing',
         start_date=datetime(2020, 6, 1),
         max_active_runs=1,
         schedule_interval='@daily',
         default_args=default_args,
         catchup=False
         ) as dag:

        opr_pivot_data = PythonOperator(
            task_id='pivot_data',
            python_callable=pivot_data
        )

        opr_load_data = S3ToSnowflakeTransferOperator(
            task_id='load_data',
            s3_keys=['{0}.csv'.format(filename)],
            stage='covid_stage',
            table='PIVOT_STATE_DATA',
            schema='SANDBOX_KENTEND',
            file_format='covid_csv',
            snowflake_conn_id='snowflake'
        )

        opr_pivot_data >> opr_load_data