import os
import time

from dotenv import load_dotenv
from instabot import Bot
from PIL import Image


def conv_ext_to_jpg(dir_img):
    """The function converts the extension to jpg for all images in the directory."""
    for img in os.listdir(dir_img):
        image = Image.open(f"{dir_img}/{img}")
        image.thumbnail((1080, 1080))
        if img.split(".")[1] != 'jpg':
            image.save(f'{dir_img}/{img.split(".")[0]}.jpg')
            os.remove(image.filename)
        else:
            image.save(image.filename)


def main():
    load_dotenv()
    timeout = 24 * 60 * 60
    bot = Bot()
    bot.login(username=os.getenv("INST_LOGIN"),
              password=os.getenv("INST_PASSWORD")
              )
    dir_img = os.path.join(os.getcwd(), 'image')
    conv_ext_to_jpg(dir_img)

    for img in os.listdir(dir_img):
        bot.upload_photo(f'{dir_img}/{img}')
        time.sleep(timeout)


if __name__ == '__main__':
    main()
