from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator

from datetime import datetime

def _task1(ti):
    ti.xcom_push(key = 'my_key', value = 24)

def _task2(ti):
    ti.xcom_pull(key = 'my_key', task_ids = 'task1')

def _branch(ti):
    value = ti.xcom_pull(key = 'my_key', task_ids = 'task1')
    if value == 42:
        return 'task2'
    return 'task3'

with DAG(dag_id='branching_dag', start_date=datetime(2023, 1, 1), schedule_interval='@daily', catchup=False) as dag:

    t1 = PythonOperator(task_id= 'task1', python_callable=_task1)
    branch = BranchPythonOperator(task_id = 'branch', python_callable= _branch)

    t2 = PythonOperator(task_id= 'task2', python_callable=_task2)
    t3 = BashOperator(task_id='task3', bash_command="echo ''")

    t4 = BashOperator(task_id='task4', bash_command="echo ''", trigger_rule='none_failed_min_one_success')

    t1 >> branch >> [t2, t3] >> t4