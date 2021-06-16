import logging

import requests

from utils import create_dir_for_img, download_img


logger = logging.getLogger(__file__)


def get_links_last_launch(url):
    """The function returns a list of links (links for image) from the last spacex launch."""
    response = requests.get(url)
    response.raise_for_status()
    launch = response.json()
    links = launch["links"]["flickr"]["original"]
    return links


def main():
    spacex_url = "https://api.spacexdata.com/v4/launches/latest"
    img_dir = create_dir_for_img()

    try:
        spacex_links = get_links_last_launch(spacex_url)
        for current_id, img_link in enumerate(spacex_links, start=1):
            img_title = f"spacex_{current_id}.jpg"
            download_img(img_dir, img_title, img_link)

    except requests.HTTPError as error:
        logger.exception(error)


if __name__ == "__main__":
    main()
