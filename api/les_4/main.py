import requests
import logging
import os
from PIL import Image


logger = logging.getLogger(__file__)


def create_dir_for_img():
    """Create dir if not exists. Return path for images."""
    root = os.path.dirname(__file__)
    new_path = os.path.join(root, 'image')
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    return new_path


def get_links_last_launch_sx(url):
    """The function returns a list of links (links for image) from the last spacex launch."""
    response = requests.get(url)
    response.raise_for_status()
    launch_data = response.json()
    list_img = launch_data['links']['flickr']['original']
    return list_img


def create_name_for_img(title, api_name=True, img_extension='jpg'):
    """"The function returns a name template for the image.
    api_name=True - spacex;
    api_name=False - hubble"""
    if api_name:
        return f"spacex_{title+1}.{img_extension}"
    else:
        return f"hubble_{title}.{img_extension}"


def download_img(path_for_save, url_dl, img_title):
    """The function downloads images."""
    response = requests.get(url_dl, verify=False)
    response.raise_for_status()
    with open(os.path.join(path_for_save, img_title), 'wb') as file:
        file.write(response.content)


def get_list_img_id_hb(url_template, coll_name):
    """The function returns the ID of the images for the collection."""
    url = url_template.format(coll_name)
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


def main():
    url_spacex = 'https://api.spacexdata.com/v4/launches/latest'
    url_template_hubble_img = 'http://hubblesite.org/api/v3/image/{}'
    url_template_hubble_coll = 'http://hubblesite.org/api/v3/images/{}'
    hubble_coll = 'spacecraft'
    dir_img = create_dir_for_img()

    try:
        spacex_links = get_links_last_launch_sx(url_spacex)
        for value, img_link in enumerate(spacex_links):
            img_title = create_name_for_img(value)
            download_img(dir_img, img_link, img_title)

        hubble_img_id = get_list_img_id_hb(url_template_hubble_coll, hubble_coll)
        for img_id in hubble_img_id:
            img_link, ext = get_link_and_extension_hb(url_template_hubble_img, img_id)
            img_title = create_name_for_img(img_id, api_name=False, img_extension=ext)
            download_img(dir_img, img_link, img_title)
    except requests.HTTPError as error:
        logger.exception(error)


if __name__ == '__main__':
    main()
