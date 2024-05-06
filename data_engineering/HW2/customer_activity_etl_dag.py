from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.exceptions import AirflowException
import pandas as pd
import os
import yaml


# Setting basic path
base_path = os.path.dirname(os.path.abspath(__file__))

# Loading configuration from yaml file
config_path = os.path.join(base_path, 'config.yaml')
if not os.path.exists(config_path):
    raise AirflowException(f"Configuration file does not exist at {config_path}")

with open(config_path, 'r') as file:
    config = yaml.safe_load(file)

# Setting paths relative to the location of the current script
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(BASE_PATH, config['data_path'])
date_today = datetime.now().strftime('%Y-%m-01')
output_path = os.path.join(BASE_PATH, config['output_folder'], config['output_name']+date_today+'.'+config['output_exe'])
transform_module = config['transform_module']
transform_function = config['transform_function']

# Checking for a transformation script
transform_script_path = os.path.join(BASE_PATH, f"{transform_module}")
if not os.path.exists(transform_script_path):
    raise AirflowException(f"Transformation script {transform_module} not found.")

# Dynamic import of the transformation function
from scripts.transform_script import transfrom as transform

def extract_data():
    """Extract data ensuring the data file exists."""
    if not os.path.exists(data_path):
        raise AirflowException(f"Source data file does not exist at {data_path}")
    return pd.read_csv(data_path)

def transform_product_data(product, **kwargs):
    ti = kwargs['ti']
    data = ti.xcom_pull(task_ids='extract_data')
    product_data = data.filter(regex=f'sum_{product}|count_{product}|id|date')
    print("data columns:", product_data.columns)
    result = transform(product_data, date_today, product)
    return result

def load_data(**kwargs):
    """Load data into the specified output directory and handle write errors."""
    results = []
    for product_num in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']:
        data = kwargs['ti'].xcom_pull(task_ids=f'transform_{product_num}')
        results.append(data)
    final_result = pd.concat(results)
    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))
    try:
        final_result.to_csv(output_path, mode='a', header=False, index=False)

    except Exception as e:
        raise AirflowException(f"Failed to write data to {output_path}: {str(e)}")

with DAG('kate_chuiko_customer_activity_etl_parallel',
         start_date=datetime(2023, 10, 5),
         schedule_interval='0 0 5 * *',
         catchup=False) as dag:

    extract_task = PythonOperator(
        task_id='extract_data',
        python_callable=extract_data
    )

    transform_tasks = []
    for product in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']:
        task = PythonOperator(
            task_id=f'transform_{product}',
            python_callable=transform_product_data,
            op_kwargs={'product': product},
            provide_context=True
        )
        extract_task >> task
        transform_tasks.append(task)

    load_task = PythonOperator(
        task_id='load_data',
        python_callable=load_data,
        provide_context=True
    )

    for task in transform_tasks:
        task >> load_task
