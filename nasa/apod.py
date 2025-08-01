"""
APOD: Astronomical Picture of the Day
"https://api.nasa.gov/planetary/apod"

"""
import os
import json

import requests

from .config import (
    API_KEY,
    API_BASE,
)


APOD_BASE_URL = API_BASE +  "/planetary/apod"

def get_NASA_APOD_info(
    start_date=None,
    end_date=None,
):
    """Gets NASA Astronomy Picture of Day (APOD) Information.
    
    Parameters
    ----------
    start_date: str
        The start of a date range, when requesting date for a range of dates.
        Format: YYYY-MM-DD

    end_date: str
        The end of the date range, when used with start_date.
        Format: YYYY-MM-DD
    
    api_key: str
        The api_key to use when sending requests
    """
    params = {"api_key": API_KEY}
    if start_date is not None and end_date is not None:
        params.update(
            {
                "start_date": start_date,
                "end_date": end_date,
            }
        )
    r = requests.get(APOD_BASE_URL, params=params)
    result = r.json()
    return result

def get_and_save_NASO_APOD_info(
    start_date,
    end_date,
    filepath,
    ):
    info = get_NASA_APOD_info(
        start_date=start_date,
        end_date=end_date,
        )
    print(info)
    with open(filepath, "w") as f:
        json.dump(info, f, indent=4)


def get_APOD_image_url(data: dict):
    hdurl = data.get("hdurl", None)
    if hdurl is None:
        return data.get("url", None)
    else:
        return hdurl


def download_APOD_image(image_url, parent_path, filename=None):
    r = requests.get(image_url)
    extension = image_url.split("/")[-1].split(".")[-1]
    if filename is None:
        filename = image_url.spllit("/")[-1].split(".")[0]
    filepath = os.path.join(parent_path, f"{filename}.{extension}")
    with open(filepath, "wb") as f:
        f.write(r.content)