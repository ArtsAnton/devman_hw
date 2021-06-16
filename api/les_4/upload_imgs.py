import os
import time

from dotenv import load_dotenv
from instabot import Bot
from PIL import Image


def process_imgs(dir_img, size):
    """The function processes all images in the directory before loading."""
    for img in os.listdir(dir_img):
        image = Image.open(f"{dir_img}/{img}")
        image.thumbnail((size, size))
        img_ext = os.path.splitext(img)[1]
        if img_ext != ".jpg":
            image.save(f"{dir_img}/{img}.jpg")
            os.remove(image.filename)
        else:
            image.save(image.filename)


def main():
    load_dotenv()
    timeout = 24 * 60 * 60
    max_img_size = 1080
    bot = Bot()
    bot.login(username=os.getenv("INST_LOGIN"),
              password=os.getenv("INST_PASSWORD")
              )
    dir_img = os.path.join(os.getcwd(), "image")
    process_imgs(dir_img, max_img_size)

    for img in os.listdir(dir_img):
        bot.upload_photo(f"{dir_img}/{img}")
        time.sleep(timeout)


if __name__ == "__main__":
    main()
