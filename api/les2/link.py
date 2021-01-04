import requests
from dotenv import load_dotenv
import os
import sys
from urllib.parse import urlparse


load_dotenv()
URL = 'https://api-ssl.bitly.com/v4/bitlinks'
HEADERS = {'Authorization': 'Bearer {}'.format(os.getenv("API_TOKEN"))}


def shorten_link(url):
    requests.get(url).raise_for_status()
    payload = {"long_url": url}
    response = requests.post(URL, headers=HEADERS, json=payload)
    return 'Битлинк:', response.json()['link']


def count_clicks(url):
    requests.get(url).raise_for_status()
    parse_link = urlparse(url)
    response = requests.get((URL + '/{}/clicks/summary').format(parse_link.netloc + parse_link.path), headers=HEADERS)
    return 'Количество переходов:', response.json()['total_clicks']


def main():
    url = input('Введите ссылку: ')
    try:
        if url.startswith('http://bit.ly') or url.startswith('https://bit.ly'):
            res = count_clicks(url)
        else:
            res = shorten_link(url)
    except requests.exceptions.HTTPError as error:
        sys.exit(error)
    else:
        print(*res)


if __name__ == '__main__':
    main()

