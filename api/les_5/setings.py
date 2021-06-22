import os

from dotenv import load_dotenv
load_dotenv()


BASE_URLS = {"hh": "https://api.hh.ru/vacancies/", "sj": "https://api.superjob.ru/2.0/vacancies/"}

PAYLOAD = {"hh": {"specialization": "1.221",
                  "page": None,
                  "per_page": "100",
                  "area": "1",
                  "period": "30",
                  "text": None},
           "sj": {"catalogues": "48",
                  "town": "4",
                  "period": "1",
                  "page": None,
                  "count": "100",
                  "keyword": None}}

HEADERS = {"hh": {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                                "(KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"},
           "sj": {"X-Api-App-Id": os.getenv("SECRET_KEY")}}

TABLE_TITLE = {"hh": "HeadHunter Moscow", "sj": "SuperJob Moscow"}

MAX_VALUE_KEY = {"hh": "found", "sj": "total"}

BATCH_VACANCIES_KEY = {"hh": "items", "sj": "objects"}

