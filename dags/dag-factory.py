from airflow import DAG
import dagfactory

dag_factory = dagfactory.DagFactory("/usr/local/airflow/include/config_file.yml")

dag_factory.clean_dags(globals())
dag_factory.generate_dags(globals())