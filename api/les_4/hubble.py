import argparse
import logging
import os
import urllib

import requests

from utils import create_dir_for_img, download_img


logger = logging.getLogger(__file__)


def get_img_ids(url):
    """The function returns the ID of the images for the collection."""
    response = requests.get(url)
    response.raise_for_status()
    return [item['id'] for item in response.json()]


def get_img_link(url_template, img_id):
    """The function returns a link to image."""
    url = url_template.format(img_id)
    hubble_response = requests.get(url)
    hubble_response.raise_for_status()
    img_data = hubble_response.json()
    img_link = f"https:{img_data['image_files'][-1]['file_url']}"
    return img_link


def get_img_extension(link):
    """The function returns a image extension."""
    link = urllib.parse.unquote(link)
    path = urllib.parse.urlsplit(link).path
    img_mane = os.path.split(path)[1]
    img_extension = os.path.splitext(img_mane)[1]
    return img_extension


def main():
    parser = argparse.ArgumentParser(description="Download photos.")
    parser.add_argument("collection", help="Hubble collection.")
    args = parser.parse_args()

    url_template_for_img = "http://hubblesite.org/api/v3/image/{}"
    url_template_for_coll = "http://hubblesite.org/api/v3/images/{}"
    url_for_coll = url_template_for_coll.format(args.collection)

    img_dir = create_dir_for_img()

    try:
        hubble_img_ids = get_img_ids(url_for_coll)
        for img_id in hubble_img_ids:
            img_link = get_img_link(url_template_for_img, img_id)
            img_ext = get_img_extension(img_link)
            img_title = f"hubble_{img_id}{img_ext}"
            download_img(img_dir, img_title, img_link)
    except requests.HTTPError as error:
        logger.exception(error)


if __name__ == "__main__":
    main()
