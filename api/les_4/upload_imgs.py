import os
import time

from dotenv import load_dotenv
from instabot import Bot
from PIL import Image


def create_img_to_dl(dir_img):
    for img in os.listdir(dir_img):
        image = Image.open(f"image/{img}")
        image.thumbnail((1080, 1080))
        if img.split(".")[1] != 'jpg':
            image.save(f'image/{img.split(".")[0]}.jpg')
            os.remove(image.filename)
        else:
            image.save(f'{image.filename}')


def main():
    load_dotenv()
    timeout = 24 * 60 * 60
    bot = Bot()
    bot.login(username=os.getenv("INST_LOGIN"),
              password=os.getenv("INST_PASSWORD")
              )
    dir_img = os.path.join(os.getcwd(), 'image')
    create_img_to_dl(dir_img)

    for img in os.listdir(dir_img):
        bot.upload_photo(f'image/{img}')
        time.sleep(timeout)


if __name__ == '__main__':
    main()
