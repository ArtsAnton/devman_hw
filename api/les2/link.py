import requests
from dotenv import load_dotenv
import os
import sys
from urllib.parse import urlparse


def shorten_link(user_url, url, headers):
    payload = {"long_url": user_url}
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return 'Битлинк:', response.json()['link']


def count_clicks(user_url, url, headers):
    parse_link = urlparse(user_url)
    response = requests.get(url.format(parse_link.netloc, parse_link.path), headers=headers)
    response.raise_for_status()
    return 'Количество переходов:', response.json()['total_clicks']


def is_bitlink(user_url, url, headers):
    res = urlparse(user_url)
    response = requests.get(url.format(res.netloc, res.path), headers=headers)
    return response.ok


def main():
    load_dotenv()
    url_for_gen_link = 'https://api-ssl.bitly.com/v4/bitlinks'
    url_for_count = 'https://api-ssl.bitly.com/v4/bitlinks/{}{}/clicks/summary'
    url_for_check = 'https://api-ssl.bitly.com/v4/bitlinks/{}{}'
    headers = {'Authorization': 'Bearer {}'.format(os.getenv("API_TOKEN"))}
    user_url = input('Введите ссылку: ')

    try:
        if is_bitlink(user_url, url_for_check, headers):
            res = count_clicks(user_url, url_for_count, headers)
        else:
            res = shorten_link(user_url, url_for_gen_link, headers)
        print(*res)
    except requests.exceptions.HTTPError as error:
        sys.exit(error)


if __name__ == '__main__':
    main()
