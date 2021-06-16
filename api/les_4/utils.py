import os

import requests


def create_dir_for_img(path=__file__):
    """Create dir if not exists. Return path for images."""
    root = os.path.dirname(path)
    new_path = os.path.join(root, "image")
    os.makedirs(new_path, exist_ok=True)
    return new_path


def download_img(dir_name, img_title, url):
    """The function downloads images."""
    response = requests.get(url, verify=False)
    response.raise_for_status()
    with open(os.path.join(dir_name, img_title), "wb") as file:
        file.write(response.content)
