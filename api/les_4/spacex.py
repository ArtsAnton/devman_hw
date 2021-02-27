import logging
import os

import requests


logger = logging.getLogger(__file__)


def create_dir_for_img():
    """Create dir if not exists. Return path for images."""
    root = os.path.dirname(__file__)
    new_path = os.path.join(root, 'image')
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    return new_path


def get_links_last_launch(url):
    """The function returns a list of links (links for image) from the last spacex launch."""
    response = requests.get(url)
    response.raise_for_status()
    launch_data = response.json()
    list_img = launch_data['links']['flickr']['original']
    return list_img


def download_img(dir_name, img_title, url_dl):
    """The function downloads images."""
    response = requests.get(url_dl, verify=False)
    response.raise_for_status()
    with open(os.path.join(dir_name, img_title), 'wb') as file:
        file.write(response.content)


def main():
    url_spacex = 'https://api.spacexdata.com/v4/launches/latest'
    dir_img = create_dir_for_img()

    try:
        spacex_links = get_links_last_launch(url_spacex)
        for value, img_link in enumerate(spacex_links):
            img_title = f"spacex_{value+1}.jpg"
            download_img(dir_img, img_title, img_link)

    except requests.HTTPError as error:
        logger.exception(error)


if __name__ == '__main__':
    main()
