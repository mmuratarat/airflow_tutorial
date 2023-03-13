from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

def helloWorld():
    print('Hello World')
          
with DAG(dag_id="hello_world_dag",
         description='A simple DAG that prints "Hello, World!"',
         start_date=datetime(2023,1,1),
         schedule_interval="@hourly",
         catchup=False) as dag:
    
    task1 = PythonOperator(
        task_id="hello_world",
        python_callable=helloWorld)
    
    task1