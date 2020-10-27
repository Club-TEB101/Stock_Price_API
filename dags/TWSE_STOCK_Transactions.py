from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.operators.python_operator import PythonOperator
#from airflow.operators.sensors import ExternalTaskSensor
import pendulum

from TWSE_STOCK.FetchTWSEprice_Check_update import latestcheck

local_tz = pendulum.timezone("Asia/Taipei")


def branch_func(**kwargs):
    ti = kwargs['ti']
    xcom_value = ti.xcom_pull(key='update', task_ids='TWSE_update_check')
    print(xcom_value)
    if xcom_value == True:
        print('continue...')
        return 'continue_task'
    else:
        print('STOP!!')
        return 'stop_task'

def push(**kwargs):
    """Pushes an XCom without a specific target"""
    year=datetime.today().date().year
    month=datetime.today().date().month
    kwargs['ti'].xcom_push(key='update', value=latestcheck(year, month))



default_args = {
    'owner': 'Airflow',
    'depends_on_past': False,
    'email': ['jimmyyang886@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2020, 10, 15 ,14, 0, tzinfo=local_tz),
    'provide_context': True
}

dag = DAG('TWSE_Transactions_MySQL', description='Fetch TWSE to MySQL',
          default_args=default_args,
          schedule_interval='0 16 * * *',
          catchup=False,)
          #schedule_interval='@daily',)

start_op = PythonOperator(
    task_id='TWSE_update_check',
    dag=dag,
    python_callable=push,
)

branch_op = BranchPythonOperator(
    task_id='branch_task',
    provide_context=True,
    python_callable=branch_func,
    dag=dag)

continue_op = DummyOperator(task_id='continue_task', dag=dag)
stop_op = DummyOperator(task_id='stop_task', dag=dag)


#start = DummyOperator(task_id='start', dag=dag)
end  = DummyOperator(task_id='end', dag=dag)

TWSE_Fetch_OP = BashOperator(task_id='TWSE_FETCH_task', 
        bash_command='/home/spark/PycharmProjects/Stock_Price_API/FetchTWSEprice_daily.sh ', dag=dag)

TWSE_Import_OP = BashOperator(task_id='TWSE_import_task', 
        bash_command='/home/spark/PycharmProjects/Stock_Price_API/ImportTWSEprice_daily.sh ', dag=dag)

proxymysql_OP = BashOperator(task_id='proxy_update_task', 
        bash_command='/home/spark/PycharmProjects/Proxy2mySQL/proxy_get.sh ', dag=dag)

proxymysql_start_OP = BashOperator(task_id='proxy_update_addcron_task', 
        bash_command='/home/spark/PycharmProjects/Proxy2mySQL/proxy_get_addcron.sh ', dag=dag)

proxymysql_stop_OP = BashOperator(task_id='proxy_update_rmcron_task', 
        bash_command='/home/spark/PycharmProjects/Proxy2mySQL/proxy_get_rmcron.sh ', dag=dag,
        trigger_rule='none_skipped')

start_op >>  branch_op >> [stop_op, continue_op]
continue_op  >>  [TWSE_Fetch_OP, proxymysql_start_OP, proxymysql_OP]
#start >> [TWSE_Fetch_OP, proxymysql_start_OP, proxymysql_OP]
TWSE_Fetch_OP >> [TWSE_Import_OP, proxymysql_stop_OP] >> end 
stop_op >> end
