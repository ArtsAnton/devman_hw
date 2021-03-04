import argparse
import logging
import os

import requests

from utils import create_dir_for_img, download_img


logger = logging.getLogger(__file__)


def get_id_imgs(url):
    """The function returns the ID of the images for the collection."""
    response = requests.get(url)
    response.raise_for_status()
    return [item['id'] for item in response.json()]


def get_link_and_extension_hb(url_template, img_id):
    """The function returns a link to a images and a images extension."""
    url = url_template.format(img_id)
    hubble_response = requests.get(url)
    hubble_response.raise_for_status()
    img_data = hubble_response.json()
    img_link = f'https:{img_data["image_files"][-1]["file_url"]}'
    img_extension = os.path.splitext(img_link)[1]
    return img_link, img_extension


def main():
    parser = argparse.ArgumentParser(description='Download photos.')
    parser.add_argument('collection', help='Hubble collection.')
    args = parser.parse_args()

    hubble_url_template_img = 'http://hubblesite.org/api/v3/image/{}'
    hubble_url_template_coll = 'http://hubblesite.org/api/v3/images/{}'
    url_for_coll = hubble_url_template_coll.format(args.collection)

    img_dir = create_dir_for_img()

    try:
        hubble_img_id = get_id_imgs(url_for_coll)
        for img_id in hubble_img_id:
            img_link, img_ext = get_link_and_extension_hb(hubble_url_template_img, img_id)
            img_title = f"hubble_{img_id}{img_ext}"
            print(img_title, img_ext, img_link)
            download_img(img_dir, img_title, img_link)
    except requests.HTTPError as error:
        logger.exception(error)


if __name__ == '__main__':
    main()
