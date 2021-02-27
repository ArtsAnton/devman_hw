import argparse
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


def get_list_img_id(url):
    """The function returns the ID of the images for the collection."""
    response = requests.get(url)
    response.raise_for_status()
    return [item['id'] for item in response.json()]


def get_link_and_extension_hb(url_template, img_id):
    """The function returns a link to a images and a images extension."""
    url = url_template.format(img_id)
    response_hubble = requests.get(url)
    response_hubble.raise_for_status()
    data = response_hubble.json()
    link_for_dl_img = f'https:{data["image_files"][-1]["file_url"]}'
    img_extension = link_for_dl_img.split('.')[-1]
    return link_for_dl_img, img_extension


def download_img(dir_name, img_title, url_dl):
    """The function downloads images."""
    response = requests.get(url_dl, verify=False)
    response.raise_for_status()
    with open(os.path.join(dir_name, img_title), 'wb') as file:
        file.write(response.content)


def main():
    parser = argparse.ArgumentParser(description='Download photos.')
    parser.add_argument('collection', help='Hubble collection.')
    args = parser.parse_args()

    url_template_hubble_img = 'http://hubblesite.org/api/v3/image/{}'
    url_template_hubble_coll = 'http://hubblesite.org/api/v3/images/{}'
    url_for_coll = url_template_hubble_coll.format(args.collection)

    dir_img = create_dir_for_img()

    try:
        hubble_img_id = get_list_img_id(url_for_coll)
        for img_id in hubble_img_id:
            img_link, ext = get_link_and_extension_hb(url_template_hubble_img, img_id)
            img_title = f"hubble_{img_id}.{ext}"
            download_img(dir_img, img_title, img_link)
    except requests.HTTPError as error:
        logger.exception(error)


if __name__ == '__main__':
    main()
