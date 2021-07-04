import logging
import os
import urllib

import requests

from random import randint

from dotenv import load_dotenv


logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def create_dir_for_img(path=__file__):
    root = os.path.dirname(path)
    new_path = os.path.join(root, "image")
    os.makedirs(new_path, exist_ok=True)
    return new_path


def get_img(url, number):
    response = requests.get(url.format(number))
    response.raise_for_status()
    return response.json()


def download_img2(url, img_path):
    response = requests.get(url)
    response.raise_for_status()
    path = urllib.parse.urlsplit(url).path
    img_name = os.path.split(path)[1]
    with open(os.path.join(img_path, img_name), "wb") as f:
        f.write(response.content)


def get_number_imgs(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()["num"]


def get_url_for_upload(base_url, group_id, token, api_version):
    api_method = "photos.getWallUploadServer"
    payloads = {"group_id": group_id, "access_token": token, "v": api_version}
    response = requests.get(base_url.format(api_method), payloads)
    response.raise_for_status()
    return response.json()["response"]["upload_url"]


def upload_img_wall(url, group_id, dir):
    payload = {"group_id": group_id}
    img_name = os.listdir(dir)[0]
    with open(f"{dir}/{img_name}", 'rb') as file:
        files = {"photo": file}
        response = requests.post(url, params=payload, files=files)
    response.raise_for_status()
    os.remove(f"{dir}/{img_name}")
    return response.json()


def save_wall_img(url, group_id, token, api_version, attr):
    api_method = "photos.saveWallPhoto"
    payloads = {"group_id": group_id,
                "photo": attr["photo"],
                "server": attr["server"],
                "hash": attr["hash"],
                "access_token": token,
                "v": api_version}
    response = requests.get(url.format(api_method), params=payloads)
    response.raise_for_status()
    return response.json()


def add_post(url, group_id, msg, post, owner_id, media_id, token, api_version):
    api_method = "wall.post"
    payloads = {"owner_id": group_id*(-1),
                "message": msg,
                "from_group": post,
                "attachments": f"type{owner_id}_{media_id}",
                "access_token": token,
                "v": api_version}
    response = requests.get(url.format(api_method), params=payloads)
    response.raise_for_status()
    return response.json()["response"]["post_id"]


def main():
    load_dotenv()

    vk_token = os.getenv("VK_TOKEN")
    vk_api_version = 5.131
    vk_group_id = int(os.getenv("VK_GROUP"))
    vk_api_base_url = "https://api.vk.com/method/{}"
    vk_add_post = 1
    xkcd_url = "http://xkcd.com/info.0.json"
    xkcd_template_url = "http://xkcd.com/{}/info.0.json"

    try:
        number_imgs = get_number_imgs(xkcd_url)
        random_num = randint(1, number_imgs)

        img_path = create_dir_for_img()
        img = get_img(xkcd_template_url, random_num)
        img_title, img_url = img["title"], img["img"]
        download_img2(img_url, img_path)

        upload_url = get_url_for_upload(vk_api_base_url, vk_group_id, vk_token, vk_api_version)
        upload_attr = upload_img_wall(upload_url, vk_group_id, img_path)
        save_attr = save_wall_img(vk_api_base_url, vk_group_id, vk_token, vk_api_version, upload_attr)

        media_id = save_attr["response"][0]["id"]
        owner_id = save_attr["response"][0]["owner_id"]

        post_id = add_post(vk_api_base_url,
                           vk_group_id,
                           img_title,
                           vk_add_post,
                           owner_id,
                           media_id,
                           vk_token,
                           vk_api_version)
        logger.info("Add new post: {}.".format(post_id))
    except requests.HTTPError as error:
        logger.exception(error)


if __name__ == "__main__":
    main()
