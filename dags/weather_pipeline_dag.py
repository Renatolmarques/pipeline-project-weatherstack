# -*- coding: utf-8 -*-

# --- Essential Imports ---
from __future__ import annotations
import pendulum
from datetime import timedelta

from airflow.models.dag import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

# --- Default Arguments ---
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

# The absolute path to your project directory on your Mac.
# Ensure this path is correct for your machine.
HOST_PROJECT_PATH = "/Users/amarante/Documents/Pessoal/Cursos/Projetos/projeto-tempo/repos/weather-data-project"

# --- DAG Definition ---
with DAG(
    dag_id='weather_data_pipeline_docker',
    default_args=default_args,
    description='Full ETL pipeline using DockerOperator.',
    schedule='@daily',
    start_date=pendulum.datetime(2025, 7, 16, tz="UTC"),
    catchup=False,
    tags=['weather', 'pipeline', 'docker'],
) as dag:

    # --- Task Definitions ---

    # Task 1: Runs the Python script using an official Python image.
    task_extract_load = DockerOperator(
        task_id='run_python_load_script',
        # Use a standard, official Python image.
        image='python:3.9-slim',
        # The command is now a multi-line bash command.
        # It first installs required libraries, then runs the script.
        command=[
            "bash", "-c",
            "pip install psycopg2-binary requests && python api-request/insert_records.py"
        ],
        # Connects this task's container to our project's network.
        network_mode='weather-data-project_default',
        # Mounts the project directory into the container.
        mounts=[Mount(source=HOST_PROJECT_PATH, target='/app', type='bind')],
        # Sets the working directory inside the container.
        working_dir='/app',
        docker_url="unix://var/run/docker.sock",
        auto_remove=True
    )

     # Task 2: Runs dbt models inside the official dbt container.
    task_transform_dbt = DockerOperator(
        task_id='run_dbt_models',
        image='ghcr.io/dbt-labs/dbt-postgres:1.8.1',
        # The command to run all dbt models.
        command='dbt run',
        
        # ADD THIS LINE to override the image's default entrypoint
        entrypoint='',

        network_mode='weather-data-project_default',
        environment={
            'DBT_USER': 'db_user',
            'DBT_PASSWORD': 'db_password'
        },
        mounts=[
            Mount(source=HOST_PROJECT_PATH, target='/app', type='bind'),
            Mount(source=f"{HOST_PROJECT_PATH}/dbt/profiles", target='/root/.dbt', type='bind')
        ],
        working_dir='/app/dbt/weather_dw',
        docker_url="unix://var/run/docker.sock",
        auto_remove=True
    )

    # Defines the dependency.
    task_extract_load >> task_transform_dbt