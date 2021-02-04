import argparse
import os
import sys

import requests

from dotenv import load_dotenv
from urllib.parse import urlparse


def shorten_link(user_url, url, headers):
    """The function returns bitlink."""
    payload = {"long_url": user_url}
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return 'Битлинк:', response.json()['link']


def count_clicks(user_url, url, headers):
    """The function counts the number of clicks on the  bitlink."""
    parse_link = urlparse(user_url)
    response = requests.get(url.format(parse_link.netloc, parse_link.path), headers=headers)
    response.raise_for_status()
    return 'Количество переходов:', response.json()['total_clicks']


def is_bitlink(user_url, url, headers):
    """The function returns true if the url is a bitlink."""
    res = urlparse(user_url)
    response = requests.get(url.format(res.netloc, res.path), headers=headers)
    return response.ok


def get_user_url():
    """The function returns the user's link."""
    parser = argparse.ArgumentParser()
    parser.add_argument('user_url', help='user url for bitly')
    namespace = parser.parse_args()
    return namespace.user_url


def main():
    load_dotenv()
    url_for_gen_link = 'https://api-ssl.bitly.com/v4/bitlinks'
    url_for_count = 'https://api-ssl.bitly.com/v4/bitlinks/{}{}/clicks/summary'
    url_for_check = 'https://api-ssl.bitly.com/v4/bitlinks/{}{}'
    headers = {'Authorization': 'Bearer {}'.format(os.getenv("API_TOKEN"))}

    try:
        user_url = get_user_url()
        if is_bitlink(user_url, url_for_check, headers):
            res = count_clicks(user_url, url_for_count, headers)
        else:
            res = shorten_link(user_url, url_for_gen_link, headers)
        print(*res)
    except requests.exceptions.HTTPError as error:
        sys.exit(error)


if __name__ == '__main__':
    main()
