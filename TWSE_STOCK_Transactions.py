from datetime import datetime
from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator


default_args = {
    'owner': 'Airflow',
    'depends_on_past': False,
    'email': ['jimmyyang886@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}
 

dag = DAG('TWSE_Transactions_MySQL', description='Fetch TWSE to MySQL',
          schedule_interval='0 14 * * *',
          start_date=datetime(2020, 10, 8), catchup=False)



TWSE_Fetch_operator = BashOperator(task_id='TWSE_FETCH_task', 
        bash_command='/home/spark/PycharmProjects/Stock_Price_API/FetchTWSEprice_daily.sh ', dag=dag)

TWSE_Import_operator = BashOperator(task_id='TWSE_import_task', 
        bash_command='/home/saprk/PycharmProjects/Stock_Price_API/ImportTWSEprice_daily.sh ', dag=dag)

TWSE_Fetch_operator >> TWSE_Import_operator  
