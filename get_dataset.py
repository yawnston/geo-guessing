from io import BytesIO
import re
import requests
import os
from os.path import isfile, join
from pathlib import Path

from typing import Optional
from grid import SQUARES
from settings import _ROOT_DIR, SETTINGS


def get_street_view_image(location: str) -> Optional[BytesIO]:
    meta_params = {
        "location": location,
        "key": SETTINGS.google_api_key,
        "radius": "5000",
    }
    meta_response = requests.get(url=SETTINGS.maps_metadata_url, params=meta_params)

    if meta_response.json()["status"] != "OK":
        return None

    img_params = {
        "location": location,
        "key": SETTINGS.google_api_key,
        "size": "640x640",
        "radius": "5000",
    }
    img_response = requests.get(url=SETTINGS.maps_image_url, params=img_params)

    if not img_response.ok:
        return None

    img = BytesIO(img_response.content)
    return img


def save_image_to_file(image: BytesIO, folder: str, train=True) -> None:
    type_folder = "data" if train else "valdata"
    folder_path = _ROOT_DIR / type_folder / folder
    Path.mkdir(folder_path, exist_ok=True, parents=True)

    folder_files = [f for f in os.listdir(folder_path) if isfile(join(folder_path, f))]
    if len(folder_files) == 0:
        new_file_name = "000001.jpg"
    else:
        max_file_number = max(
            [int(re.search(r"(\d{6})\.jpg", x).group(1)) for x in folder_files]
        )

        new_file_number = max_file_number + 1
        new_file_name = str(new_file_number).rjust(6, "0") + ".jpg"

    with open(folder_path / new_file_name, "wb") as out_img:
        out_img.write(image.getbuffer())


if __name__ == "__main__":
    for square in SQUARES:
        square_points = square.sample_points(1)
        for point in square_points:
            img = get_street_view_image(f"{point[0]}, {point[1]}")
            if img:
                save_image_to_file(img, f"{square.id}", train=True)
