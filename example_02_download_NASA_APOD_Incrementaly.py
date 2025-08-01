import json
import requests
import pathlib
import pendulum
import logging
import os
import shutil
import utils

from nasa import (
    get_and_save_NASO_APOD_info,
    download_APOD_image,
    get_APOD_image_url,
)


PATH = pathlib.Path("/root/airflow/dags/data/APOD/")
ARCHIVE_PATH = pathlib.Path("/root/airflow/dags/data/APOD/archive")
# d["templates_dict"] = {"start_date": "2022-11-19", "end_date": "2022-11-19", "api_key":"HLZysbeK3rb2s6SlsN5HLfh43eb6Er0qQQdLjhJN"}
# PATH = pathlib.Path("./data/")


def _build_directories():
    PATH.mkdir(parents=True, exist_ok=True)
    ARCHIVE_PATH.mkdir(parents=True, exist_ok=True)

def _get_and_save_NASO_APOD_INFO_task(
    **context
    ):
    start_date = context["templates_dict"]["start_date"]
    end_date = context["templates_dict"]["end_date"]
    logging.info(f"start_date = {start_date}")
    logging.info(f"end_date = {end_date}")
    get_and_save_NASO_APOD_info(
        start_date=start_date,
        end_date=end_date,
        filepath=f"{PATH.__str__()}/{start_date}_{end_date}.json",
    )


def _download_image(**context):
    start_date = context["templates_dict"]["start_date"]
    end_date = context["templates_dict"]["end_date"]

    with open(f"{PATH.__str__()}/{start_date}_{end_date}.json", "r") as f:
        for data in json.load(f):
                print(data)
                url = get_APOD_image_url(data)
                download_APOD_image(
                    image_url=url,
                    parent_path=PATH.__str__(),
                    filename=data["date"],
                    )
            


def archive_json_url_info(**context):
    start_date = context["templates_dict"]["start_date"]
    end_date = context["templates_dict"]["end_date"]

    utils.move_file(
        f"{PATH.__str__()}/{start_date}_{end_date}.json",
        f"{ARCHIVE_PATH.__str__()}/{start_date}_{end_date}.json",
        )
    


# =======================================================
# ==================== DAG ==============================
# =======================================================
from airflow import DAG
from airflow.operators.python import PythonOperator

dag = DAG(
    dag_id="download_NASA_APOD_incremental",
    start_date=pendulum.today().add(days=-50),
    schedule_interval="@daily",
)


build_directories_task = PythonOperator(
    task_id="build_directories",
    dag=dag,
    python_callable=_build_directories,
)


get_and_save_NASO_APOD_INFO_task = PythonOperator(
    task_id="download_NASA_APOD_information_inc",
    dag=dag,
    python_callable=_get_and_save_NASO_APOD_INFO_task,
    templates_dict={
        "start_date": "{{ ds }}",
        "end_date": "{{ ds  }}",
    },
)

download_image_task = PythonOperator(
    task_id="download_image_task_inc",
    dag=dag,
    python_callable=_download_image,
    templates_dict={
        "start_date": "{{ ds }}",
        "end_date": "{{ ds  }}",
    },
)


archive_json_url_info_task = PythonOperator(
    task_id="archive_json_url_info_task",
    dag=dag,
    python_callable=archive_json_url_info,
    templates_dict={
        "start_date": "{{ ds }}",
        "end_date": "{{ ds  }}",
    },
)


build_directories_task >> get_and_save_NASO_APOD_INFO_task >> download_image_task >> archive_json_url_info_task