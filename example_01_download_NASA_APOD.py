import json
import requests
import pathlib
import pendulum

from nasa import (
    get_and_save_NASO_APOD_info,
    download_APOD_image,
    get_APOD_image_url,
)

PATH = pathlib.Path("/root/airflow/dags/data/APOD/")


def _build_directories():
    PATH.mkdir(parents=True, exist_ok=True)

def _get_and_save_NASO_APOD_INFO(
    start_date,
    end_date,
    ):
    get_and_save_NASO_APOD_info(
        start_date=start_date,
        end_date=end_date,
        filepath=f"{PATH.__str__()}/{start_date}_{end_date}.json",
    )


def download_image():
    p = PATH.glob('**/*')
    files = [x for x in p if x.is_file() if x.name.endswith(".json")]
    for file in files:
        with open(file, "r") as f:
            for data in json.load(f):
                print(data)
                url = get_APOD_image_url(data)
                download_APOD_image(
                    image_url=url,
                    parent_path=PATH.__str__(),
                    filename=data["date"],
                    )


# =======================================================
# ==================== DAG ==============================
# =======================================================
from airflow import DAG
from airflow.operators.python import PythonOperator

dag = DAG(
    dag_id="download_NASA_APOD",
    start_date=pendulum.today().add(days=-2),
    schedule_interval=None,
)

build_directories_task = PythonOperator(
    task_id="build_directories",
    dag=dag,
    python_callable=_build_directories,
)

get_and_save_NASO_APOD_INFO_task = PythonOperator(
    task_id="download_NASA_APOD_information",
    dag=dag,
    python_callable=_get_and_save_NASO_APOD_INFO,
    op_kwargs={
        "start_date": "2022-10-01",
        "end_date": "2022-10-25",
    }
)

download_image_task = PythonOperator(
    task_id="download_image_task",
    dag=dag,
    python_callable=download_image,
)

build_directories_task >> get_and_save_NASO_APOD_INFO_task >> download_image_task