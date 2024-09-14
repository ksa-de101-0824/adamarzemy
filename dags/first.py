from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# Default arguments for all tasks
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}


# Define the functions to be executed by the PythonOperator
def print_hello():
    print("Hello, Airflow!")


def print_goodbye():
    print("Goodbye, Airflow!")


# Define the DAG
with DAG(
    dag_id='simple_dag_example',
    default_args=default_args,
    description='A simple DAG example',
    schedule_interval=timedelta(days=1),  # Daily schedule
    start_date=datetime(2024, 9, 1),  # Start date
    end_date=datetime(2024, 9, 12), # End date
    catchup=False,  # Don't backfill missing runs
    tags=['example_1']
) as dag:

    # Task: Print "Hello, Airflow!"
    hello_task = PythonOperator(
        task_id='hello_task',  # Unique ID for the task
        python_callable=print_hello,  # Python function to execute
        provide_context=True,
    )

    goodbye_task = PythonOperator(
        task_id="goodbye_task",
        python_callable=print_goodbye,
        provide_context=True,
    )

hello_task >> goodbye_task




# with DAG(
#     dag_id='simple_dag_example',
#     default_args=default_args,
#     description='A simple DAG example',
#     schedule_interval="*/30 * * * *",  # Every 30 minutes
#     start_date=datetime(2023, 9, 1),  # Start date
#     end_date=datetime(2023, 9, 12) # End date
#     catchup=False,  # Don't backfill missing runs
#     tags=['example']
# ) as dag:

#     # Task: Print "Hello, Airflow!"
#     hello_task = PythonOperator(
#         task_id='hello_task',  # Unique ID for the task
#         python_callable=print_hello,  # Python function to execute
#         provide_context=True,
#     )

#     goodbye_task = PythonOperator(
#         task_id="goodbye_task",
#         python_callable=print_goodbye,
#         provide_context=True,
#     )


# hello_task >> goodbye_task