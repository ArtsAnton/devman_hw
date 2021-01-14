import logging
import os
import time

import requests
import telegram

from dotenv import load_dotenv


def get_task_description(url, headers, params):
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def create_message_for_user(description, devman_url):
    message = 'У Вас проверили работу "{}"! \n {} \n {}'
    if description['is_negative']:
        lesson_status = 'Задача решена неверно!'
    else:
        lesson_status = 'Задача решена успешно!'
    lesson_title = description['lesson_title']
    lesson_url = devman_url.format(description['lesson_url'])
    return message.format(lesson_title, lesson_status, lesson_url)


def main():
    load_dotenv()
    TG_CHAT_ID = os.getenv("TG_CHAT_ID")
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    DEVMAN_TOKEN = os.getenv("DEVMAN_TOKEN")

    bot = telegram.Bot(token=TELEGRAM_TOKEN)

    devman_url = 'https://dvmn.org{}'
    devman_api_url = 'https://dvmn.org/api/long_polling/'
    headers = {'Authorization': 'Token {}'.format(DEVMAN_TOKEN)}
    params = {'timestamp': time.time()}

    while True:
        task_description = get_task_description(devman_api_url, headers, params)
        try:
            if task_description["status"] == "found":
                bot.send_message(
                    chat_id=TG_CHAT_ID,
                    text=create_message_for_user(
                        task_description['new_attempts'][0],
                        devman_url,
                    ),
                )
                params = {'timestamp': task_description['last_attempt_timestamp']}
            else:
                params = {'timestamp': task_description['timestamp_to_request']}
        except requests.exceptions.HTTPError as http_error:
            logging.warning(http_error)
        except requests.exceptions.ReadTimeout as read_timeout_error:
            logging.warning(read_timeout_error)
        except requests.exceptions.ConnectionError as connection_error:
            logging.warning(connection_error)
            time.sleep(60)


if __name__ == '__main__':
    main()
