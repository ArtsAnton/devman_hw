import logging
import os
import urllib

import requests

from random import randint

from dotenv import load_dotenv


def create_dir_for_img(dirname, path=__file__):
    root = os.path.dirname(path)
    new_path = os.path.join(root, dirname)
    os.makedirs(new_path, exist_ok=True)
    return new_path


def get_random_comic(max_value):
    xkcd_template_url = "http://xkcd.com/{}/info.0.json"
    random_num = randint(1, max_value)
    response = requests.get(xkcd_template_url.format(random_num))
    response.raise_for_status()
    return response.json()


def download_img(url, img_path):
    response = requests.get(url)
    response.raise_for_status()
    path = urllib.parse.urlsplit(url).path
    path = urllib.parse.unquote(path, encoding='utf-8')
    img_name = os.path.split(path)[1]
    with open(os.path.join(img_path, img_name), "wb") as f:
        f.write(response.content)
    return img_name


def get_last_comic_number():
    xkcd_url = "http://xkcd.com/info.0.json"
    response = requests.get(xkcd_url)
    response.raise_for_status()
    return response.json()["num"]


def get_url_for_upload(base_url, group_id, token, api_version):
    api_method = "photos.getWallUploadServer"
    payloads = {"group_id": group_id, "access_token": token, "v": api_version}
    response = requests.get(base_url.format(api_method), payloads)
    response.raise_for_status()
    return response.json()["response"]["upload_url"]


def upload_img_wall(url, group_id, dir, img_name):
    payload = {"group_id": group_id}
    with open(f"{dir}/{img_name}", "rb") as file:
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


def logger():
    logger = logging.getLogger(__file__)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def main():
    load_dotenv()
    log = logger()

    vk_token = os.getenv("VK_TOKEN")
    vk_api_version = 5.131
    vk_group_id = int(os.getenv("VK_GROUP"))
    vk_api_base_url = "https://api.vk.com/method/{}"
    vk_add_post = 1

    img_dir = "image"

    try:
        number_of_comics = get_last_comic_number()

        img_path = create_dir_for_img(img_dir)
        random_comic = get_random_comic(number_of_comics)
        img_title, img_url = random_comic["title"], random_comic["img"]
        img_name = download_img(img_url, img_path)

        upload_url = get_url_for_upload(vk_api_base_url, vk_group_id, vk_token, vk_api_version)
        upload_attr = upload_img_wall(upload_url, vk_group_id, img_path, img_name)
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
        log.info("Add new post: {}.".format(post_id))
    except requests.HTTPError as error:
        log.exception(error)


if __name__ == "__main__":
    main()
